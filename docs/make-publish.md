# Make publish scenario (thin glue — no logic lives in Make)

Purpose: approved canonical content merged to `main` → WordPress, automatically,
with an audit record. The repo side is already built (`publish-notify.yml` +
`engine/scripts/publish_notify.py`). Build the Make side once:

## Scenario (3 modules)

1. **Webhooks → Custom webhook.** Create it, copy the URL, save it in the repo as
   Actions secret `MAKE_PUBLISH_WEBHOOK_URL`. Payload received per page:
   `project_id, project_name, domain, page_id, page_name, page_url, version,
   path, created, content_markdown, content_html`.
2. **WordPress → Create a page** (or *Update a page* keyed on slug; or a generic
   HTTP module to `POST /wp-json/wp/v2/pages` with an Application Password).
   Map: title ← `page_name`, slug ← `page_url` (strip slashes),
   content ← `content_html`, status ← `draft` first (switch to `publish` once
   trusted). Route by `domain` with a Router module if you run multiple sites
   from one repo.
3. **(Optional) GitHub → Create issue comment / add label** — or skip it: the
   workflow already comments the publish event on the page's issue; Make can add
   the `status:complete` label instead.

## Audit trail

Every publish event is commented on the page's `[PAGE] <ID>` issue automatically.
For the permanent record, append one line to `control/change-log.md` in the page's
closing PR: `YYYY-MM-DD | Publish | System | <page_id> v<N> published to <url>`.
(The log is append-only via PRs by design — spec §17 — so the workflow records on
the issue and you log it at the next merge.)

## Failure mode

If the webhook POST fails, the issue comment says so explicitly — nothing is
silently lost, and the payload is rebuildable any time:
`python engine/scripts/publish_notify.py --all`.
