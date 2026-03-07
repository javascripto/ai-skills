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

## Inventário de Skills

Para lista de skills ativas, status e categorias, use somente `SKILLS.md`.
O `README.md` descreve convenções e objetivos gerais, sem replicar o inventário.

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
