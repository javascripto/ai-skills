---
name: send-mail-authorized
description: Ensina agentes de IA a enviar emails para você mesmo ou para destinatários explicitamente autorizados usando o comando `send-mail` disponível no sistema. Use quando o usuário pedir para redigir, revisar ou enviar email com `send-mail`, inclusive com corpo via stdin, HTML, Markdown, histórico e modos JSON/silent.
---

# Send Mail Authorized

Use esta skill quando o usuário quiser que o agente envie um email com o comando `send-mail`.

Esta skill é restrita a dois casos:
- envio para o próprio usuário
- envio para terceiros que o usuário autorizou explicitamente na conversa

Se a autorização para terceiros não estiver clara, pare e peça confirmação curta antes de enviar.

## Ferramenta

- Preferência: use o comando `send-mail` já configurado no sistema.
- Script de referência: `scripts/send_mail.py`
- Completion de referência: `scripts/_send-mail`

## Preferência de uso

- Sempre prefira o `send-mail` disponível no terminal do sistema.
- Use `scripts/send_mail.py` apenas como referência de implementação, fallback local ou para manutenção da skill.
- Se houver diferença entre o script da skill e o comando instalado no sistema, siga o comportamento do comando do sistema para executar o envio.

## Fluxo recomendado

1. Confirme mentalmente quem é o destinatário.
2. Se for o próprio usuário, pode prosseguir.
3. Se for outra pessoa, verifique se houve permissão explícita nesta conversa.
4. Redija um assunto claro e uma mensagem objetiva.
5. Use `send-mail --subject ... --message ...` para mensagens curtas.
6. Use `--message -` com stdin quando o corpo for longo, multilinha ou tiver aspas que compliquem escaping.
7. Use `--html` para HTML direto e `--markdown` quando quiser converter Markdown simples para HTML antes do envio.
8. Depois do envio, relate de forma breve para quem foi enviado e qual foi o assunto.

## Comandos úteis

Mensagem curta:

```bash
send-mail --subject "Quick update" --message "The task is complete."
```

Enviar para si mesmo:

```bash
send-mail --subject "Note to self" --message "Remember to review the draft."
```

Enviar para terceiro autorizado:

```bash
send-mail --to "person@example.com" --subject "Status update" --message "Sharing the latest status as requested."
```

Corpo longo por stdin:

```bash
cat message.txt | send-mail --to "person@example.com" --subject "Weekly summary" --message -
```

Saída estruturada:

```bash
send-mail --to "person@example.com" --subject "Status" --message "Done." --json
```

HTML direto:

```bash
send-mail --subject "Styled update" --message "<strong>Hello</strong>" --html
```

Markdown convertido para HTML:

```bash
cat summary.md | send-mail --subject "Weekly summary" --message - --markdown
```

Sem imprimir saída:

```bash
send-mail --to "person@example.com" --subject "Status" --message "Done." --silent
```

## Quando usar stdin

Prefira `--message -` quando:
- o email tiver múltiplos parágrafos
- o texto vier de arquivo ou de outro comando
- houver aspas, markdown ou caracteres especiais que dificultem escaping

Exemplo:

```bash
cat <<'EOF' | send-mail --subject "Project recap" --message -
Hello,

Here is the latest project recap.

Best,
Yuri
EOF
```

## Histórico e inspeção

Ver histórico:

```bash
send-mail --show-history
```

Ver uma mensagem específica:

```bash
send-mail --show-message 1
```

## Regras operacionais

- Não envie email para terceiros sem permissão explícita do usuário.
- Não invente destinatários. Se faltar o email, peça o endereço.
- Se o usuário pedir apenas rascunho, escreva o conteúdo mas não execute `send-mail`.
- Se o conteúdo for sensível, confirme destinatário e assunto antes do envio quando houver risco de erro.
- Prefira mensagens objetivas e em inglês no corpo técnico, salvo se o usuário pedir outro idioma.

## Gatilhos comuns

Esta skill deve ativar para pedidos como:
- "mande um email para mim"
- "envie isso por email"
- "use send-mail"
- "redija e envie um email para fulano"
- "mande um resumo para mim mesmo"
- "mostre o histórico do send-mail"
