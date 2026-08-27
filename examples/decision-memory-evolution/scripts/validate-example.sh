#!/usr/bin/env bash
set -euo pipefail

example_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
repo_dir="$(cd "$example_dir/../.." && pwd)"

uvx check-jsonschema --check-metaschema "$example_dir/artifacts/decision-episode.schema.json"
uvx check-jsonschema --check-metaschema "$example_dir/artifacts/decision-episodes.schema.json"
uvx check-jsonschema --schemafile "$repo_dir/schemas/fde-scenario.schema.json" "$example_dir/scenario.json"
uvx check-jsonschema \
  --base-uri "file://$example_dir/artifacts/" \
  --schemafile "$example_dir/artifacts/decision-episodes.schema.json" \
  "$example_dir/evidence/decision-episodes.json"

jq -e '
  . as $episodes
  | length == 6
  and ([.[].episodeId] | unique | length == 3)
  and all(.[]; . as $episode | all(.evidence[]; .availableAt <= $episode.decisionAsOf))
  and all(.[] | select(.supersedesRevisionId != null);
    . as $revision
    | .revisionId != .supersedesRevisionId
    and any($episodes[];
      .revisionId == $revision.supersedesRevisionId
      and .episodeId == $revision.episodeId))
  and ([.[] | select(.supersedesRevisionId == null and .humanInterpretation.disposition == "revised")] | length == 3)
  and ([.[] | select(.supersedesRevisionId != null and any(.evidence[]; .evidenceId | endswith("-service")))] | length == 3)
  and all(.[] | select(.outcome != null);
    (.outcome.evidence | length) > 0
    and all(.outcome.evidence[];
      .availableAt >= .sourceOccurredAt
      and .accessDecisionId != ""))
' "$example_dir/evidence/decision-episodes.json" >/dev/null

echo "decision-memory-evolution validation: passed"
