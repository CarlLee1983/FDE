.PHONY: test validate-scenarios validate-pages verify install-skill

UV ?= uv
AGENT ?= both

test:
	UV="$(UV)" scripts/verify.sh test

validate-scenarios:
	UV="$(UV)" scripts/verify.sh scenarios

validate-pages:
	UV="$(UV)" scripts/verify.sh pages

verify:
	UV="$(UV)" scripts/verify.sh

install-skill:
	@test -n "$(TARGET)" || { echo "TARGET is required" >&2; exit 64; }
	scripts/install-skill.sh --target "$(TARGET)" --agent "$(AGENT)"
