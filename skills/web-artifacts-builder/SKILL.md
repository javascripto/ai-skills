---
name: web-artifacts-builder
description: Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for complex artifacts requiring state management, routing, or shadcn/ui components - not for simple single-file HTML/JSX artifacts.
license: Complete terms in LICENSE.txt
---

# Web Artifacts Builder

## Objetivo
Criar artifacts HTML complexos e autocontidos para claude.ai usando React + TypeScript + Vite, com bundling final em um único arquivo.

## Quando Usar
Use esta skill quando o pedido exigir:
- múltiplos componentes e estado compartilhado
- roteamento, composição de UI e arquitetura de app frontend
- uso de Tailwind CSS e/ou shadcn/ui
- empacotamento final em um único `bundle.html`

Não use para artifacts simples que cabem em um único arquivo HTML/JSX sem estrutura de app.

## Stack
- React 18
- TypeScript
- Vite
- Parcel (bundling final)
- Tailwind CSS
- shadcn/ui

## Fluxo Padrão

1. Inicialize o projeto do artifact:
   ```bash
   bash scripts/init-artifact.sh <project-name>
   cd <project-name>
   ```
2. Desenvolva o artifact editando o código gerado.
3. Gere o arquivo final autocontido:
   ```bash
   bash scripts/bundle-artifact.sh
   ```
4. Entregue o `bundle.html` para visualização.
5. Teste visualmente apenas se necessário ou solicitado.

## Requisitos e Comportamento Esperado
- O projeto precisa conter `index.html` na raiz para o bundling funcionar.
- O bundling deve gerar `bundle.html` com JS/CSS/dependências inline.
- Evitar etapas interativas sempre que possível.
- Documentar decisões relevantes de implementação no resultado entregue ao usuário.

## Diretrizes de Design

Muito importante: evitar "AI slop".
- Evitar layouts excessivamente centralizados como padrão.
- Evitar gradientes roxos genéricos.
- Evitar cantos arredondados uniformes em todos os elementos.
- Evitar fonte Inter como default.

Buscar direção visual intencional, com identidade clara e hierarquia consistente.

## Referência
- shadcn/ui components: `https://ui.shadcn.com/docs/components`
