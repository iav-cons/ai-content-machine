#!/usr/bin/env bash
# One-shot repo setup, run inside a GitHub Codespace on YOUR repo.
# Does everything scriptable: installs files via one PR, first Hard QC run,
# merge, labels, branch protection. Prints the few human-only steps at the end.
set -uo pipefail
say(){ printf '\n== %s\n' "$*"; }
REPO="${GITHUB_REPOSITORY:-}"
[ -z "$REPO" ] && { echo "Run this inside a Codespace on your repo."; exit 1; }

say "1/5 Installing engine files on a setup branch"
git config user.name  >/dev/null 2>&1 || git config user.name  "setup"
git config user.email >/dev/null 2>&1 || git config user.email "setup@local"
git checkout -B setup/install
P="$(ls -d projects/*/ 2>/dev/null | head -1)"
if [ -n "$P" ] && [ -f "${P}control/project-state.md" ]; then
  echo "- setup test line (safe to remove later)" >> "${P}control/project-state.md"
else
  mkdir -p projects && echo "setup $(date -u +%F)" > projects/.setup-marker
fi
git add -A
git commit -m "Install content engine + first Hard QC run" || echo "(nothing new to commit)"
git push -u origin setup/install -f || { echo "PUSH FAILED — check Codespace permissions."; exit 1; }

say "2/5 Opening the install PR and waiting for Hard QC"
gh pr create --title "Install content engine" --body "Automated setup PR — triggers the first Hard QC run." --head setup/install --base main 2>/dev/null || echo "(PR already exists)"
gh pr checks setup/install --watch || echo "NOTE: if no checks ran, .github/workflows may be missing from this commit."

say "3/5 Merging the install PR"
gh pr merge setup/install --squash --delete-branch || gh pr merge setup/install --squash --delete-branch --admin || {
  echo "MERGE BLOCKED — open the PR in the browser, merge manually, then re-run this script; it will skip ahead."; exit 1; }
git checkout main && git pull

say "4/5 Creating labels"
sh engine/scripts/labels.sh "$REPO" || echo "Labels step had errors (safe to redo manually: Issues → Labels)."

say "5/5 Branch protection (require PR + green Hard QC)"
CHECK="$(gh api "repos/$REPO/commits/$(git rev-parse HEAD)/check-runs" --jq '.check_runs[].name' 2>/dev/null | head -1)"
CHECK="${CHECK:-hard-qc}"
echo "Using status-check name: $CHECK"
if gh api -X PUT "repos/$REPO/branches/main/protection" \
  --input - >/dev/null 2>&1 << JSON
{ "required_status_checks": { "strict": false, "contexts": ["$CHECK"] },
  "enforce_admins": false,
  "required_pull_request_reviews": { "required_approving_review_count": 0 },
  "restrictions": null }
JSON
then echo "Branch protection set: PRs required, '$CHECK' must pass."
else
  echo "Could not set protection via API. Do it in the browser (1 min):"
  echo "  Settings → Branches → Add rule → pattern: main"
  echo "  ✓ Require a pull request (leave approvals unticked)"
  echo "  ✓ Require status checks → select: $CHECK"
fi

say "DONE — remaining human-only steps"
cat << 'TXT'
1. API key:  run    gh secret set ANTHROPIC_API_KEY    then paste your key
   (from console.anthropic.com), or add it in Settings → Secrets → Actions.
2. Install the Claude GitHub App on this repo: https://github.com/apps/claude
3. Delete this Codespace when finished: https://github.com/codespaces
Then: SETUP.md → "Per page" (existing project) or "New project" (intake form).
TXT
