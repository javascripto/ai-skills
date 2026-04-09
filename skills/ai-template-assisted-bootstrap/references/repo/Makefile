.PHONY: help build run stop debug clean test github-release tree

TREE_IGNORE ?= .git|build|bin|.env|.env.*|*.log|*.tmp

# AI agents: future complex make-related scripts should live in scripts/make/.

help:
	@printf '%s\n' "Available targets:"
	@printf '%s\n' "  make build    Run the build step"
	@printf '%s\n' "  make stop     Run the stop step"
	@printf '%s\n' "  make run      Stop, build, and run the project"
	@printf '%s\n' "  make debug    Stop, build, and run the debug step"
	@printf '%s\n' "  make clean    Run the clean step"
	@printf '%s\n' "  make test     Run the test step"
	@printf '%s\n' "  make github-release  Run the GitHub release step"
	@printf '%s\n' "  make tree     Show the project tree and copy it to clipboard"

build:
	@printf '%s\n' "Build step not implemented yet."

stop:
	@printf '%s\n' "Stop step not implemented yet."

run: stop build
	@printf '%s\n' "Run step not implemented yet."

debug: stop build
	@printf '%s\n' "Debug step not implemented yet."

clean:
	@printf '%s\n' "Clean step not implemented yet."

test:
	@printf '%s\n' "Test step not implemented yet."

github-release:
	@printf '%s\n' "GitHub release step not implemented yet."

tree:
	@tree -C -a --dirsfirst --condense --gitignore -I '$(TREE_IGNORE)' # print
	@tree -a --dirsfirst --condense --gitignore -I '$(TREE_IGNORE)' | pbcopy # copy
