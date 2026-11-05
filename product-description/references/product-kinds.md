# Mapping the template onto a product

The document template is product-neutral. Four decisions make it concrete; make them once, before the pilot, and hold them across every document:

1. **The unit of interaction.** The smallest thing the user does with a beginning, a possibly long middle and an end, narrated in five phases: *starting*, *ending at once*, *becoming extended*, *while extended*, *finishing*.
2. **The variant axis.** What the user can hold, pass or have set that changes the outcome of the same interaction: modifier keys, flags, options, roles, settings, the state of the target. The "Modifiers" table is built on it.
3. **The interrupt list.** What can happen mid-interaction, identical and in the same order in every document, every cell filled even with "no effect". The most valuable part of the method: the same questions asked of every feature expose gaps.
4. **The cross-cutting concerns, in order.** "Interactions with other systems" walks the same list in the same order everywhere.

Write the answers into the README's "Document template" section (items 3 to 6) and define the interrupt words in the glossary's "events that end or interrupt" section.

Below are answers for four product kinds; take the nearest and adjust.

## The interrupt families

Every interrupt list draws on five families: the user's explicit abort; the user doing something else mid-way; the environment failing (focus, network, session, process); something else changing the target; the input device or channel changing. Derive the product's list from these and it will be complete.

- The **"ends at once" phase** exists everywhere (a click without drag, a form left untouched, `--help`, an empty message) and holds most "nothing happens" claims. Document it anyway; "nothing is recorded" is checkable.
- **"Commit"** is the product's durable step: an undo entry, a saved record, a file on disk, a persisted message. The finishing phase says what is committed, in how many steps, and whether it can be undone.
- **Foundations** own the numbers and the words: thresholds, timings, what "saved", "selected" or "done" means, what each interrupt word means. Other documents link to them.

## Pointer-driven editor

Canvases, design and drawing tools, diagramming, maps, timelines, node editors, grid spreadsheets. Also most native and mobile apps, with the OS lifecycle added to the interrupts.

- **Surface:** one route or window, default configuration.
- **Unit:** a gesture: *pointer down* → *up without dragging* → *becoming a drag* (distance threshold or long press) → *during the drag* → *up after dragging*.
- **Variant axis:** Shift, Alt/Option, Ctrl/Cmd, Space, plus product toggles (tool lock, pen mode). Columns: held at the start, pressed during.
- **Interrupts:** Escape; switching tools or modes; events the product treats as "complete" (a menu opening, navigation, undo or redo); events it treats as "interrupt" (a pinch beginning, another input device taking over); window loses focus; pointer leaves the window; target deleted, locked or moved by something else; touch cancel; product modes that change what follows the gesture. Mobile adds: app backgrounded, rotation, incoming call or notification, low memory.
- **Cross-cutting:** containers, groups, locked or hidden objects, clipping, readonly, history, zoom, coarse pointer, stylus, collaboration.
- **Foundations:** the input model (thresholds, click detection, modifiers, what cancels, completes and interrupts), the object model, the tool or mode model, the camera or viewport.
- **Pilot:** a small tool with a real drag (pan, lasso, ruler). **Hardest:** the selection or main editing tool: many documents that must agree on state hand-offs.
- **Verification:** devices are mouse, keyboard, touch, pen and a second user. A console handle on the app sets up scenes and reads state back; it never stands in for gesturing.

## Form-and-page web app

CRUD apps, dashboards, settings, checkout, admin panels, content management.

- **Surface:** one named role's view of production or staging, fresh account, default settings. A second role is usually a second repo or a cross-cutting document.
- **Unit:** a page or form lifecycle: *arrive* (route, what loads, focus, prefill) → *leave untouched* (back, close, link out; is anything recorded?) → *begin editing* (what becomes dirty, what validates, what enables) → *while editing* (live validation, autosave, dependent fields, the URL) → *submit* (what is sent, what is optimistic, what is disabled, success and failure paths, where the user lands).
- **Variant axis:** role or plan; record state (draft, published, archived, locked by someone else); default-on flags; keys the form honours (Enter, Cmd+Enter, Escape, Tab order). Columns: at arrival, during editing.
- **Interrupts:** Escape; browser back or forward; reload; tab or window closed; in-app link away; network lost mid-request; request times out or errors; session expires; record changed in another tab; record changed by another user; autofill or a password manager writes in; window loses focus.
- **Cross-cutting:** permissions and roles, validation and error display, unsaved changes, undo, optimistic updates and rollback, offline, notifications and toasts, search and filter state in the URL, localization, accessibility, side effects the user can notice (emails, webhooks).
- **Foundations:** the data model in user terms (what a record is, what "saved" means, what is shared), auth and roles, navigation (routes, URL state, what is restored), dirty and saved, notifications.
- **Pilot:** a small form with a submit and a validation rule (rename dialog, profile, invite). **Hardest:** the main editor or list-detail flow, where records are created, edited and moved between states.
- **Verification:** devices are browser and viewport, role, network condition, and a second account in a second browser. Use the environment and permitted actions recorded in Phase 0; a throwaway production account does not authorize emails, payments, invites, publishing or shared-data changes. Devtools' network tab shows what a submit sent, the application tab what was stored.

## Command-line tool

CLIs, build tools, package managers, database and deploy tools.

- **Surface:** one binary at one version, default configuration, no rc file, a named shell (POSIX unless Windows-first), a TTY unless the document says otherwise.
- **Unit:** an invocation: *invoke* (parsing, what is validated before anything runs, first output, prompts) → *exits immediately* (help, version, validation error: exit code, stderr or stdout) → *begins running* (first side effect, first progress, when Ctrl+C becomes unsafe) → *while running* (progress, streaming, what is written when, idempotence) → *finishes* (final output, exit code, what is on disk, failure versus success output).
- **Variant axis:** flags, environment variables, config keys, stdout and stdin TTY or pipe, `--json` and other machine modes, `--dry-run`, verbosity. Columns: changes what happens, changes what is printed.
- **Interrupts:** Ctrl+C once and twice; SIGTERM; terminal closed (SIGHUP); stdin closed or stdout pipe closed (SIGPIPE); network lost mid-run; disk full or file locked; a required file changed during the run; two instances at once; process killed outright (what state is left on disk).
- **Cross-cutting:** config precedence (flag, env, file, default), output modes (TTY, piped, `--json`, `--quiet`), colour and unicode, exit codes, logging, locking and concurrency, caching, network and proxies, permissions and sudo, shell completion, update or version checks.
- **Foundations:** invocation (parsing, subcommands, help), configuration, output (streams, TTY detection, exit codes), state on disk (what the tool owns, lockfiles, caches), what "done" and "safe to interrupt" mean.
- **Pilot:** a leaf subcommand with a side effect and a flag (`init`, `add`, `rename`). **Hardest:** the subcommand with the most work and states (`build`, `deploy`, `sync`, `install`), usually one document per phase of its run.
- **Verification:** devices are OS, shell, TTY or pipe, and network. Most items are commands with expected output and exit code, so a pass can be a script (say so in `verification/README.md`); watch TTY-only items (progress bars, prompts, colour) by hand.

## Chat, agent and messaging products

LLM assistants, chat apps, support inboxes: a message and a response that may be long, streamed and interruptible.

- **Surface:** one client (web, desktop or mobile), one plan or role, default model and settings, a fresh account.
- **Unit:** a turn: *compose* (what input accepts, attachments, slash commands, mentions, draft persistence, Enter versus Shift+Enter) → *answered immediately* (empty input, a local command, a validation error) → *response begins* (what shows while waiting, when the message joins history, what is still editable) → *while streaming* (live updates, tool calls and their display, what the user can do: scroll, type the next message, switch conversations) → *completes* (final rendering, new actions, what is persisted, the draft).
- **Variant axis:** model or mode, attachments, conversation state (new, continued, shared, archived), role or plan, rendering settings (markdown, code, reduced motion). Columns: set before sending, changed during the response.
- **Interrupts:** Stop or Escape while streaming; sending another message in flight; editing or deleting the message being answered; switching conversations; reload; tab or app closed; network lost; error or rate limit mid-stream; session expires; the conversation open on a second tab or device; a message from another participant.
- **Cross-cutting:** history and persistence, sharing and permissions, search, notifications and unread state, attachments and limits, rendering (markdown, code, images), shortcuts, offline and reconnection, multi-device sync, rate limits and quotas, accessibility.
- **Foundations:** the conversation model (conversation, message, turn, draft; what "sent" and "delivered" mean), accounts and plans, navigation (conversation list, routes, what is restored), streaming and interruption (what Stop does at each stage, what is kept).
- **Pilot:** the simplest complete turn, or one local command. **Hardest:** the composer and streaming response together, with every modifier, interrupt and attachment type.
- **Verification:** devices are client, network condition, a second device on the account, a second participant. Model responses are not deterministic: content items say "a response" and check structure, timing and state, not wording. Run on staging with a throwaway account.
