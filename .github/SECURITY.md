# Security Policy

## Supported versions

This project is pre-1.0. Only the latest tag and the `main` branch receive fixes; earlier tags do not.

## Reporting a vulnerability

Report privately through GitHub: open the repository's **Security** tab and choose **Report a vulnerability**. Do not open a public issue for an unfixed vulnerability, and do not include a working exploit in the first report — describe the class of problem, the affected file, and the impact.

Expect an acknowledgement within seven days. If you get no reply, open a public issue that says only that a private report is awaiting a response, with no details.

## Scope

The repository publishes documents, JSON schemas, worked examples, and small Python and Bash tooling (`scripts/`, `tests/`, the skill's `scripts/`, and the read-only build under `docs/evaluations/evidence/`). Findings in that tooling are in scope — path traversal in the Pages build, unsafe file handling, a GitHub Actions workflow permission or unpinned-action problem, or a schema that accepts input it should reject.

Out of scope: the content of an analysis produced by the skill, the correctness of a reference hypothesis in an example case, and anything about a deployed system belonging to a third party. Those are analysis-quality questions — open a normal issue.

## Secrets

This repository holds no credentials and none of its tooling reads any. If you find something that looks like a secret in the history, report it privately as above.
