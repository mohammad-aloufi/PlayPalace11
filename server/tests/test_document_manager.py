"""Tests for the DocumentManager class."""

from __future__ import annotations

import json
import time

import pytest

from server.core.documents.manager import DocumentManager


@pytest.fixture
def docs_dir(tmp_path):
    """Return a clean temporary documents directory."""
    d = tmp_path / "documents"
    d.mkdir()
    return d


@pytest.fixture
def manager(docs_dir):
    return DocumentManager(docs_dir)


# ------------------------------------------------------------------
# load()
# ------------------------------------------------------------------


class TestLoad:
    def test_load_empty_directory(self, manager, docs_dir):
        count = manager.load()
        assert count == 0
        # Root _metadata.json should be created
        assert (docs_dir / "_metadata.json").exists()

    def test_load_creates_root_metadata_if_missing(self, manager, docs_dir):
        assert not (docs_dir / "_metadata.json").exists()
        manager.load()
        with open(docs_dir / "_metadata.json", encoding="utf-8") as f:
            data = json.load(f)
        assert data == {"categories": {}}

    def test_load_with_existing_root_metadata(self, manager, docs_dir):
        root_meta = {
            "categories": {
                "rules": {"sort": "alphabetical", "name": {"en": "Game Rules"}}
            }
        }
        with open(docs_dir / "_metadata.json", "w", encoding="utf-8") as f:
            json.dump(root_meta, f)

        manager.load()
        cats = manager.get_categories("en")
        assert len(cats) == 1
        assert cats[0]["slug"] == "rules"
        assert cats[0]["name"] == "Game Rules"

    def test_load_existing_documents_auto_generates_metadata(self, manager, docs_dir):
        doc_dir = docs_dir / "my_doc"
        doc_dir.mkdir()
        (doc_dir / "en.md").write_text("Hello", encoding="utf-8")

        count = manager.load()
        assert count == 1
        # _metadata.json should now exist
        assert (doc_dir / "_metadata.json").exists()
        with open(doc_dir / "_metadata.json", encoding="utf-8") as f:
            meta = json.load(f)
        assert "en" in meta["locales"]
        assert meta["titles"]["en"] == "My Doc"
        assert meta["source_locale"] == "en"

    def test_load_existing_documents_with_metadata(self, manager, docs_dir):
        doc_dir = docs_dir / "test_doc"
        doc_dir.mkdir()
        (doc_dir / "en.md").write_text("Content", encoding="utf-8")
        meta = {
            "categories": ["rules"],
            "source_locale": "en",
            "titles": {"en": "Custom Title"},
            "locales": {
                "en": {
                    "created": "2026-01-01T00:00:00Z",
                    "modified_contents": "2026-01-01T00:00:00Z",
                    "public": True,
                }
            },
        }
        with open(doc_dir / "_metadata.json", "w", encoding="utf-8") as f:
            json.dump(meta, f)

        count = manager.load()
        assert count == 1
        docs = manager.get_documents_in_category(None, "en")
        assert docs[0]["title"] == "Custom Title"

    def test_load_skips_underscore_dirs(self, manager, docs_dir):
        hidden = docs_dir / "_internal"
        hidden.mkdir()
        (hidden / "en.md").write_text("hidden", encoding="utf-8")

        count = manager.load()
        assert count == 0

    def test_load_multiple_locales_detected(self, manager, docs_dir):
        doc_dir = docs_dir / "multi_lang"
        doc_dir.mkdir()
        (doc_dir / "en.md").write_text("English", encoding="utf-8")
        (doc_dir / "es.md").write_text("Spanish", encoding="utf-8")

        manager.load()
        meta_path = doc_dir / "_metadata.json"
        with open(meta_path, encoding="utf-8") as f:
            meta = json.load(f)
        assert "en" in meta["locales"]
        assert "es" in meta["locales"]


# ------------------------------------------------------------------
# get_categories
# ------------------------------------------------------------------


class TestGetCategories:
    def test_locale_fallback_to_english(self, manager, docs_dir):
        root_meta = {
            "categories": {
                "news": {
                    "sort": "alphabetical",
                    "name": {"en": "News", "es": "Noticias"},
                }
            }
        }
        with open(docs_dir / "_metadata.json", "w", encoding="utf-8") as f:
            json.dump(root_meta, f)
        manager.load()

        cats_fr = manager.get_categories("fr")
        assert cats_fr[0]["name"] == "News"  # falls back to en

        cats_es = manager.get_categories("es")
        assert cats_es[0]["name"] == "Noticias"

    def test_fallback_to_slug(self, manager, docs_dir):
        root_meta = {"categories": {"misc": {"sort": "alphabetical", "name": {}}}}
        with open(docs_dir / "_metadata.json", "w", encoding="utf-8") as f:
            json.dump(root_meta, f)
        manager.load()

        cats = manager.get_categories("en")
        assert cats[0]["name"] == "misc"


# ------------------------------------------------------------------
# get_documents_in_category
# ------------------------------------------------------------------


class TestGetDocumentsInCategory:
    def _setup_docs(self, docs_dir):
        """Create two docs, one categorized and one not."""
        root_meta = {
            "categories": {
                "rules": {"sort": "alphabetical", "name": {"en": "Rules"}}
            }
        }
        with open(docs_dir / "_metadata.json", "w", encoding="utf-8") as f:
            json.dump(root_meta, f)

        for name, cats in [("doc_a", ["rules"]), ("doc_b", [])]:
            d = docs_dir / name
            d.mkdir()
            (d / "en.md").write_text(f"{name} content", encoding="utf-8")
            meta = {
                "categories": cats,
                "source_locale": "en",
                "titles": {"en": name.replace("_", " ").title()},
                "locales": {
                    "en": {
                        "created": "2026-01-01T00:00:00Z",
                        "modified_contents": "2026-01-01T00:00:00Z",
                        "public": True,
                    }
                },
            }
            with open(d / "_metadata.json", "w", encoding="utf-8") as f:
                json.dump(meta, f)

    def test_filter_by_category(self, manager, docs_dir):
        self._setup_docs(docs_dir)
        manager.load()
        docs = manager.get_documents_in_category("rules", "en")
        assert len(docs) == 1
        assert docs[0]["folder_name"] == "doc_a"

    def test_uncategorized(self, manager, docs_dir):
        self._setup_docs(docs_dir)
        manager.load()
        docs = manager.get_documents_in_category("", "en")
        assert len(docs) == 1
        assert docs[0]["folder_name"] == "doc_b"

    def test_all_documents(self, manager, docs_dir):
        self._setup_docs(docs_dir)
        manager.load()
        docs = manager.get_documents_in_category(None, "en")
        assert len(docs) == 2


# ------------------------------------------------------------------
# get_document_content
# ------------------------------------------------------------------


class TestGetDocumentContent:
    def test_reads_md_on_demand(self, manager, docs_dir):
        doc_dir = docs_dir / "hello"
        doc_dir.mkdir()
        (doc_dir / "en.md").write_text("# Hello World", encoding="utf-8")
        manager.load()

        content = manager.get_document_content("hello", "en")
        assert content == "# Hello World"

    def test_returns_none_for_missing_locale(self, manager, docs_dir):
        doc_dir = docs_dir / "hello"
        doc_dir.mkdir()
        (doc_dir / "en.md").write_text("hi", encoding="utf-8")
        manager.load()

        assert manager.get_document_content("hello", "fr") is None

    def test_returns_none_for_missing_document(self, manager):
        manager.load()
        assert manager.get_document_content("nonexistent", "en") is None


# ------------------------------------------------------------------
# save_document_content
# ------------------------------------------------------------------


class TestSaveDocumentContent:
    def test_writes_file_and_updates_timestamp(self, manager, docs_dir):
        doc_dir = docs_dir / "editable"
        doc_dir.mkdir()
        (doc_dir / "en.md").write_text("original", encoding="utf-8")
        manager.load()

        original_ts = manager._documents["editable"]["locales"]["en"]["modified_contents"]
        result = manager.save_document_content("editable", "en", "updated", "alice")
        assert result is True
        assert (doc_dir / "en.md").read_text(encoding="utf-8") == "updated"
        new_ts = manager._documents["editable"]["locales"]["en"]["modified_contents"]
        assert new_ts != original_ts

    def test_creates_new_locale_entry_on_save(self, manager, docs_dir):
        doc_dir = docs_dir / "editable"
        doc_dir.mkdir()
        (doc_dir / "en.md").write_text("english", encoding="utf-8")
        manager.load()

        result = manager.save_document_content("editable", "fr", "français", "bob")
        assert result is True
        assert "fr" in manager._documents["editable"]["locales"]

    def test_returns_false_for_unknown_document(self, manager):
        manager.load()
        assert manager.save_document_content("nope", "en", "x", "alice") is False


# ------------------------------------------------------------------
# Version history
# ------------------------------------------------------------------


class TestVersionHistory:
    def test_backup_created_on_save(self, manager, docs_dir):
        doc_dir = docs_dir / "versioned"
        doc_dir.mkdir()
        (doc_dir / "en.md").write_text("v1", encoding="utf-8")
        manager.load()

        manager.save_document_content("versioned", "en", "v2", "alice")
        history = list((doc_dir / "_history").glob("en_*.md"))
        assert len(history) == 1
        assert history[0].read_text(encoding="utf-8") == "v1"

    def test_version_cap_enforced(self, manager, docs_dir):
        doc_dir = docs_dir / "capped"
        doc_dir.mkdir()
        (doc_dir / "en.md").write_text("v0", encoding="utf-8")
        manager.load()

        # Pre-create 6 backup files to test the cap without timestamp collisions
        history_dir = doc_dir / "_history"
        history_dir.mkdir()
        for i in range(6):
            (history_dir / f"en_20260101T0000{i:02d}Z.md").write_text(
                f"old_v{i}", encoding="utf-8"
            )
        assert len(list(history_dir.glob("en_*.md"))) == 6

        # One more save triggers backup + prune
        manager.save_document_content("capped", "en", "v_new", "alice")

        history = list(history_dir.glob("en_*.md"))
        assert len(history) == 5  # cap


# ------------------------------------------------------------------
# Edit locks
# ------------------------------------------------------------------


class TestEditLocks:
    def test_acquire_and_release(self, manager):
        manager.load()
        result = manager.acquire_edit_lock("doc", "en", "alice")
        assert result is None  # success
        manager.release_edit_lock("doc", "en", "alice")

    def test_conflict_detection(self, manager):
        manager.load()
        manager.acquire_edit_lock("doc", "en", "alice")
        result = manager.acquire_edit_lock("doc", "en", "bob")
        assert result == "alice"

    def test_same_user_reacquires(self, manager):
        manager.load()
        manager.acquire_edit_lock("doc", "en", "alice")
        result = manager.acquire_edit_lock("doc", "en", "alice")
        assert result is None

    def test_stale_lock_cleanup(self, manager):
        manager.load()
        manager.acquire_edit_lock("doc", "en", "alice")
        # Manually age the lock
        manager._edit_locks[("doc", "en")]["timestamp"] = time.time() - 3600

        manager.cleanup_stale_locks(timeout_seconds=1800)
        # Lock should be cleaned up, so bob can acquire
        result = manager.acquire_edit_lock("doc", "en", "bob")
        assert result is None

    def test_save_releases_lock(self, manager, docs_dir):
        doc_dir = docs_dir / "locked"
        doc_dir.mkdir()
        (doc_dir / "en.md").write_text("text", encoding="utf-8")
        manager.load()

        manager.acquire_edit_lock("locked", "en", "alice")
        manager.save_document_content("locked", "en", "new text", "alice")
        # Lock should be released
        assert ("locked", "en") not in manager._edit_locks


# ------------------------------------------------------------------
# create_document / create_category
# ------------------------------------------------------------------


class TestCreateOperations:
    def test_create_document(self, manager, docs_dir):
        manager.load()
        result = manager.create_document("new_doc", ["rules"], "en", "New Doc", "# New")
        assert result is True
        assert (docs_dir / "new_doc" / "en.md").exists()
        assert (docs_dir / "new_doc" / "_metadata.json").exists()
        assert manager.get_document_content("new_doc", "en") == "# New"

    def test_create_duplicate_document_fails(self, manager, docs_dir):
        manager.load()
        manager.create_document("dup", [], "en", "Dup", "content")
        result = manager.create_document("dup", [], "en", "Dup", "content2")
        assert result is False

    def test_create_category(self, manager, docs_dir):
        manager.load()
        result = manager.create_category("faq", "FAQ", "en")
        assert result is True
        cats = manager.get_categories("en")
        assert any(c["slug"] == "faq" for c in cats)

    def test_create_duplicate_category_fails(self, manager, docs_dir):
        manager.load()
        manager.create_category("faq", "FAQ", "en")
        result = manager.create_category("faq", "FAQ 2", "en")
        assert result is False


# ------------------------------------------------------------------
# slugify
# ------------------------------------------------------------------


class TestSlugify:
    def test_basic_title(self):
        assert DocumentManager.slugify("Uno Rules") == "uno_rules"

    def test_special_characters(self):
        assert DocumentManager.slugify("FAQ & Tips!") == "faq_tips"

    def test_hyphens_become_underscores(self):
        assert DocumentManager.slugify("how-to-play") == "how_to_play"

    def test_multiple_spaces_collapse(self):
        assert DocumentManager.slugify("Game   Rules   2") == "game_rules_2"

    def test_leading_trailing_stripped(self):
        assert DocumentManager.slugify("  Hello World  ") == "hello_world"

    def test_empty_string(self):
        assert DocumentManager.slugify("") == ""

    def test_only_special_chars(self):
        assert DocumentManager.slugify("!!!") == ""

    def test_unicode_stripped(self):
        assert DocumentManager.slugify("Café Rules") == "cafe_rules"

    def test_numbers_preserved(self):
        assert DocumentManager.slugify("Chapter 3") == "chapter_3"


# ------------------------------------------------------------------
# delete_category
# ------------------------------------------------------------------


class TestDeleteCategory:
    def test_delete_existing_category(self, manager, docs_dir):
        manager.load()
        manager.create_category("news", "News", "en")
        result = manager.delete_category("news")
        assert result is True
        cats = manager.get_categories("en")
        assert not any(c["slug"] == "news" for c in cats)

    def test_delete_nonexistent_category(self, manager):
        manager.load()
        assert manager.delete_category("nope") is False

    def test_delete_category_removes_from_documents(self, manager, docs_dir):
        manager.load()
        manager.create_category("rules", "Rules", "en")
        manager.create_document("doc1", ["rules"], "en", "Doc", "content")
        manager.delete_category("rules")
        meta = manager.get_document_metadata("doc1")
        assert "rules" not in meta["categories"]

    def test_delete_category_persists(self, manager, docs_dir):
        manager.load()
        manager.create_category("temp", "Temp", "en")
        manager.delete_category("temp")
        # Reload from disk
        manager2 = DocumentManager(docs_dir)
        manager2.load()
        cats = manager2.get_categories("en")
        assert not any(c["slug"] == "temp" for c in cats)


# ------------------------------------------------------------------
# rename_category
# ------------------------------------------------------------------


class TestRenameCategory:
    def test_rename_category(self, manager, docs_dir):
        manager.load()
        manager.create_category("faq", "FAQ", "en")
        result = manager.rename_category("faq", "Frequently Asked Questions", "en")
        assert result is True
        cats = manager.get_categories("en")
        faq = next(c for c in cats if c["slug"] == "faq")
        assert faq["name"] == "Frequently Asked Questions"

    def test_rename_adds_locale(self, manager, docs_dir):
        manager.load()
        manager.create_category("news", "News", "en")
        manager.rename_category("news", "Noticias", "es")
        cats = manager.get_categories("es")
        news = next(c for c in cats if c["slug"] == "news")
        assert news["name"] == "Noticias"

    def test_rename_nonexistent(self, manager):
        manager.load()
        assert manager.rename_category("nope", "Name", "en") is False


# ------------------------------------------------------------------
# set_category_sort / get_category_sort
# ------------------------------------------------------------------


class TestCategorySort:
    def test_default_sort(self, manager, docs_dir):
        manager.load()
        manager.create_category("rules", "Rules", "en")
        assert manager.get_category_sort("rules") == "alphabetical"

    def test_set_sort_method(self, manager, docs_dir):
        manager.load()
        manager.create_category("rules", "Rules", "en")
        result = manager.set_category_sort("rules", "date_modified")
        assert result is True
        assert manager.get_category_sort("rules") == "date_modified"

    def test_set_sort_nonexistent(self, manager):
        manager.load()
        assert manager.set_category_sort("nope", "alphabetical") is False

    def test_get_sort_nonexistent_returns_default(self, manager):
        manager.load()
        assert manager.get_category_sort("nope") == "alphabetical"

    def test_sort_by_date_created(self, manager, docs_dir):
        manager.load()
        manager.create_category("rules", "Rules", "en")
        manager.set_category_sort("rules", "date_created")
        manager.create_document(
            "old_doc", ["rules"], "en", "Old Doc", "old",
        )
        # Manually set timestamps to control ordering
        meta = manager.get_document_metadata("old_doc")
        meta["locales"]["en"]["created"] = "2026-01-01T00:00:00Z"
        manager.create_document(
            "new_doc", ["rules"], "en", "New Doc", "new",
        )
        meta2 = manager.get_document_metadata("new_doc")
        meta2["locales"]["en"]["created"] = "2026-06-01T00:00:00Z"

        docs = manager.get_documents_in_category("rules", "en")
        # date_created sorts newest first
        assert docs[0]["folder_name"] == "new_doc"
        assert docs[1]["folder_name"] == "old_doc"
