---
name: Antigravity Knowledge System
description: Estabelece as regras nativas de como o agente Antigravity deve obrigatoriamente buscar e consumir Knowledge Items (KIs) curados antes de investigar repositórios.
---

# Antigravity Knowledge System (KIs/DNA)

## Objetivo
Garantir que o agente atue com "memória de longo prazo arquitetural". Antes de executar análises exploratórias em bases de código legadas ou de desenhar novas soluções para o usuário, o agente deve recuperar, ler e integrar as decisões documentadas no passado daquele mesmo repositório, salvas na forma de Itens de Conhecimento (KIs).

## O Mecanismo de Knowledge Items (KIs)
Um **Knowledge Item (KI)** é um pacote curado e destilado de informação técnica (padrões de implementação, logs de bugs conhecidos, regras de arquitetura e schemas) gerado automaticamente por um Subagente de Conhecimento que atua assincronamente lendo as transcrições das nossas conversas passadas.

Todo KI reside em: `~/.gemini/antigravity/knowledge/`.
Ele é composto de:
1. `metadata.json`: Metadados do tópico, timestamps e ponteiros de artefatos.
2. `artifacts/`: Arquivos Markdown de documentações, diagramas ou snippets consolidados do mesmo assunto.

## A Regra de Ouro (MANDATORY FIRST STEP)
**NUNCA inicie uma pesquisa autônoma cega usando `list_dir` ou `grep_search` se a tarefa envolver arquitetura ou refatoração profunda sem antes verificar KIs.**

### Fluxo de Recuperação Obrigatório:
1. **Checagem de Sumário:** Assim que o Chat inicia, o agente recebe os sumários dos KIs globais mapeados na estrutura (`KI summaries with artifact paths`). Pare tudo e leia-os mentalmente.
2. **Match de Tópicos:** Se o usuário solicitar *"Mude o comportamento do Engine Core"* e houver um KI chamado *"Core Engine Architecture"* listado, você deve imediatamente inferir que os padrões originais estão ali.
3. **Leitura de KIs:** Utilize `view_file` para abrir e ler os `.md` do KI listados nos sumários *antes* de sair futucando os arquivos brutos do código-fonte com buscas recursivas extensas.
4. **Construção de Contexto:** Use o que foi lido no KI como "Verdade Orientadora" (Ground Truth) provisória, combinada com verificações no código ao vivo, para propor a nova solução ao usuário.

## Exemplos Práticos de Invocação de KIs
Sempre priorize a leitura de KIs nas seguintes situações:
- **Debugging:** Verificar se um bug que esvazia a memória já não foi tipificado num KI passado;
- **Follow-up Architectural:** Quando pedirem para adicionar novo componente que conecte na API, verifique o KI de "Integration Patterns";
- **Complexidade Invisível:** O que parece ser *"só adicionar um campo de tracker"* pode quebrar uma "Metadata Instrumentation" rígida já documentada em um KI. Procure e honre o Ki de infraestrutura.
