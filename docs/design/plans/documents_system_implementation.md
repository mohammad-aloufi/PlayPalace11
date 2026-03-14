# Documents System Implementation Progress
Reference file: docs/design/plans/documents_system.md

## Architecture Rule
**No document-related code in `server/core/server.py`.** All document system
logic — menu handlers, editbox handlers, dispatch entries — must live in the
mixin modules under `server/core/documents/`:

| Module | Responsibility |
|---|---|
| `manager.py` | Data layer (`DocumentManager`): metadata, content, locks, history |
| `browsing.py` | `DocumentBrowsingMixin`: browsing menus, action menu, settings, editing flows |
| `transcriber_role.py` | `TranscriberRoleMixin`: transcriber assignment and management menus |

The Server class inherits both mixins and wires them into the central dispatch
via two hooks — **do not add individual entries to `server.py`**:

- **Menu dispatch**: `_get_document_menu_handlers(user, selection_id, state)` on `DocumentBrowsingMixin` returns a dict of all document + transcriber menu handlers. It is unpacked into the `handlers` dict inside `_dispatch_menu_selection`.
- **Editbox dispatch**: `_handle_document_editbox(user, current_menu, packet, state)` on `DocumentBrowsingMixin` is called early in `_handle_editbox` and returns `True` if handled.
- **Document editor dispatch**: `_handle_document_editor_response(user, packet, state)` on `DocumentBrowsingMixin` handles the `document_editor` packet type (a dedicated client dialog, not an editbox). Wired via a minimal `_handle_document_editor_packet` in `server.py`.

New document menus or editboxes should be added to these methods (or to `_get_transcriber_menu_handlers` for transcriber-specific menus), never directly to `server.py`.

## Completed (Sessions 1 through 3)

### Database Layer (session 1)
- `fluent_languages` column on `users` table (JSON text)
- `transcriber_assignments` table with full CRUD methods
- Migration support in `server/persistence/database.py`

### Backend Infrastructure (session 1)
- **NetworkUser.fluent_languages**: property, setter, plumbed from DB on login/reconnect (`server/core/users/network_user.py`, `server/core/server.py`)
- **Fluent languages option**: toggle menu in options, uses `show_language_menu` with on/off status labels, saves to DB (`server/core/server.py`, `server/locales/en/main.ftl`)
- **Localization.get_available_locale_codes()**: warmup-safe method that returns language codes from directory names without triggering bundle compilation (`server/messages/localization.py`)
- **DocumentManager class**: `server/core/documents/manager.py`
  - Startup loading with auto-generated metadata for existing folders
  - Category queries with locale fallback (en -> slug)
  - Document filtering by category (all / specific / uncategorized)
  - Content read on demand, write with metadata timestamp update
  - Edit locks: acquire, release, conflict detection, stale cleanup (30min timeout)
  - Version history: backup on save, 5-version cap per locale
  - Create document and create category operations
- **Server wiring**: DocumentManager initialized and loaded on startup
- **Tests**: 29 DocumentManager tests, 4 new fluent languages tests in options menu suite
- **Locale completeness**: fixed missing .ftl files across 28 locales, added Serbian (sr)

### Document Browsing — Read-Only (session 2)
- "Documents" item in main menu for all users (approved and unapproved)
- `_show_documents_menu`: category list + "All documents" + "Uncategorized"
- `_show_documents_list`: document titles for a given category
- `_show_document_view`: read-only editbox with locale fallback to English
- Dispatch table entries for `documents_menu`, `documents_list_menu`

### Transcriber Management (session 3)
- "View transcribers by language" and "View transcribers by user" items added to documents menu
- **By language flow**: `show_language_menu` with per-language user counts → user list for selected language → admin can click to remove (with confirmation) or "Add users" to show toggle list of eligible users (filtered by fluent_languages)
- **By user flow**: transcriber list with language counts → language list for selected user → admin can click to remove (with confirmation) or "Add languages" to show toggle list of unassigned fluent languages
- Validation: only users with a language in `fluent_languages` can be assigned as transcribers
- Toggle sounds: `checkbox_list_on.wav` / `checkbox_list_off.wav` for add/remove
- Dispatch table entries: `transcribers_for_language_menu`, `transcriber_remove_confirm`, `transcribers_by_user_menu`, `transcriber_user_languages_menu`, `transcriber_remove_lang_confirm`
- 20 new locale strings in `server/locales/en/main.ftl`

### Module Refactor (session 4)
- Moved document browsing and transcriber management code out of `server/core/server.py` into mixin modules
- Module structure under `server/core/documents/`:
  - `manager.py` — data layer (DocumentManager)
  - `browsing.py` — `DocumentBrowsingMixin` (document menus, list, view)
  - `transcriber_role.py` — `TranscriberRoleMixin` (transcriber assignment/management menus)
- Server class inherits both mixins; cross-mixin calls resolve via MRO

### Document Actions (session 5)
- Action menu for transcribers/admins (View, Edit placeholder, Document settings)
- Document settings submenu with title, visibility, categories, add/remove translation, delete
- New DocumentManager data methods: get/set title, visibility, categories; add/remove translation; delete document
- Menu and editbox dispatch entries moved entirely out of `server/core/server.py` via `_get_document_menu_handlers()` and `_handle_document_editbox()` on the browsing mixin
- Transcriber menu dispatch entries also moved out via `_get_transcriber_menu_handlers()` on the transcriber role mixin

### Document Editing & Add Translation (session 6)
- **New `document_editor` packet type**: bidirectional packet for the document editor dialog (server→client opens editor, client→server sends save/cancel response)
  - `DocumentEditorPacket` (server→client): dialog_id, content, source_content, source_label, prompt
  - `DocumentEditorResponsePacket` (client→server): dialog_id, action (save/cancel), content
- **Desktop client**: `DocumentEditorDialog(wx.Dialog)` in `clients/desktop/ui/document_editor_dialog.py` — read-only source panel + editable content area + save/cancel buttons, cancel confirms if content changed
- **Web client**: `createDocumentEditor` in `clients/web/ui/document_editor.js` — `<dialog>` modal with same layout, wired in `app.js` and `index.html`
- **Edit flow**: language selection menu → acquire lock → open editor dialog → save (backup + lock release) or cancel (lock release)
- **Add translation flow**: language selection (untranslated languages filtered to assigned) → title editbox → open editor dialog → save creates translation (private by default)
- **Shared title editbox handler**: flow-aware — `change_title` saves immediately, `add_translation` stores title and opens editor for content
- **Shared helpers**: `_get_user_assigned_languages(username)`, `_get_user_accessible_locales(user, folder_name)` — consolidated locale filtering from Chunk 4
- **Server dispatch**: `_handle_document_editor_packet` in `server.py` forwards to `_handle_document_editor_response` on the browsing mixin
- 4 new locale strings: `documents-locked`, `documents-content-saved`, `documents-editor-prompt`, `documents-source-label`

### Document & Category Creation (session 7)
- **New document flow**: admin selects categories (toggle list with Done/Back) → title editbox → auto-slugify → collision check → document editor dialog → `create_document()`
- **New category flow**: slug editbox → display name editbox → `create_category()`
- **Category management** in documents list menu (for real categories):
  - Rename category (transcriber/admin): editbox with current name → `rename_category(slug, name, locale)`
  - Category settings (admin): sort method submenu (alphabetical, date created, date modified) → `set_category_sort()`
  - Delete category (admin): yes/no confirmation → `delete_category()` removes category and cleans up document associations
- **New DocumentManager methods**: `slugify()` (static), `delete_category()`, `rename_category()`, `set_category_sort()`, `get_category_sort()`
- **Updated `get_documents_in_category()`**: now respects category sort method (alphabetical/date_created/date_modified)
- **Shared title editbox handler**: extended with `"new_document"` flow — slugifies title, checks collision, opens editor
- **Shared document editor**: extended with `"new_document"` flow — no lock/metadata needed, creates document on save
- 4 new dispatch menu entries: `new_document_categories_menu`, `category_settings_menu`, `category_sort_menu`, `delete_category_confirm`
- 3 new editbox handlers: `new_category_slug_editbox`, `new_category_name_editbox`, `rename_category_editbox`
- 16 new locale strings for creation flows, slug validation, category management
- 21 new tests: slugify (9), delete_category (4), rename_category (3), category_sort (5)

---

## Chunk 4: Document Actions (Admin & Transcriber)

The action menu that appears when a transcriber or admin clicks a document.

### Scope
- Role-based behavior: normal users auto-view, transcribers/admins see action menu
- Action menu: View, Edit, Document settings
- Document settings submenu:
  - Change title (per locale)
  - Manage visibility (public/private toggles per locale)
  - Modify category list (admin, boolean toggle list)
  - ~~Add translation~~ — deferred to Chunk 5 (shares the document contents dialog for content entry)
  - Remove translation (admin, confirmation with safeguards)
  - Delete document (admin, confirmation with translation count)
- Permission checks: transcribers limited to their assigned languages
- Locale strings for all prompts and confirmations
- Tests for action menu routing and permission checks

### Files modified
- `server/core/documents/manager.py` — new data methods (get/set title, visibility, categories; add/remove translation; delete)
- `server/core/documents/browsing.py` — action menu, settings submenu, all management handlers; dispatch via `_get_document_menu_handlers` and `_handle_document_editbox`
- `server/core/documents/transcriber_role.py` — dispatch via `_get_transcriber_menu_handlers`
- `server/locales/en/main.ftl` — 24 new locale strings

---

## Chunk 5: Document Editing & Add Translation ✓

The document contents dialog — used any time document content is shown for editing (editing an existing document, adding a translation, creating a new document). Also includes the "Add translation" flow deferred from Chunk 4, since the content entry step should reuse this same dialog. Read-only viewing remains a simple editbox.

### Scope
- **Document contents dialog** (new client UI dialog — see platform notes below): multiline editbox with current content, edit locks, save/cancel
- Source reference display: if editing a non-source locale, a read-only panel shows the source content alongside the editor
- Save handler: calls `DocumentManager.save_document_content()` (handles backup + lock release)
- Cancel handler: release edit lock, return to document actions
- Escape = cancel, with confirmation if content changed
- Lock acquisition on edit open, conflict message if locked by another user
- **Add translation**: locale selection + title editbox, then open the document contents dialog for content entry
- Locale strings for editor prompts, save/cancel confirmations, lock conflict messages
- Tests for edit flow, lock integration, save with version backup

### Platform constraint: new dialog type required

The existing client UI supports only one editbox at a time (via `request_input` packets), and cannot display menus and editboxes simultaneously. This makes the side-by-side source comparison impossible with the current editbox system — it would require two text fields (one editable, one read-only) plus save/cancel controls all visible at once.

**Solution**: Introduce a new `document_editor` packet type and corresponding dialog implementation in both clients. This dedicated dialog handles all document content editing needs and provides a foundation for future editing features.

#### New packet: `document_editor`

**Server → Client** (`document_editor` packet):
- `dialog_id`: str — identifier for response routing
- `content`: str — current document content (empty string for new translations)
- `source_content`: str | None — source locale content for reference (None if editing the source locale or if source has no content)
- `source_label`: str | None — label for the source panel (e.g. "English (source)")
- `prompt`: str — accessible label/title for the editor (e.g. "Edit: Uno Rules (Spanish)")

**Client → Server** (`document_editor` packet):
- `dialog_id`: str — matches the server's dialog_id
- `action`: str — "save" or "cancel"
- `content`: str | None — the edited text (only present when action is "save")

#### Desktop client (`clients/desktop/`)

Create a new `DocumentEditorDialog(wx.Dialog)` class. Layout:
- If `source_content` is provided: a read-only multiline `wx.TextCtrl` labeled with `source_label`, followed by the editable multiline `wx.TextCtrl`
- If `source_content` is None: only the editable multiline `wx.TextCtrl`
- Save and Cancel buttons at the bottom
- Dialog title set from `prompt`
- Escape key triggers cancel (with confirmation if content changed)
- The handler in `main_window.py` listens for the `document_editor` packet, opens the dialog modally, and sends the response packet

#### Web client (`clients/web/`)

Create a `<dialog>` element for the document editor. Layout:
- If `source_content` is provided: a read-only `<textarea>` labeled with `source_label`, followed by the editable `<textarea>`
- If `source_content` is None: only the editable `<textarea>`
- Save and Cancel buttons
- Escape key triggers cancel (with confirmation if content changed)
- The handler in `app.js` listens for the `document_editor` packet, opens the dialog as a modal, and sends the response packet

#### Server side

- Add `DocumentEditorPacket` to `server/network/packet_models.py`
- Add `show_document_editor(dialog_id, content, source_content, source_label, prompt)` to `NetworkUser`
- Add `_handle_document_editor_response(user, packet, state)` dispatch in `browsing.py`, wired into the server dispatch (following the same pattern as `_handle_document_editbox`)

### Design notes: shared handlers and reuse

**Shared title editbox**: The title editbox handler must be a single reusable handler used by all flows that set a document title: changing an existing title, naming a new translation, and naming a new document. Do not duplicate the title prompt/save logic across these flows.

**Shared document contents dialog**: The document contents dialog (the new `document_editor` dialog described above) must be a single reusable flow on the server. Callers: edit existing document, add translation (after title entry), create new document (Chunk 6). Each caller passes context (folder_name, locale, whether it's a new translation/document) and the dialog handles save uniformly.

**Shared locale picker for document operations**: Change title, manage visibility, remove translation, and add translation all need to show the document's locales filtered by the user's assigned transcriber languages. This should be a single helper (e.g. `_get_user_accessible_locales(user, folder_name)`) rather than repeating the filter logic in each handler. Note: Chunk 4's implementation currently repeats this filter — consolidate when implementing Chunk 5.

**Shared category toggle list**: Chunk 4's "modify categories" and Chunk 6's "new document category selection" both present a toggle list of categories. Reuse the same display/toggle handler for both.

### Files to modify
- `server/network/packet_models.py` — new `DocumentEditorPacket` model
- `server/core/users/network_user.py` — new `show_document_editor()` method
- `server/core/documents/browsing.py` — editor handlers, document_editor response dispatch; add new entries to `_handle_document_editbox` and new `_handle_document_editor_response`
- `server/core/server.py` — wire `document_editor` response packets to the browsing mixin dispatch (minimal: call `_handle_document_editor_response`)
- `clients/desktop/ui/document_editor_dialog.py` — new `DocumentEditorDialog` class
- `clients/desktop/ui/main_window.py` — handler for `document_editor` packet
- `clients/web/app.js` — handler for `document_editor` packet
- `clients/web/ui/document_editor.js` — new document editor dialog module
- `clients/web/index.html` — new `<dialog>` element for the editor
- `server/locales/en/main.ftl` — locale strings
- **Not** `server/core/server.py` for document logic — see Architecture Rule above (only the packet dispatch wire goes there)

---

## Chunk 6: Document & Category Creation ✓

Admin flows for creating new documents and categories.

### Scope
- New document flow: category selection (reuse shared category toggle list) -> title editbox (reuse shared title handler) -> document contents dialog (reuse shared contents dialog) -> auto-generate folder slug from title
- Slug collision detection with user-friendly error
- New category flow: slug editbox -> display name editbox
- Category management: rename (per locale), change sort method, delete (with document cleanup)
- Locale strings for creation flows
- Tests for creation flows and edge cases (duplicate slugs, empty input)
- See Chunk 5 design notes for all shared handlers that must be reused here

### Files modified
- `server/core/documents/browsing.py` — creation handlers, category management handlers; new menu/editbox entries in `_get_document_menu_handlers` and `_handle_document_editbox`
- `server/core/documents/manager.py` — `slugify()`, `delete_category()`, `rename_category()`, `set_category_sort()`, `get_category_sort()`; updated `get_documents_in_category()` with sort support
- `server/locales/en/main.ftl` — 16 new locale strings
- `server/tests/test_document_manager.py` — 21 new tests
- **Not** `server/core/server.py` — see Architecture Rule above
