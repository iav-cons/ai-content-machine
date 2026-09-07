#!/bin/sh
# Create the workflow labels (spec §8, §11, §13). Requires GitHub CLI: gh auth login
# Usage: sh engine/scripts/labels.sh <owner/repo>
REPO="$1"
[ -z "$REPO" ] && { echo "usage: sh engine/scripts/labels.sh <owner/repo>"; exit 1; }
for L in not_started researching research_complete brief_pending brief_qc awaiting_approval approved drafting draft_qc revision complete; do
  gh label create "status:$L" --repo "$REPO" --color 0e8a16 --force
done
gh label create "awaiting_manual_worker" --repo "$REPO" --color d93f0b --force   # spec §11
gh label create "human_review_required"  --repo "$REPO" --color b60205 --force   # spec §13
gh label create "needs-qualitative-qc"   --repo "$REPO" --color 1d76db --force   # spec §12
gh label create "phase1"                 --repo "$REPO" --color 5319e7 --force
echo "Labels created on $REPO"
