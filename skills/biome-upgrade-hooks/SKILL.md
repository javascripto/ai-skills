---
name: biome-upgrade-hooks
description: "Migrar projetos JavaScript/TypeScript para Biome como substituto de ESLint e Prettier, atualizar Biome/Husky/lint-staged para versões recentes, configurar scripts npm e hooks Git (pre-commit/pre-push), e adaptar biome.json para a estrutura atual do Biome 2.4.6. Usar quando o pedido envolver padronização de lint/format com Biome, remoção de legado ESLint/Prettier, ou ajuste de validações antes de commit/push."
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

Antes de editar `biome.json` ou `biome.jsonc`, abrir obrigatoriamente a referência 2.4.6 abaixo e usá-la durante a migração:

- Config base no schema atual: [`references/biome-2.4.6.migrated.reference.json`](references/biome-2.4.6.migrated.reference.json)

Regra operacional:

- Se `biome.json` ou `biome.jsonc` não existir, criar o arquivo a partir de `references/biome-2.4.6.migrated.reference.json` e só depois adaptar exclusões, regras e exceções do projeto.
- Se a config existir, mas estiver incompleta ou sem blocos relevantes da estrutura 2.4.6, copiar a referência 2.4.6 como baseline local e fazer merge não-destrutivo das customizações do projeto em cima dela.
- Se a config atual estiver em schema antigo ou formato legado, migrar para o schema atual e usar a referência 2.4.6 como alvo estrutural final.
- Sempre abrir `references/biome-2.4.6.migrated.reference.json` antes de propor ou aplicar a config final, para garantir que a saída use a estrutura do schema 2.4.6.
- Não confiar só no `biome migrate --write`; comparar o resultado migrado com a referência 2.4.6 e ajustar manualmente quando faltarem blocos relevantes como `assist`, `files.includes`, `css.parser.tailwindDirectives` ou overrides de regras.

Fluxo recomendado para aplicar a referência:

1. Copiar `references/biome-2.4.6.migrated.reference.json` para o projeto como base de trabalho.
2. Se já houver `biome.json` ou `biome.jsonc`, portar manualmente apenas as decisões ainda válidas do projeto que não contradigam a referência.
3. Manter as preferências da referência como fonte de verdade para estilo e formatter. Se o projeto usava algo diferente antes da migração, não preservar automaticamente opções como `quoteStyle`, `jsxQuoteStyle`, `semicolons`, `trailingCommas`, `indentStyle`, `indentWidth` ou `lineWidth`.
4. Ajustar somente os trechos específicos do projeto, como paths ignorados, regras temporariamente relaxadas e integrações como Tailwind ou shadcn/ui.
5. Validar com `npx @biomejs/biome check .` antes de seguir para scripts e hooks.

Regra de precedência:

- Quando houver conflito entre preferências já existentes do projeto e a referência 2.4.6, a referência vence para opções de estilo e formatação.
- Exemplo: se a referência usa `quoteStyle: "single"` e o projeto usava aspas duplas, manter `single` na config final do Biome.
- Preservar do projeto apenas o que for contextual, como exclusões de arquivos, integrações necessárias, relaxamentos temporários de regras e exceções deliberadas do time.

Exemplo de bootstrap quando o projeto ainda não tiver config:

```bash
cp path/to/references/biome-2.4.6.migrated.reference.json biome.json
```

Se existir config antiga, migrar automaticamente:

```bash
npx @biomejs/biome migrate --write
```

Depois validar:

```bash
npx @biomejs/biome check .
```

Checklist mínimo pós-migração com base na referência 2.4.6:

- conferir `$schema` do Biome 2.4.6
- conferir presença e estrutura de `assist.actions.source.organizeImports`
- conferir `files.includes` e exclusões comuns do projeto
- conferir `formatter`, `javascript.formatter`, `json.formatter` e `css.formatter`, preservando os valores da referência para estilo
- conferir `css.parser.tailwindDirectives` quando houver Tailwind v4
- conferir regras customizadas em `linter.rules`

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

- Ler obrigatoriamente [`references/biome-2.4.6.migrated.reference.json`](references/biome-2.4.6.migrated.reference.json) sempre que tocar em `biome.json` ou `biome.jsonc`; ela é a base da estrutura final esperada no schema 2.4.6.
- Copiar essa referência para o projeto quando a config estiver ausente ou incompleta; depois fazer merge não-destrutivo das necessidades locais, em vez de tentar reconstruir a estrutura 2.4.6 manualmente do zero.
- Em conflitos de estilo e formatter, seguir a referência e não o legado do projeto.
- Copiar os snippets de [`references/hooks-reference.md`](references/hooks-reference.md) para `.husky/pre-commit` e `.husky/pre-push`.
