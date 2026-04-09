# AGENTS.md

Este repositório é um template genérico para desenvolvimento assistido por IA.

## Objetivo

Manter o projeto simples, configurável e fácil de reutilizar como base.

## Regras de trabalho

- Sempre leia `README.md` ou `README.pt-BR.md` e `docs/ai/AGENTS.md` antes de editar.
- Preserve mudanças do usuário e não reverta arquivos sem pedir.
- Use `apply_patch` para alterações manuais.
- Prefira comandos não destrutivos.
- Prefira links Markdown relativos.
- Ignore `.env` e `.env.*` quando eles não fizerem parte da tarefa.
- Antes de executar qualquer fluxo que rode o projeto, rode `make stop`.
- Consulte o `Makefile` e `make help` para descobrir os comandos disponíveis.
- Depois de mudanças de workflow ou execução, valide o `make`.

## Convenções

- Mantenha o template genérico e independente de linguagem.
- Se o trabalho envolver documentação, mantenha o texto curto e prático.
- Se algo depender de processo em execução, pare a instância anterior antes de iniciar outra.

## Ferramentas

### Claude

- Use [CLAUDE.md](../../CLAUDE.md) como ponteiro curto.
- Mantenha o arquivo curto e alinhado com este guia central.

### Gemini

- Use [GEMINI.md](../../GEMINI.md) como ponteiro curto.
- Mantenha o arquivo curto e alinhado com este guia central.

### GitHub Copilot

- Use [`.github/copilot-instructions.md`](../../.github/copilot-instructions.md) como entrada curta do repositório.

### Cursor

- Use [`.cursor/rules/template.mdc`](../../.cursor/rules/template.mdc) como regra curta do Cursor neste repositório.
- Mantenha as rules alinhadas com este guia central.

## Estado do projeto

- Não há código de implementação no template ainda.
- O repositório guarda a estrutura de documentação e ferramentas para servir como template.

## Skills

- As skills locais do projeto vivem em [skills/README.md](../../skills/README.md).
- Quando houver uma skill, ela deve ficar em uma pasta própria com `SKILL.md`.

## Make

- O contrato de `make` vive no [Makefile](../../Makefile).
- O `make help` é a referência rápida para os comandos disponíveis.
