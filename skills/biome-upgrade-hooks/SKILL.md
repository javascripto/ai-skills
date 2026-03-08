---
name: biome-upgrade-hooks
description: "Migrar projetos JavaScript/TypeScript para Biome como substituto de ESLint e Prettier, atualizar Biome/Husky/lint-staged para versões recentes, configurar scripts npm e hooks Git (pre-commit/pre-push), e adaptar biome.json de versões antigas (ex.: 1.9.3) para a versão atual. Usar quando o pedido envolver padronização de lint/format com Biome, remoção de legado ESLint/Prettier, ou ajuste de validações antes de commit/push."
---

# Biome Upgrade Hooks

## Overview

Padronizar projetos para usar Biome como ferramenta única de lint/format/check, com Husky + lint-staged e hooks Git consistentes para commit e push.

## Guardrails

- Não fazer commit automaticamente.
- Em projeto grande já existente, não rodar formatação em massa antes do primeiro commit da migração para Biome.
- Em projeto legado, preferir validação sem escrita no início (`npx @biomejs/biome check .`) e deixar `--write` para etapa controlada.
- Rodar validações finais e comandos potencialmente amplos somente após confirmação explícita do usuário.
- Em projetos com shadcn/ui, ignorar `src/components/ui/**/*` no Biome para não reformatar componentes gerados que seguem padrão próprio.
- Em projetos com Tailwind v4 (`@custom-variant`, `@theme`, `@apply`), habilitar `css.parser.tailwindDirectives: true`.
- Em SPA que não devem usar `lang` em `<html>` por decisão de produto/compatibilidade, desabilitar `a11y.useHtmlLang`.
- Se o time quiser permitir `return` dentro de callback de `forEach`, manter `useIterableCallbackReturn` ativo mas com `options.checkForEach: false`.
- Se o projeto quiser reduzir bloqueios em hooks React durante migração, usar `correctness.useExhaustiveDependencies: "warn"`.

## Workflow

1. Confirmar stack e estado atual
2. Atualizar dependências para versões recentes
3. Migrar e validar `biome.json`
4. Ajustar scripts e configuração do `lint-staged`
5. Atualizar hooks `pre-commit` e `pre-push`
6. Remover legado de ESLint/Prettier
7. Executar validação final

## 1) Confirmar stack e estado atual

Executar:

```bash
node -v
npm -v
npm pkg get devDependencies dependencies scripts
ls -la .husky
```

Detectar:

- presença de `@biomejs/biome`
- presença de `husky` e `lint-staged`
- presença de configs legadas (`.eslintrc*`, `eslint.config.*`, `.prettierrc*`, `prettier.config.*`, `.prettierignore`)
- presença de `biome.json` ou `biome.jsonc`

## 2) Atualizar dependências

Consultar versões recentes no momento da execução:

```bash
npm view @biomejs/biome version
npm view husky version
npm view lint-staged version
```

Atualizar:

```bash
npm install -D @biomejs/biome@latest husky@latest lint-staged@latest
```

Nota de referência histórica (apenas contexto): em 2026-03-08, versões observadas:

- `@biomejs/biome`: `2.4.6`
- `husky`: `9.1.7`
- `lint-staged`: `16.3.2`

## 3) Migrar e validar biome.json

Se existir config antiga (ex.: schema `1.9.3`), migrar automaticamente:

```bash
npx @biomejs/biome migrate --write
```

Depois validar:

```bash
npx @biomejs/biome check .
```

Usar como referência:

- Config legado base: [`references/biome-1.9.3.reference.json`](references/biome-1.9.3.reference.json)
- Config migrado para 2.4.6: [`references/biome-2.4.6.migrated.reference.json`](references/biome-2.4.6.migrated.reference.json)

Para projetos com shadcn/ui, garantir também no `files.includes`:

```json
["**", "!**/node_modules", "!dist/**/*", "!src/components/ui/**/*"]
```

Para projetos com Tailwind v4, garantir:

```json
{
  "css": {
    "parser": {
      "tailwindDirectives": true
    }
  }
}
```

Se o projeto SPA optar por não usar `lang` no `index.html`, ajustar:

```json
{
  "linter": {
    "rules": {
      "a11y": {
        "useHtmlLang": "off"
      }
    }
  }
}
```

Se quiser suprimir alertas de `forEach` retornando valor (sem desativar a regra para outros iterables), ajustar:

```json
{
  "linter": {
    "rules": {
      "suspicious": {
        "useIterableCallbackReturn": {
          "level": "error",
          "options": {
            "checkForEach": false
          }
        }
      }
    }
  }
}
```

Se quiser tratar `useExhaustiveDependencies` como aviso (sem bloquear lint):

```json
{
  "linter": {
    "rules": {
      "correctness": {
        "useExhaustiveDependencies": "warn"
      }
    }
  }
}
```

## 4) Ajustar scripts npm e lint-staged

Garantir scripts mínimos no `package.json`:

```json
{
  "scripts": {
    "prepare": "husky",
    "lint": "npx @biomejs/biome lint --write",
    "format": "npx @biomejs/biome format --write",
    "biome:check": "npx @biomejs/biome check --write"
  }
}
```

Garantir `lint-staged` com foco em JS/TS/JSON:

```json
{
  "lint-staged": {
    "*.{js,ts,cjs,mjs,d.cts,d.mts,jsx,tsx,json,jsonc}": [
      "biome check --write"
    ]
  }
}
```

## 5) Atualizar hooks Git

### pre-commit

Usar este padrão:

```sh
if [ "$GITHUB_ACTIONS" = "true" ]; then
  exit 0
fi

npx lint-staged
```

### pre-push (TS/TSX alterados desde upstream)

Não usar conceito de "staged" no pre-push. Em vez disso, validar arquivos alterados entre upstream e `HEAD`.

Fluxo recomendado:

1. Resolver branch upstream (`@{u}`)
2. Listar arquivos alterados `*.ts` e `*.tsx`
3. Se lista vazia, sair com sucesso
4. Rodar `biome check --write` apenas nesses arquivos

Template pronto em [`references/hooks-reference.md`](references/hooks-reference.md).

## 6) Remover legado ESLint/Prettier

Remover dependências antigas:

```bash
npm uninstall eslint prettier @typescript-eslint/parser @typescript-eslint/eslint-plugin eslint-config-prettier eslint-plugin-prettier
```

Remover arquivos legados quando existirem:

- `.eslintrc`
- `.eslintrc.js`
- `.eslintrc.cjs`
- `.eslintrc.json`
- `eslint.config.js`
- `eslint.config.mjs`
- `eslint.config.cjs`
- `.prettierrc`
- `.prettierrc.js`
- `.prettierrc.json`
- `prettier.config.js`
- `prettier.config.cjs`
- `.prettierignore`

## 7) Validação final

Executar somente se o usuário confirmar:

```bash
npm run lint
npm run format
npm run biome:check
git diff --name-only
```

Para projeto grande já existente, preferir primeiro:

```bash
npx @biomejs/biome check .
```

Depois, aplicar `--write` de forma gradual (por pasta, por arquivo, ou em conjunto pequeno de mudanças).

Confirmar que:

- `biome.json` está compatível com versão atual
- hooks estão executáveis
- não há referências restantes a ESLint/Prettier

## Resource Usage Notes

- Ler [`references/biome-1.9.3.reference.json`](references/biome-1.9.3.reference.json) somente para espelhar regras legadas.
- Ler [`references/biome-2.4.6.migrated.reference.json`](references/biome-2.4.6.migrated.reference.json) para ajustes pós-migração no schema novo.
- Copiar os snippets de [`references/hooks-reference.md`](references/hooks-reference.md) para `.husky/pre-commit` e `.husky/pre-push`.
