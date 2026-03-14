"""Document manager for loading, editing, and versioning server documents."""

import json
import logging
import re
import shutil
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

LOG = logging.getLogger("playpalace.documents")

_MAX_HISTORY_PER_LOCALE = 5


class DocumentManager:
    """Manages document metadata, content, edit locks, and version history.

    Documents live in a directory tree where each subfolder is a document,
    containing locale-specific ``.md`` files and a ``_metadata.json``.
    """

    def __init__(self, documents_dir: Path):
        self._dir = documents_dir
        self._categories: dict = {}  # slug -> {sort, name: {locale: str}}
        self._documents: dict = {}  # folder_name -> document metadata dict
        self._edit_locks: dict = {}  # (folder_name, locale) -> {user, timestamp}

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load(self) -> int:
        """Load document metadata from disk.

        Returns the number of documents loaded.
        """
        self._dir.mkdir(parents=True, exist_ok=True)

        # Load or create root metadata
        root_meta_path = self._dir / "_metadata.json"
        if root_meta_path.exists():
            with open(root_meta_path, "r", encoding="utf-8") as f:
                root_meta = json.load(f)
            self._categories = root_meta.get("categories", {})
        else:
            self._categories = {}
            self._save_root_metadata()

        # Scan document subfolders
        self._documents.clear()
        for entry in sorted(self._dir.iterdir()):
            if not entry.is_dir():
                continue
            if entry.name.startswith("_"):
                continue

            doc_meta_path = entry / "_metadata.json"
            if doc_meta_path.exists():
                with open(doc_meta_path, "r", encoding="utf-8") as f:
                    self._documents[entry.name] = json.load(f)
            else:
                # Auto-generate metadata for existing document folders
                self._documents[entry.name] = self._generate_default_metadata(entry)
                self._save_document_metadata(entry.name)

        return len(self._documents)

    def _generate_default_metadata(self, folder: Path) -> dict:
        """Generate default metadata for a document folder without one."""
        now = datetime.now(timezone.utc).isoformat()
        title = folder.name.replace("_", " ").title()

        # Detect existing locale files
        locales = {}
        locale_codes = []
        for md_file in sorted(folder.glob("*.md")):
            locale_code = md_file.stem
            locale_codes.append(locale_code)
            locales[locale_code] = {
                "created": now,
                "modified_contents": now,
                "public": True,
            }

        # Ensure at least an 'en' entry
        if not locales:
            locale_codes.append("en")
            locales["en"] = {
                "created": now,
                "modified_contents": now,
                "public": True,
            }

        titles = {code: title for code in locale_codes}

        return {
            "categories": [],
            "source_locale": "en",
            "titles": titles,
            "locales": locales,
        }

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_categories(self, locale: str) -> list[dict]:
        """Return categories sorted by sort order with display names.

        Each entry has keys ``slug`` and ``name``.
        """
        result = []
        for slug, info in self._categories.items():
            names = info.get("name", {})
            display = names.get(locale) or names.get("en") or slug
            result.append({"slug": slug, "name": display})
        result.sort(key=lambda c: c["name"].lower())
        return result

    def get_category_document_counts(self) -> dict[str | None, int]:
        """Return document counts per category in a single pass.

        Keys are category slugs, plus ``None`` for all documents and
        ``""`` for uncategorized.
        """
        counts: dict[str | None, int] = {None: len(self._documents), "": 0}
        for meta in self._documents.values():
            cats = meta.get("categories", [])
            if not cats:
                counts[""] += 1
            for slug in cats:
                counts[slug] = counts.get(slug, 0) + 1
        return counts

    def get_documents_in_category(
        self, category_slug: str | None, locale: str
    ) -> list[dict]:
        """Return documents in a category.

        Args:
            category_slug: Category slug to filter by.  ``None`` returns all
                documents, ``""`` returns uncategorized documents.
            locale: Locale for display title resolution.

        Returns a list of dicts with ``folder_name`` and ``title``.
        """
        results = []
        for folder_name, meta in self._documents.items():
            cats = meta.get("categories", [])
            if category_slug is None:
                pass  # include all
            elif category_slug == "":
                if cats:
                    continue
            else:
                if category_slug not in cats:
                    continue

            titles = meta.get("titles", {})
            title = titles.get(locale) or titles.get("en") or folder_name
            # Include sort-relevant timestamps from source locale.
            source = meta.get("source_locale", "en")
            loc_info = meta.get("locales", {}).get(source, {})
            results.append({
                "folder_name": folder_name,
                "title": title,
                "created": loc_info.get("created", ""),
                "modified": loc_info.get("modified_contents", ""),
            })

        sort_method = self.get_category_sort(category_slug) if category_slug else "alphabetical"
        if sort_method == "date_created":
            results.sort(key=lambda d: d["created"], reverse=True)
        elif sort_method == "date_modified":
            results.sort(key=lambda d: d["modified"], reverse=True)
        else:
            results.sort(key=lambda d: d["title"].lower())
        return results

    def get_document_metadata(self, folder_name: str) -> dict | None:
        """Return the full metadata dict for a document, or None."""
        return self._documents.get(folder_name)

    def get_document_locale_count(self, folder_name: str) -> int:
        """Return the number of locales for a document."""
        meta = self._documents.get(folder_name)
        if meta is None:
            return 0
        return len(meta.get("locales", {}))

    def get_document_content(self, folder_name: str, locale: str) -> str | None:
        """Read a document's ``.md`` file for the given locale."""
        if folder_name not in self._documents:
            return None
        md_path = self._dir / folder_name / f"{locale}.md"
        if not md_path.exists():
            return None
        return md_path.read_text(encoding="utf-8")

    # ------------------------------------------------------------------
    # Writing
    # ------------------------------------------------------------------

    def save_document_content(
        self,
        folder_name: str,
        locale: str,
        content: str,
        editor_username: str,
    ) -> bool:
        """Write document content, back up the previous version, and release lock.

        Returns ``True`` on success, ``False`` if the document doesn't exist.
        """
        if folder_name not in self._documents:
            return False

        md_path = self._dir / folder_name / f"{locale}.md"

        # Back up existing version before overwriting
        if md_path.exists():
            self._backup_version(folder_name, locale)

        md_path.write_text(content, encoding="utf-8")

        # Update metadata timestamp
        meta = self._documents[folder_name]
        locales = meta.setdefault("locales", {})
        now = datetime.now(timezone.utc).isoformat()
        if locale in locales:
            locales[locale]["modified_contents"] = now
        else:
            locales[locale] = {
                "created": now,
                "modified_contents": now,
                "public": True,
            }
        self._save_document_metadata(folder_name)

        # Release edit lock
        self.release_edit_lock(folder_name, locale, editor_username)
        return True

    def create_document(
        self,
        folder_name: str,
        categories: list[str],
        locale: str,
        title: str,
        content: str,
    ) -> bool:
        """Create a new document folder with initial content.

        Returns ``False`` if a document with that folder name already exists.
        """
        if folder_name in self._documents:
            return False

        doc_dir = self._dir / folder_name
        doc_dir.mkdir(parents=True, exist_ok=True)

        now = datetime.now(timezone.utc).isoformat()
        meta = {
            "categories": categories,
            "source_locale": locale,
            "titles": {locale: title},
            "locales": {
                locale: {
                    "created": now,
                    "modified_contents": now,
                    "public": True,
                }
            },
        }
        self._documents[folder_name] = meta
        self._save_document_metadata(folder_name)

        md_path = doc_dir / f"{locale}.md"
        md_path.write_text(content, encoding="utf-8")
        return True

    def set_document_title(
        self, folder_name: str, locale: str, title: str
    ) -> bool:
        """Update the title for a locale in document metadata.

        Titles are stored separately from locale entries, so setting a title
        for a locale that has no translation yet does not create a locale entry.

        Returns ``True`` on success, ``False`` if the document is not found.
        """
        meta = self._documents.get(folder_name)
        if meta is None:
            return False
        titles = meta.setdefault("titles", {})
        titles[locale] = title
        self._save_document_metadata(folder_name)
        return True

    def set_document_visibility(
        self, folder_name: str, locale: str, public: bool
    ) -> bool:
        """Update the public flag for a locale in document metadata.

        Returns ``True`` on success, ``False`` if document or locale not found.
        """
        meta = self._documents.get(folder_name)
        if meta is None:
            return False
        locales = meta.get("locales", {})
        if locale not in locales:
            return False
        locales[locale]["public"] = public
        self._save_document_metadata(folder_name)
        return True

    def set_document_categories(
        self, folder_name: str, categories: list[str]
    ) -> bool:
        """Replace the category list for a document.

        Returns ``True`` on success, ``False`` if document not found.
        """
        meta = self._documents.get(folder_name)
        if meta is None:
            return False
        meta["categories"] = categories
        self._save_document_metadata(folder_name)
        return True

    def add_document_translation(
        self, folder_name: str, locale: str, title: str, content: str
    ) -> bool:
        """Create a new locale entry (private by default) and write the .md file.

        Returns ``False`` if the document doesn't exist or the locale already exists.
        """
        meta = self._documents.get(folder_name)
        if meta is None:
            return False
        locales = meta.setdefault("locales", {})
        if locale in locales:
            return False
        now = datetime.now(timezone.utc).isoformat()
        locales[locale] = {
            "created": now,
            "modified_contents": now,
            "public": False,
        }
        titles = meta.setdefault("titles", {})
        titles[locale] = title
        md_path = self._dir / folder_name / f"{locale}.md"
        md_path.write_text(content, encoding="utf-8")
        self._save_document_metadata(folder_name)
        return True

    def remove_document_translation(
        self, folder_name: str, locale: str, *, remove_title: bool = True,
    ) -> bool:
        """Delete a locale entry, its .md file, and history backups.

        When *remove_title* is ``False`` the title for the locale is kept
        in metadata so it can be reused if the translation is re-added later.

        Returns ``False`` if the locale is the source locale or doesn't exist.
        """
        meta = self._documents.get(folder_name)
        if meta is None:
            return False
        if meta.get("source_locale") == locale:
            return False
        locales = meta.get("locales", {})
        if locale not in locales:
            return False
        del locales[locale]
        if remove_title:
            meta.get("titles", {}).pop(locale, None)
        md_path = self._dir / folder_name / f"{locale}.md"
        if md_path.exists():
            md_path.unlink()
        # Remove history backups for this locale
        history_dir = self._dir / folder_name / "_history"
        if history_dir.exists():
            for backup in history_dir.glob(f"{locale}_*.md"):
                backup.unlink()
        self._save_document_metadata(folder_name)
        # Fail-safe: clean up orphaned locks.  The browsing layer checks
        # for active locks *before* calling this method and blocks the
        # removal when someone is editing.  This cleanup handles cases
        # where the data is removed outside the UI (e.g. filesystem
        # deletion, or a reconnected client whose lock was already stale).
        self._edit_locks.pop((folder_name, locale), None)
        return True

    def delete_document(self, folder_name: str) -> bool:
        """Remove a document folder from disk and from memory.

        Returns ``False`` if the document doesn't exist.
        """
        if folder_name not in self._documents:
            return False
        doc_dir = self._dir / folder_name
        if doc_dir.exists():
            shutil.rmtree(doc_dir)
        del self._documents[folder_name]
        # Fail-safe: clean up orphaned locks.  The browsing layer checks
        # for active locks *before* calling this method and blocks the
        # deletion when someone is editing.  This cleanup handles cases
        # where the document is removed outside the UI (e.g. filesystem
        # deletion, or a reconnected client whose lock was already stale).
        stale = [key for key in self._edit_locks if key[0] == folder_name]
        for key in stale:
            del self._edit_locks[key]
        return True

    def create_category(self, slug: str, name: str, locale: str) -> bool:
        """Create a new category.

        Returns ``False`` if the slug already exists.
        """
        if slug in self._categories:
            return False
        self._categories[slug] = {
            "sort": "alphabetical",
            "name": {locale: name},
        }
        self._save_root_metadata()
        return True

    def delete_category(self, slug: str) -> bool:
        """Delete a category and remove it from all documents.

        Returns ``False`` if the category doesn't exist.
        """
        if slug not in self._categories:
            return False
        del self._categories[slug]
        self._save_root_metadata()
        # Remove from all documents that reference this category.
        for folder_name, meta in self._documents.items():
            cats = meta.get("categories", [])
            if slug in cats:
                cats.remove(slug)
                self._save_document_metadata(folder_name)
        return True

    def rename_category(self, slug: str, name: str, locale: str) -> bool:
        """Update the display name for a category in a specific locale.

        Returns ``False`` if the category doesn't exist.
        """
        cat = self._categories.get(slug)
        if cat is None:
            return False
        cat.setdefault("name", {})[locale] = name
        self._save_root_metadata()
        return True

    def set_category_sort(self, slug: str, sort_method: str) -> bool:
        """Update the sort method for a category.

        Returns ``False`` if the category doesn't exist.
        """
        cat = self._categories.get(slug)
        if cat is None:
            return False
        cat["sort"] = sort_method
        self._save_root_metadata()
        return True

    def get_category_sort(self, slug: str) -> str:
        """Return the sort method for a category (default ``"alphabetical"``)."""
        cat = self._categories.get(slug)
        if cat is None:
            return "alphabetical"
        return cat.get("sort", "alphabetical")

    @staticmethod
    def slugify(title: str) -> str:
        """Convert a document title to a folder-name slug.

        Lowercases, replaces whitespace/hyphens with underscores, strips
        non-ASCII and special characters, and collapses runs of underscores.
        """
        slug = unicodedata.normalize("NFKD", title)
        slug = slug.encode("ascii", "ignore").decode("ascii")
        slug = slug.lower()
        slug = re.sub(r"[\s\-]+", "_", slug)
        slug = re.sub(r"[^\w]", "", slug)
        slug = re.sub(r"_+", "_", slug)
        slug = slug.strip("_")
        return slug

    # ------------------------------------------------------------------
    # Edit locks
    # ------------------------------------------------------------------

    def acquire_edit_lock(
        self, folder_name: str, locale: str, username: str
    ) -> str | None:
        """Attempt to acquire an edit lock.

        Returns ``None`` on success, or the locking username on failure.
        """
        self.cleanup_stale_locks()
        key = (folder_name, locale)
        existing = self._edit_locks.get(key)
        if existing and existing["user"] != username:
            return existing["user"]
        self._edit_locks[key] = {"user": username, "timestamp": time.time()}
        return None

    def release_edit_lock(
        self, folder_name: str, locale: str, username: str
    ) -> None:
        """Release an edit lock if held by *username*."""
        key = (folder_name, locale)
        existing = self._edit_locks.get(key)
        if existing and existing["user"] == username:
            del self._edit_locks[key]

    def get_edit_lock_holder(
        self, folder_name: str, locale: str
    ) -> str | None:
        """Return the username holding the lock, or ``None``."""
        self.cleanup_stale_locks()
        lock = self._edit_locks.get((folder_name, locale))
        return lock["user"] if lock else None

    def get_document_lock_holders(self, folder_name: str) -> dict[str, str]:
        """Return ``{locale: username}`` for every active lock on *folder_name*."""
        self.cleanup_stale_locks()
        return {
            locale: lock["user"]
            for (doc, locale), lock in self._edit_locks.items()
            if doc == folder_name
        }

    def cleanup_stale_locks(self, timeout_seconds: int = 1800) -> None:
        """Remove locks older than *timeout_seconds*."""
        now = time.time()
        stale = [
            key
            for key, lock in self._edit_locks.items()
            if now - lock["timestamp"] > timeout_seconds
        ]
        for key in stale:
            del self._edit_locks[key]

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------

    def _save_root_metadata(self) -> None:
        """Write categories to the root ``_metadata.json``."""
        path = self._dir / "_metadata.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"categories": self._categories}, f, indent=4, ensure_ascii=False)

    def _save_document_metadata(self, folder_name: str) -> None:
        """Write a document's ``_metadata.json``."""
        meta = self._documents.get(folder_name)
        if meta is None:
            return
        path = self._dir / folder_name / "_metadata.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=4, ensure_ascii=False)

    def _backup_version(self, folder_name: str, locale: str) -> None:
        """Copy the current ``.md`` to ``_history/`` and enforce version cap."""
        md_path = self._dir / folder_name / f"{locale}.md"
        if not md_path.exists():
            return

        history_dir = self._dir / folder_name / "_history"
        history_dir.mkdir(exist_ok=True)

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup_name = f"{locale}_{timestamp}.md"
        shutil.copy2(md_path, history_dir / backup_name)

        # Enforce per-locale cap
        backups = sorted(
            history_dir.glob(f"{locale}_*.md"),
            key=lambda p: p.name,
        )
        while len(backups) > _MAX_HISTORY_PER_LOCALE:
            oldest = backups.pop(0)
            oldest.unlink()
