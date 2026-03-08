# Hook templates

## `.husky/pre-commit`

```sh
#!/usr/bin/env sh

if [ "$GITHUB_ACTIONS" = "true" ]; then
  exit 0
fi

npx lint-staged
```

## `.husky/pre-push`

```sh
#!/usr/bin/env sh

if [ "$GITHUB_ACTIONS" = "true" ]; then
  exit 0
fi

set -e

UPSTREAM="@{u}"
if ! git rev-parse --verify "$UPSTREAM" >/dev/null 2>&1; then
  # Sem upstream configurado: não bloquear o primeiro push.
  exit 0
fi

CHANGED_TSX=$(git diff --name-only --diff-filter=ACMR "$UPSTREAM"...HEAD -- '*.ts' '*.tsx')

if [ -z "$CHANGED_TSX" ]; then
  echo "No .ts/.tsx changes to validate"
  exit 0
fi

# shellcheck disable=SC2086
npx biome check --write $CHANGED_TSX
```

## `package.json` snippets

```json
{
  "scripts": {
    "prepare": "husky",
    "lint": "npx @biomejs/biome lint --write",
    "format": "npx @biomejs/biome format --write",
    "biome:check": "npx @biomejs/biome check --write"
  },
  "lint-staged": {
    "*.{js,ts,cjs,mjs,d.cts,d.mts,jsx,tsx,json,jsonc}": [
      "biome check --write"
    ]
  }
}
```
