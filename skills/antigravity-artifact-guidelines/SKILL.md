---
name: Antigravity Artifact Guidelines
description: Diretrizes oficiais para criação contínua de respostas visuais de Markdown rico usando carrosséis, diffs e alertas estilizados no fluxo de Chat do agente.
---

# Antigravity Artifact Guidelines (DNA)

## Objetivo
Potencializar a interface conversacional. Ao apresentar análises, comparativos de código, documentações em `task.md` ou explicações técnicas, o agente Antigravity não deve despejar texto cru, mas utilizar todo o espectro do **Markdown Rico (GFM tunings)** ativadas nativamente em seu front-end.

## Regras de Formatação Obrigatórias no Chat e Artefatos

1. **GitHub-Style Alerts:**
   Sempre estruture "Avisos" e "Dicas" críticas usando as chamadas estilizadas. Nunca aninhe ou coloque chamadas consecutivas:
   - `> [!NOTE]` para contextos de fundo.
   - `> [!TIP]` para dicas de performance/eficiência.
   - `> [!IMPORTANT]` para exigências críticas no código (ex: senhas, segredos vazados).
   - `> [!WARNING]` para quebras de compatibilidade (breaking changes).
   - `> [!CAUTION]` para riscos de perda de dado de banco.

2. **Carrosséis (Carousels) de Informação:**
   Apresente logs extensos ou *"Antes e Depois"* de telas/códigos de maneira colapsada usando nossa tag nativa de `carousel`.
   Isso permite que o usuário desfile por "slides" na própria tela de chat.
   **Sintaxe requerida**: 4 `backticks` e os separadores `<!-- slide -->`.
   *(Consulte o arquivo em `examples/carousel-demo.md` desta skill para o gabarito estrutural).*

3. **Mermaid Diagrams:**
   Se a arquitetura de banco de dados ou a hierarquia de componentes Frontend (`shadcn`, fluxos React) se tornar difícil de explicar, crie um **Diagrama Mermaid** num bloco delineado (` ```mermaid `) para representar a lógica graficamente. (Não use tags HTML dentro de rótulos Mermaid).

4. **Tratamento de Arquivos Locais (Absolute Paths e Diff Renders):**
   - Todos os arquivos lidados ou criados devem ser sempre linkados na resposta usando caminhos absolutos (*Absolute Paths*). Formato: `[utils.py](file:///path/to/utils.py)`
   - Se modificou código dentro de um artefato vivo com muitas linhas, nunca cole blocos longos de `diffs` copiados do terminal. Apresente toda a diferença das edições daquela _Task_ usando nosso renderizador nativo colocando a instrução `render_diffs(file:///path/absoluto)` numa linha limpa. O Chat fará o parser visual para o usuário.

5. **Exibição de Media (Provas Visuais - _Walkthroughs_):**
   A validação via WebP gravada ou Screenshot tirada obrigatoriamente tem que ser "embutida" como Media (imagem não clicável, renderizada na tela). Formato exigido: `![Caption Curto com Descrição do Vídeo/Imagem](/absolute/path/to/media.webp)`.
