---
name: ai-template-assisted-bootstrap
description: Inicialize ou refatore um repositório para um template mínimo de desenvolvimento assistido por IA. Use ao criar ou atualizar a estrutura base com um hub central em docs/ai/AGENTS.md, ponteiros curtos na raiz para Claude, Gemini, Cursor e Copilot, contrato genérico de Makefile, tasks do VS Code e um .gitignore multi-linguagem mesclado.
---

# Bootstrap de Template Assistido por IA

## Workflow

1. Leia referencia de [README.md](references/repo/README.md) para entender a estrutura do template.
2. Leia a seção **Conteúdo dos arquivos curtos** deste `SKILL.md` antes de escrever os arquivos de entrada da raiz.
3. Leia referências de [Makefile](references/repo/Makefile), [.vscode/tasks.json](references/repo/.vscode/tasks.json) e [.codex/environments/environment.toml](references/repo/.codex/environments/environment.toml) como contratos explícitos do template e preserve seus alvos e ações atuais (`build`, `stop`, `run`, `debug`, `clean`, `test`, `github-release` e `tree`).
4. Leia referencia de [skills/README.md](references/repo/skills/README.md) para manter a pasta de skills reservada mesmo quando vazia.
5. Leia referencia de [tree-structure.md](references/tree-structure.md) para validar a estrutura mínima esperada.
6. Leia referencia de [.gitignore](references/repo/.gitignore) antes de mesclar ou podar o `.gitignore`.
7. Mantenha o template mínimo. Crie apenas os arquivos que o repositório alvo realmente vai usar.

## Output Shape

- Crie `docs/ai/AGENTS.md` como hub canônico.
- Crie sempre `AGENTS.md`, `CLAUDE.md` e `GEMINI.md` na raiz, salvo se o uso da skill explicitar que eles não devem ser criados.
- Crie `.cursor/rules/template.mdc` e `.github/copilot-instructions.md`.
- Crie `.vscode/tasks.json` alinhado ao Makefile.
- Crie `.codex/environments/environment.toml` com ações curtas para `build`, `stop`, `run`, `debug` e `test`.
- Trate `Makefile`, `.codex/environments/environment.toml` e `.vscode/tasks.json` como contratos explícitos do template: se o arquivo não existir, crie-o com a referência; se já existir, faça merge sem quebrar o contrato do projeto.
- Crie `Makefile` com os alvos `build`, `stop`, `run`, `debug`, `clean`, `test`, `github-release` e `tree`.
- Crie ou mescle `.gitignore` usando as seções de linguagem necessárias no repositório alvo.
- Crie `skills/README.md` para reservar a pasta de skills do projeto, mesmo quando não houver skills locais.
- Crie `README.pt-BR.md` somente quando documentação bilíngue for solicitada.

<details>
<summary>Conteúdo dos arquivos curtos</summary>

### AGENTS.md

```md
# AGENTS.md

Este arquivo é um ponteiro curto para a documentação central do repositório.

Leia a versão completa em [docs/ai/AGENTS.md](docs/ai/AGENTS.md).
```

### CLAUDE.md

```md
@AGENTS.md

# CLAUDE.md

Este arquivo é um ponteiro curto para a documentação central de agentes.

Leia a versão completa em [docs/ai/AGENTS.md](docs/ai/AGENTS.md).
```

### GEMINI.md

```md
@AGENTS.md

# GEMINI.md

Este arquivo é um ponteiro curto para o contexto do template.

Leia a versão completa em [docs/ai/AGENTS.md](docs/ai/AGENTS.md).
```

### .github/copilot-instructions.md

```md
# GitHub Copilot Instructions

This file is a short entrypoint for GitHub Copilot in this repository.

Read the canonical agent guide in [docs/ai/AGENTS.md](../docs/ai/AGENTS.md).
```

### .cursor/rules/template.mdc

```md
---
description: Repository rules for the AI-assisted template
globs:
  - "**/*"
alwaysApply: true
---

Read the canonical agent guide in [docs/ai/AGENTS.md](../../docs/ai/AGENTS.md).
```

</details>

## Guardrails

- Não crie docs redundantes nem índices extras.
- Mantenha `docs/ai/AGENTS.md` como a fonte única de comportamento dos agentes.
- Mantenha os arquivos da raiz como ponteiros curtos.
- Atualize arquivos existentes em vez de duplicá-los ou substituí-los.
- Mescle o conteúdo do `.gitignore` quando o repositório alvo já tiver um.
- Preserve o contrato atual do Makefile do template quando ele existir no repositório alvo: `build`, `stop`, `run`, `debug`, `clean`, `test`, `github-release` e `tree`.
- Na pasta `.vscode`, crie apenas os arquivos que o repositório alvo já usa; neste template-base, o arquivo obrigatório é `tasks.json`.
- Mantenha `skills/README.md` como reserva explícita da pasta de skills do template.
- Ao gerar qualquer arquivo de referência do template, use o conteúdo de referência quando o arquivo não existir e faça merge quando ele já existir.
