#!/usr/bin/env python3

import smtplib
import os
import sys
import webbrowser
import argparse
import re
import html
from email.message import EmailMessage
from dotenv import (
    load_dotenv,
)  # pip install dotenv --break-system-packages # instala globalmente
from platformdirs import user_data_dir
import shelve
from datetime import datetime
import json
from pathlib import Path

import signal


PROG_NAME = Path(sys.argv[0]).name or "send-mail"


# 🔐 lista de emails permitidos (via .env)
def get_allowed_recipients():
    raw = os.getenv("EMAIL_ALLOWED_RECIPIENTS", "")
    emails = [e.strip() for e in raw.split(";") if e.strip()]
    return set(emails)


ALLOWED_RECIPIENTS = get_allowed_recipients()

# 📁 diretório de dados (cross-platform)
APP_NAME = "send-email-cli"
DATA_DIR = user_data_dir(APP_NAME)
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "email_logs")
SCRIPT_DIR = Path(__file__).resolve().parent
APP_PASSWORD_URL = "https://myaccount.google.com/apppasswords"


# Handle SIGINT (Ctrl+C)
def handle_sigint(signum, frame):
    print("\nInterrompido pelo usuário (Ctrl+C)")
    sys.exit(130)  # padrão Unix para SIGINT


signal.signal(signal.SIGINT, handle_sigint)


# Helper functions for history and message retrieval
def get_history():
    with shelve.open(DB_PATH) as db:
        return db.get("logs", [])


def get_trash():
    with shelve.open(DB_PATH) as db:
        return db.get("logs_trash", [])


def get_message_by_id(message_id):
    logs = get_history()
    return next((l for l in logs if str(l["id"]) == str(message_id)), None)


def move_all_logs_to_trash():
    with shelve.open(DB_PATH) as db:
        logs = db.get("logs", [])
        trash = db.get("logs_trash", [])
        trash.extend(logs)
        db["logs_trash"] = trash
        db["logs"] = []


def move_log_to_trash(log_id):
    with shelve.open(DB_PATH) as db:
        logs = db.get("logs", [])
        trash = db.get("logs_trash", [])

        log = next((l for l in logs if str(l["id"]) == str(log_id)), None)
        if not log:
            return False

        logs = [l for l in logs if str(l["id"]) != str(log_id)]
        trash.append(log)

        db["logs"] = logs
        db["logs_trash"] = trash
        return True


def restore_log(log_id):
    with shelve.open(DB_PATH) as db:
        logs = db.get("logs", [])
        trash = db.get("logs_trash", [])

        log = next((l for l in trash if str(l["id"]) == str(log_id)), None)
        if not log:
            return False

        trash = [l for l in trash if str(l["id"]) != str(log_id)]
        logs.append(log)

        db["logs"] = logs
        db["logs_trash"] = trash
        return True


def reindex_logs():
    with shelve.open(DB_PATH) as db:
        logs = db.get("logs", [])
        for i, log in enumerate(logs, start=1):
            log["id"] = i
        db["logs"] = logs


# Display functions for history and single message
def show_history(output_json: bool):
    logs = get_history()
    if output_json:
        print(
            json.dumps(
                [{k: v for k, v in log.items() if k != "message"} for log in logs],
                indent=2,
            )
        )
    else:
        for log in logs:
            print(
                f"{log['id']} | {log['timestamp']} | {log['to']} | {log['subject']} | {'OK' if log['success'] else 'FAIL'}"
            )


def show_trash(output_json: bool):
    logs = get_trash()
    if output_json:
        print(
            json.dumps(
                [{k: v for k, v in log.items() if k != "message"} for log in logs],
                indent=2,
            )
        )
    else:
        for log in logs:
            print(
                f"{log['id']} | {log['timestamp']} | {log['to']} | {log['subject']} | {'OK' if log['success'] else 'FAIL'}"
            )


def show_message(message_id: str, output_json: bool):
    log = get_message_by_id(message_id)
    if not log:
        print("ID não encontrado")
        return

    if output_json:
        print(json.dumps(log, indent=2))
    else:
        print(log["message"])


def show_usage():
    prog = PROG_NAME
    print(
        f"""
Uso:
  {prog} --subject "Assunto" --message "Mensagem" [--to email]

Opções:
  -h, --help                Mostrar ajuda
  --subject                 Assunto do email
  --message                 Conteúdo do email (use '-' para stdin)
  --html                    Enviar mensagem como HTML
  --markdown                Converter Markdown simples para HTML e enviar
  --to                      Destinatário
  --auth                    Gerar App Password
  --silent                  Não imprime saída
  --json                    Output em JSON
  --show-history            Mostrar histórico
  --show-message            Mostrar mensagem específica por ID
  --clear-history           Apagar histórico de emails
  --delete-log-message ID   Mover log específico para lixeira
  --show-trash              Mostrar lixeira
  --restore-log ID          Restaurar log da lixeira
  --reindex                 Reindexar IDs

Exemplos:
  {prog} --subject "Teste" --message "Funcionando"
  {prog} --subject "Teste" --message "<b>Oi</b>" --html
  {prog} --subject "Teste" --message "# Titulo" --markdown
  {prog} --show-history
  {prog} --show-message 1
  {prog} --delete-log-message 1
  {prog} --clear-history
  {prog} --auth
  {prog} --subject "Teste" --message - < email.txt
  cat email.txt | {prog} --subject "Teste" --message -
"""
    )


def open_auth_flow():
    print("Abrindo página para gerar App Password...\n")
    print("1. Faça login")
    print("2. Gere uma App Password")
    print("3. Copie a senha\n")

    webbrowser.open(APP_PASSWORD_URL)

    input("Pressione ENTER depois de gerar a senha...")

    password = input("Cole sua App Password: ").strip()

    env_path = SCRIPT_DIR / ".env"

    if env_path.exists():
        # Atualiza ou adiciona EMAIL_PASS no .env
        lines = env_path.read_text().splitlines()
        updated = False

        for i, line in enumerate(lines):
            if line.startswith("EMAIL_PASS="):
                lines[i] = f'EMAIL_PASS="{password}"'
                updated = True
                break

        if not updated:
            lines.append(f'EMAIL_PASS="{password}"')

        env_path.write_text("\n".join(lines) + "\n")
        print(f"\nEMAIL_PASS salvo em {env_path}")
    else:
        print("\nArquivo .env não encontrado.")
        print("Adicione manualmente:\n")
        print(f'EMAIL_PASS="{password}"')


def validate_recipient(to_email: str):
    if to_email not in ALLOWED_RECIPIENTS:
        print(f"Erro: destinatário '{to_email}' não permitido")
        sys.exit(1)


def markdown_to_html(markdown_text: str) -> str:
    # Prefer a real Markdown parser when available.
    try:
        import markdown as markdown_lib

        return markdown_lib.markdown(
            markdown_text, extensions=["extra", "sane_lists", "nl2br"]
        )
    except ImportError:
        pass

    lines = markdown_text.splitlines()
    parts = []
    in_list = False

    def close_list():
        nonlocal in_list
        if in_list:
            parts.append("</ul>")
            in_list = False

    def apply_inline(text: str) -> str:
        escaped = html.escape(text)
        escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
        escaped = re.sub(
            r"\*\*\*([^\*]+)\*\*\*", r"<strong><em>\1</em></strong>", escaped
        )
        escaped = re.sub(r"\*\*([^\*]+)\*\*", r"<strong>\1</strong>", escaped)
        escaped = re.sub(r"\*([^\*]+)\*", r"<em>\1</em>", escaped)
        escaped = re.sub(
            r"\[([^\]]+)\]\((https?://[^)]+)\)",
            r'<a href="\2">\1</a>',
            escaped,
        )
        return escaped

    for line in lines:
        stripped = line.strip()
        if not stripped:
            close_list()
            continue

        if stripped.startswith("### "):
            close_list()
            parts.append(f"<h3>{apply_inline(stripped[4:])}</h3>")
            continue
        if stripped.startswith("## "):
            close_list()
            parts.append(f"<h2>{apply_inline(stripped[3:])}</h2>")
            continue
        if stripped.startswith("# "):
            close_list()
            parts.append(f"<h1>{apply_inline(stripped[2:])}</h1>")
            continue
        if stripped.startswith(("- ", "* ")):
            if not in_list:
                parts.append("<ul>")
                in_list = True
            parts.append(f"<li>{apply_inline(stripped[2:])}</li>")
            continue

        close_list()
        parts.append(f"<p>{apply_inline(stripped)}</p>")

    close_list()
    return "\n".join(parts)


def send_email(subject: str, body: str, to_email: str, content_format: str = "plain"):
    email = os.environ.get("EMAIL_USER")
    password = os.environ.get("EMAIL_PASS")

    if not email or not password:
        print("Erro: defina EMAIL_USER e EMAIL_PASS")
        sys.exit(1)

    validate_recipient(to_email)

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = email
    msg["To"] = to_email
    if content_format == "html":
        msg.set_content("This email contains HTML content. Use an HTML-capable client.")
        msg.add_alternative(body, subtype="html")
    elif content_format == "markdown":
        msg.set_content(body)
        msg.add_alternative(markdown_to_html(body), subtype="html")
    else:
        msg.set_content(body)

    success = True
    error = None

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email, password)
            smtp.send_message(msg)
    except Exception as e:
        success = False
        error = str(e)

    # salvar log
    with shelve.open(DB_PATH) as db:
        logs = db.get("logs", [])
        log_entry = {
            "id": len(logs) + 1,
            "timestamp": datetime.now().isoformat(),
            "subject": subject,
            "to": to_email,
            "message": body,
            "success": success,
            "error": error,
        }
        logs.append(log_entry)
        db["logs"] = logs

    return log_entry


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--help", action="store_true")

    parser.add_argument("--subject")
    parser.add_argument("--message")
    parser.add_argument("--html", action="store_true")
    parser.add_argument("--markdown", action="store_true")
    parser.add_argument("--to")
    parser.add_argument("--auth", action="store_true")
    parser.add_argument("--silent", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--show-history", action="store_true")
    parser.add_argument("--show-message")
    parser.add_argument("--clear-history", action="store_true")
    parser.add_argument("--delete-log-message")
    parser.add_argument("--show-trash", action="store_true")
    parser.add_argument("--restore-log")
    parser.add_argument("--reindex", action="store_true")

    return parser.parse_args()


def validate_args(args):
    # comandos especiais não precisam validar envio
    if (
        args.auth
        or args.show_history
        or args.show_message
        or args.show_trash
        or args.restore_log
        or args.delete_log_message
        or args.clear_history
        or args.reindex
    ):
        return

    # validação de envio
    if not args.subject or not args.message:
        print("Erro: --subject e --message são obrigatórios")
        show_usage()
        sys.exit(1)
    if args.html and args.markdown:
        print("Erro: use apenas um entre --html e --markdown")
        sys.exit(1)


def handle_special_commands(args):
    if args.auth:
        open_auth_flow()
        return True

    if args.show_history:
        show_history(args.json)
        return True

    if args.show_message:
        show_message(args.show_message, args.json)
        return True

    if args.show_trash:
        show_trash(args.json)
        return True

    if args.restore_log:
        ok = restore_log(args.restore_log)
        if not args.silent:
            print("Restaurado" if ok else "ID não encontrado")
        return True

    if args.delete_log_message:
        ok = move_log_to_trash(args.delete_log_message)
        if not args.silent:
            print(f"Log movido para lixeira" if ok else "ID não encontrado")
        return True

    if args.clear_history:
        move_all_logs_to_trash()
        if not args.silent:
            print("Histórico movido para lixeira")
        return True

    if args.reindex:
        reindex_logs()
        if not args.silent:
            print("Reindexado")
        return True

    return False


def main():
    # carregar .env relativo ao script (funciona com symlinks e aliases)
    load_dotenv(dotenv_path=SCRIPT_DIR / ".env")
    global ALLOWED_RECIPIENTS
    ALLOWED_RECIPIENTS = get_allowed_recipients()

    args = parse_args()
    if args.help:
        show_usage()
        sys.exit(0)
    validate_args(args)

    if handle_special_commands(args):
        return

    # 📥 suporte a stdin
    body = args.message
    if body == "-":
        body = sys.stdin.read()

    # envia para mim mesmo se não especificar destinatário
    to_email = args.to or os.environ.get("EMAIL_USER")

    if not to_email:
        print("Erro: destinatário não definido")
        sys.exit(1)

    content_format = "plain"
    if args.html:
        content_format = "html"
    elif args.markdown:
        content_format = "markdown"

    result = send_email(args.subject, body, to_email, content_format)

    if not args.silent:
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            status = "OK" if result["success"] else "FAIL"
            print(f"[EMAIL] {status} -> {to_email}")

    # ❗ sair com código apropriado
    if not result["success"]:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
