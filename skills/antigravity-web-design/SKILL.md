---
name: Antigravity Web Design
description: Instruções nativas detalhadas do Antigravity para desenvolvimento web com excelência estética e design premium.
---

# Antigravity Web Design (DNA)

## Objetivo
Aplicar as diretrizes nativas (System Prompt) do agente Antigravity para garantir que qualquer aplicação web desenvolvida neste ambiente tenha uma aparência **premium**, **rica** e **impressionante**. O uso de designs básicos, genéricos ou "MVPs" visuais simplórios é considerado uma falha de entrega.

## Stack Tecnológica e Setup
1. **Core**: Use HTML para estrutura e JavaScript moderno para lógica.
2. **Estilo (CSS)**: O comportamento padrão exige o uso de **Vanilla CSS** para máxima flexibilidade e controle no design. Evite TailwindCSS a menos que explicitamente solicitado pelo usuário (neste caso, confirme a versão desejada).
3. **Web App Avançado**: Se o usuário pedir explicitamente um web app complexo, use frameworks modernos como React/Vite ou Next.js. O padrão da casa do repositório dita (via `AGENTS.md`) React + TypeScript + Vite.
4. **Criação de Novo Projeto**: 
   - Ao criar projetos via CLI (`npx`), use `npx -y` para aprovar prompts automáticos.
   - Instale no diretório atual `./` se apropriado.
   - Rode sempre em modo não-interativo para o agente não travar aguardando inputs no shell. 
   - Consulte o comando com `--help` antes se não tiver certeza das flags exatas para evitar erros no terminal.
5. **Ambiente Local e Build**: Use `npm run dev` para desenvolvimento/verificação. Só faça build de produção (`npm run build`) se for explicitamente solicitado ou parte essencial da validação.

## Estética de Design (Regras Críticas)
A excelência estética é inegociável. A interface web deve causar sensação de estado-da-arte e impressionar o usuário (Efeito "WOW").

1. **Estética Rica**:
   - Substitua paletas padrões sem graça (vermelho puro, azul padrão) por cores selecionadas no formato HSL, criando harmonias elegantes.
   - Implemente Dark Mode de qualidade (cores de fundo como `#0a0a0a` ou derivados em substituição ao preto absoluto e textos legíveis).
   - Use técnicas modernas como *Glassmorphism* (desfoque de fundo) para modais, overlays e navegações flutuantes.

2. **Tipografia Premium**:
   - Nunca confie no `sans-serif` default do browser (Arial, Times, etc).
   - Integre Google Fonts modernas como **Inter, Roboto, Outfit** ou equivalentes para entregar clareza e elegância na leitura.

3. **Motion e Dynamism (Design Vivo)**:
   - A interface deve responder ativamente. Tudo que for clicável deve ter um estado de *hover* e estado `.active`/`focus`.
   - Adicione **micro-animações** vitais em botões, aberturas de janelas e carregamentos (transições suaves como `transition: all 0.3s ease`).

4. **Uso de Imagens Reais (Sem Placeholders)**:
   - Evite `divs` cinzas dizendo "Placeholder". Se for necessário provar o conceito de uma vitrine de imagens ou galeria, utilize a ferramenta `generate_image` (se disponível no ambiente) para criar assets ricos que encham a tela com sentido.

## Fluxo de Trabalho e Implementação Estruturada
Siga sempre este roteiro metódico ao erguer as bases:
1. **Compreensão e Referência**: Absorva os requisitos e pense no conceito principal e paleta de cores antes de escrever qualquer CSS.
2. **Fundação Visual (`index.css` global)**: Comece pelos tokens globais de cores, fontes, margens e utilitários.
3. **Desenvolvimento de Componentes**: Isole cada estrutura visual. Cumpra rigorosamente o design system idealizado na etapa anterior (evite inline styles e "puxadinhos").
4. **Composição da Página**: Aplique grids/flexbox sofisticados e garanta que seja **100% responsivo** em telas menores, sem quebras horizontais.
5. **Quality Assurance e Polimento**: Verifique margens, contrastes e velocidade de carregamento visual.

## Práticas de SEO Implícitas
Ainda que não solicitado, inclua automaticamente best-practices estruturais:
- Crie `Title Tags` e `Meta Descriptions` ricas se escrever o HTML raiz.
- Defina uma estrutura semântica HTML5 correta (um único `<h1>`, uso inteligente de `<main>`, `<section>`).
- Adicione **IDs únicos** e descritivos em elementos interativos importantes para facilitar testes ou buscas automáticas do browser.
