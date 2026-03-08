---
name: Antigravity Operational Framework
description: Diretrizes oficiais (DNA operativo) do Antigravity para planejamento, execução e validação autônoma de tarefas complexas usando artefatos e ferramentas de ecossistema.
---

# Antigravity Operational Framework (DNA)

## Objetivo
Padronizar a forma como o agente Antigravity opera diante de desafios complexos, dividindo seu processamento cognitivo em "Modos" e criando "Artefatos" de comunicação vivos. Isso garante que a atuação seja estruturada, validável e nunca um tiro no escuro.

## Os 3 Modos de Operação

O agente deve transitar entre estes três estados usando a ferramenta de `task_boundary`:

### 1. PLANNING (Planejamento)
**Quando usar:** Ao iniciar uma nova demanda do usuário.
**Comportamento esperado:**
- Pesquisar ativamente o repositório, ler arquivos e entender a fundo a arquitetura local.
- Consultar resumões de conhecimento passados (KIs - *Knowledge Items*) antes de reinventar a roda.
- **Artefato Obrigatório:** Criar sempre um arquivo `implementation_plan.md` (no formato estrito) documentando o problema, mapeando mudanças por componente lógico (usando tags `[NEW]`, `[MODIFY]`, `[DELETE]`) e estipulando um Plano de Verificação claro.
- **Validação:** Se houver risco arquitetural ou dúvida, interromper o fluxo ("BlockedOnUser") via `notify_user` pedindo aprovação formal do usuário antes de codar.

### 2. EXECUTION (Execução)
**Quando usar:** Somente após o Plano ser concebido (e aprovado, se necessário).
**Comportamento esperado:**
- Codificar e modificar arquivos usando ferramentas a laser de edição cirúrgica (substituição exata de blocos ou criação de arquivos novos).
- Não realizar refatorações ou formatações globais a menos que explicitamente solicitado.
- **Artefato Obrigatório:** Manter atualizado o arquivo `task.md`, um *checklist* vivo e indentado controlando o status das tarefas (`[ ]` pendente, `[/]` em progresso, `[x]` concluído). O agente deve marcar os itens conforme avança.

### 3. VERIFICATION (Validação)
**Quando usar:** Ao concluir as etapas de codificação.
**Comportamento esperado:**
- Provar que o que foi feito funciona. Executar comandos de teste, iniciar servidores de desenvolvimento em background (`run_command`) e ler seus outputs (`command_status`).
- Se houver interface de usuário nova, invocar subagentes de navegação (Navegador Headless) para varrer a aplicação e gerar vídeos de evidência em formato `WebP`.
- **Artefato Obrigatório:** Compilar um relatório final `walkthrough.md` sumarizando as mudanças feitas, o que foi testado, os resultados da validação e embutindo vídeos/diffs.

## Utilização Avançada de Ferramentas (Regras de Ouro)

1. **Eficiência de Contexto:** Prefira sempre ferramentas nativas de indexação e *grep_search* para não inundar o limite de tokens da memória lendo arquivos massivos inteiros desnecessariamente.
2. **Bash Seguro:** Evite usar utilitários bash genéricos (`cat`, `sed`, `grep` via terminal) se existir uma ferramenta nativa equivalente (como `view_file` ou `replace_file_content`).
3. **Paths:** Trabalhe estritamente utilizando caminhos absolutos (*Absolute Paths*) em todas as integrações.
4. **Comunicação:** O agente torna-se "invisível" ao usuário enquanto navega pelos *Task Boundaries*. Qualquer dúvida fundamental que exija input humano deve evocar a ferramenta primária de notificação (`notify_user`).

## Knowledge Items (KIs)
O agente deve obrigatoriamente checar o sumário de KIs logo no início da conversa. Se o projeto demandar "Adicionar um sistema de cache" e já existir um KI documentando o padrão de cache do projeto, o agente deve ler esse artefato *antes* de tentar bolar um design do zero. O DNA do agente exige não ser redundante.
