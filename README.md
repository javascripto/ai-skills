# AI Skills Library

Este repositório contém um conjunto estruturado de **Skills em Markdown** para ensinar agentes de IA a executar tarefas de forma padronizada, previsível e controlada.

Cada Skill descreve:
- Objetivo claro
- Contexto de uso
- Pré-requisitos
- Passos executáveis
- Comandos
- Restrições
- Decisões arquiteturais

O objetivo é reduzir ambiguidade e impedir improvisações.

## Documentos Principais

- Índice de skills: `SKILLS.md`
- Regras globais de agentes: `AGENTS.md`
- Backlog de skills: `skills-backlog.md`

---

# 🧱 Convenções Globais

As convenções globais ficam centralizadas em `AGENTS.md`.
Use este arquivo como fonte única de verdade para regras de comportamento e restrições.

---

# 📐 Estrutura Base de uma Skill

Cada skill deve ter um `SKILL.md` com:

- Frontmatter YAML obrigatório:
  - `name`
  - `description` (o que faz + quando usar)
- Corpo em Markdown com instruções operacionais para execução da skill.

Estrutura mínima da pasta:

```text
<skill-name>/
  SKILL.md
```

Recursos opcionais (quando agregam valor):

```text
<skill-name>/
  SKILL.md
  scripts/
  references/
  templates/
```

Seções sugeridas para o corpo do `SKILL.md` (adaptar conforme o caso):

- Objetivo
- Quando usar
- Pré-requisitos
- Passos
- Comandos
- Padrões e decisões
- Restrições

Princípios de autoria:

- Ser conciso e evitar conteúdo redundante.
- Definir o grau de liberdade adequado (instrução aberta vs. sequência prescritiva).
- Usar progressive disclosure: manter o fluxo principal no `SKILL.md` e mover detalhes variantes para `references/`.


---

# 📁 Organização Atual

```text
skills/
  init-vite-react-ts/
    SKILL.md
  add-tailwind-shadcn/
    SKILL.md
  add-shadcn-darkmode-theme/
    SKILL.md
  instagram-caption-fetcher/
    SKILL.md
    agents/
    scripts/
  local-faster-whisper-transcribe/
    SKILL.md
    agents/
    scripts/
  manus-skill-creator/
    SKILL.md
    scripts/
    references/
  codex-skill-creator/
    SKILL.md
    agents/
    scripts/
    references/
    assets/
```

Cada skill deve viver em seu próprio diretório, com `SKILL.md` como ponto de entrada.

## Escolha de Skill para Criar Skills

Você pode escolher entre duas skills de criação:

- `skills/manus-skill-creator/SKILL.md`: fluxo mais amplo/original para criação de skills.
- `skills/codex-skill-creator/SKILL.md`: fluxo enxuto focado em criação/atualização de skills para Codex.

---

# 🎯 Objetivo do Sistema

Criar um conjunto modular de instruções reutilizáveis para:
- Padronizar projetos
- Automatizar criação de aplicações
- Controlar decisões técnicas
- Reduzir inconsistências

Cada nova capability deve virar uma Skill.
