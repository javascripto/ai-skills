#!/usr/bin/env bash
# validate-tiss.sh — Valida um arquivo XML TISS via api.validadortiss.com.br
# Uso: ./validate-tiss.sh <arquivo.xml> [bearer_token]
#
# Estratégia de autenticação:
# 1) Usa token informado/ambiente/arquivo se estiver válido
# 2) Se token ausente/expirado/inválido, gera novo token com login OAuth+PKCE
#
# Credenciais para login automático (não salvar na skill):
# - Variáveis: TISS_VALIDATOR_EMAIL e TISS_VALIDATOR_PASSWORD
# - Arquivo: ~/.tiss-credentials com linhas KEY=VALUE

set -euo pipefail

API_BASE="https://api.validadortiss.com.br/tiss/validador"
AUTH_BASE="https://auth.validadortiss.com.br"
APP_ORIGIN="https://app.validadortiss.com.br"
CLIENT_ID="c0a9f4021dc514e0dbc111b3420dfeb8"
REDIRECT_URI="https://app.validadortiss.com.br/"
SCOPE="openid email"

TOKEN_FILE="${HOME}/.tiss-token"
CREDENTIALS_FILE="${HOME}/.tiss-credentials"
TOKEN_SKEW_SECONDS=60

log() {
  echo "[validate-tiss] $*" >&2
}

die() {
  echo "Erro: $*" >&2
  exit 1
}

strip_wrapping_quotes() {
  local v="$1"
  if [[ "$v" == \"*\" && "$v" == *\" ]]; then
    v="${v:1:${#v}-2}"
  elif [[ "$v" == \'*\' && "$v" == *\' ]]; then
    v="${v:1:${#v}-2}"
  fi
  printf '%s' "$v"
}

get_credential_from_file() {
  local key="$1"
  local line

  [[ -f "$CREDENTIALS_FILE" ]] || return 1

  line="$(grep -m1 -E "^[[:space:]]*${key}=" "$CREDENTIALS_FILE" || true)"
  [[ -n "$line" ]] || return 1

  line="${line#*=}"
  line="$(strip_wrapping_quotes "$line")"
  printf '%s' "$line"
}

load_credentials() {
  local email="${TISS_VALIDATOR_EMAIL:-}"
  local password="${TISS_VALIDATOR_PASSWORD:-}"

  if [[ -z "$email" ]]; then
    email="$(get_credential_from_file "TISS_VALIDATOR_EMAIL" || true)"
  fi

  if [[ -z "$password" ]]; then
    password="$(get_credential_from_file "TISS_VALIDATOR_PASSWORD" || true)"
  fi

  if [[ -z "$email" || -z "$password" ]]; then
    return 1
  fi

  printf '%s\n%s\n' "$email" "$password"
}

read_token_from_sources() {
  if [[ -n "${2:-}" ]]; then
    printf '%s' "$2"
    return 0
  fi

  if [[ -n "${TISS_VALIDATOR_TOKEN:-}" ]]; then
    printf '%s' "$TISS_VALIDATOR_TOKEN"
    return 0
  fi

  if [[ -f "$TOKEN_FILE" ]]; then
    tr -d '[:space:]' < "$TOKEN_FILE"
    return 0
  fi

  return 1
}

token_exp_unix() {
  local token="$1"
  python3 - "$token" <<'PY'
import sys, json, base64

token = sys.argv[1].strip()
parts = token.split('.')
if len(parts) != 3:
    print('')
    raise SystemExit(0)

payload = parts[1]
payload += '=' * (-len(payload) % 4)
try:
    data = json.loads(base64.urlsafe_b64decode(payload.encode()))
except Exception:
    print('')
    raise SystemExit(0)

exp = data.get('exp')
print(exp if isinstance(exp, int) else '')
PY
}

token_is_probably_valid() {
  local token="$1"
  local exp now

  [[ -n "$token" ]] || return 1

  exp="$(token_exp_unix "$token")"
  if [[ -z "$exp" ]]; then
    # Se não for possível ler exp, tenta usar e deixa a API decidir.
    return 0
  fi

  now="$(date +%s)"
  (( now + TOKEN_SKEW_SECONDS < exp ))
}

gen_pkce_values() {
  python3 <<'PY'
import secrets, hashlib, base64

state = secrets.token_urlsafe(32)
nonce = secrets.token_urlsafe(24)
verifier = secrets.token_urlsafe(64)[:96]
challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip('=')

print(state)
print(nonce)
print(verifier)
print(challenge)
PY
}

json_field() {
  local body="$1"
  local field="$2"
  python3 - "$field" <<'PY' <<<"$body"
import sys, json

field = sys.argv[1]
try:
    data = json.load(sys.stdin)
except Exception:
    print('')
    raise SystemExit(0)

value = data.get(field, '')
if isinstance(value, (dict, list)):
    print('')
else:
    print(value if value is not None else '')
PY
}

authenticate_and_get_token() {
  local creds email password
  local state nonce code_verifier code_challenge
  local auth_effective_url tid state_back
  local status_payload login_payload
  local login_response login_http
  local login_body auth_code
  local token_response token_http token_body access_token

  creds="$(load_credentials)" || die "credenciais ausentes. Defina TISS_VALIDATOR_EMAIL/TISS_VALIDATOR_PASSWORD ou ~/.tiss-credentials"
  email="$(printf '%s\n' "$creds" | sed -n '1p')"
  password="$(printf '%s\n' "$creds" | sed -n '2p')"

  readarray -t pkce < <(gen_pkce_values)
  state="${pkce[0]}"
  nonce="${pkce[1]}"
  code_verifier="${pkce[2]}"
  code_challenge="${pkce[3]}"

  auth_effective_url="$(curl -sS -L -o /dev/null -w '%{url_effective}' -G "${AUTH_BASE}/oauth/authorize" \
    --data-urlencode "client_id=${CLIENT_ID}" \
    --data-urlencode "redirect_uri=${REDIRECT_URI}" \
    --data-urlencode 'response_type=code' \
    --data-urlencode "scope=${SCOPE}" \
    --data-urlencode "state=${state}" \
    --data-urlencode "nonce=${nonce}" \
    --data-urlencode "code_challenge=${code_challenge}" \
    --data-urlencode 'code_challenge_method=S256')"

  tid="$(python3 - "$auth_effective_url" <<'PY'
import sys
from urllib.parse import urlparse, parse_qs
url = sys.argv[1]
print(parse_qs(urlparse(url).query).get('tid', [''])[0])
PY
)"

  state_back="$(python3 - "$auth_effective_url" <<'PY'
import sys
from urllib.parse import urlparse, parse_qs
url = sys.argv[1]
print(parse_qs(urlparse(url).query).get('state', [''])[0])
PY
)"

  [[ -n "$tid" ]] || die "não foi possível iniciar sessão de login (tid ausente)"
  [[ -n "$state_back" ]] || die "não foi possível iniciar sessão de login (state ausente)"

  status_payload="$(python3 - "$tid" "$email" <<'PY'
import sys, json
print(json.dumps({
  'TransactionId': sys.argv[1],
  'User': {'UserName': '', 'Email': sys.argv[2], 'PhoneNumber': ''}
}, separators=(',',':')))
PY
)"

  curl -sS "${AUTH_BASE}/LoginApp/Status/" \
    -H 'accept: */*' \
    -H 'content-type: application/json' \
    -H "origin: ${AUTH_BASE}" \
    -H "referer: ${AUTH_BASE}/oauth/login/?client=${CLIENT_ID}&state=${state_back}&tid=${tid}" \
    --data "$status_payload" > /dev/null

  login_payload="$(python3 - "$tid" "$email" "$password" <<'PY'
import sys, json
print(json.dumps({
  'TransactionId': sys.argv[1],
  'User': {'UserName': '', 'Email': sys.argv[2], 'PhoneNumber': ''},
  'Password': sys.argv[3]
}, separators=(',',':')))
PY
)"

  login_response="$(curl -sS -w '\n%{http_code}' "${AUTH_BASE}/LoginApp/Login/" \
    -H 'accept: */*' \
    -H 'content-type: application/json' \
    -H "origin: ${AUTH_BASE}" \
    -H "referer: ${AUTH_BASE}/oauth/login/?client=${CLIENT_ID}&state=${state_back}&tid=${tid}" \
    --data "$login_payload")"

  login_http="$(echo "$login_response" | tail -1)"
  login_body="$(echo "$login_response" | sed '$d')"

  if [[ "$login_http" -ge 400 ]]; then
    die "falha no login (HTTP ${login_http})"
  fi

  auth_code="$(json_field "$login_body" 'code')"
  if [[ -z "$auth_code" ]]; then
    die "login não retornou authorization code"
  fi

  token_response="$(curl -sS -w '\n%{http_code}' -X POST "${AUTH_BASE}/oauth/token" \
    -H 'content-type: application/x-www-form-urlencoded' \
    -H "origin: ${APP_ORIGIN}" \
    -H "referer: ${APP_ORIGIN}/" \
    --data-urlencode 'grant_type=authorization_code' \
    --data-urlencode "code=${auth_code}" \
    --data-urlencode "redirect_uri=${REDIRECT_URI}" \
    --data-urlencode "code_verifier=${code_verifier}" \
    --data-urlencode "scope=${SCOPE}" \
    --data-urlencode "client_id=${CLIENT_ID}")"

  token_http="$(echo "$token_response" | tail -1)"
  token_body="$(echo "$token_response" | sed '$d')"

  if [[ "$token_http" -ge 400 ]]; then
    die "falha ao obter token (HTTP ${token_http})"
  fi

  access_token="$(json_field "$token_body" 'access_token')"
  [[ -n "$access_token" ]] || die "endpoint /oauth/token não retornou access_token"

  umask 077
  printf '%s\n' "$access_token" > "$TOKEN_FILE"

  printf '%s' "$access_token"
}

run_validation_with_token() {
  local token="$1"
  local filename upload_response upload_code upload_body validation_id
  local result_response result_code result_body=""
  local i

  filename="$(basename "$XML_FILE")"

  log "Enviando '${filename}' para validação..."

  upload_response="$(curl -sS -w "\n%{http_code}" \
    "${API_BASE}/validacoes" \
    -H 'accept: */*' \
    -H "authorization: Bearer ${token}" \
    -H "origin: ${APP_ORIGIN}" \
    -H "referer: ${APP_ORIGIN}/" \
    -F "fileUpload=@${XML_FILE};type=text/xml;filename=${filename}")"

  upload_code="$(echo "$upload_response" | tail -1)"
  upload_body="$(echo "$upload_response" | sed '$d')"

  if [[ "$upload_code" -eq 401 || "$upload_code" -eq 403 ]]; then
    return 41
  fi

  if [[ "$upload_code" -ge 400 ]]; then
    echo "Erro no upload (HTTP ${upload_code}):" >&2
    echo "$upload_body" >&2
    return 1
  fi

  validation_id="$(echo "$upload_body" | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' | head -1)"
  if [[ -z "$validation_id" ]]; then
    echo "Erro: não foi possível extrair o ID da validação." >&2
    echo "Resposta: $upload_body" >&2
    return 1
  fi

  log "Validação criada: ${validation_id}"
  log "Aguardando resultado..."
  sleep 2

  for i in $(seq 1 10); do
    result_response="$(curl -sS -w "\n%{http_code}" \
      "${API_BASE}/validacoes/'${validation_id}'/" \
      -H 'accept: */*' \
      -H "authorization: Bearer ${token}" \
      -H "origin: ${APP_ORIGIN}" \
      -H "referer: ${APP_ORIGIN}/")"

    result_code="$(echo "$result_response" | tail -1)"
    result_body="$(echo "$result_response" | sed '$d')"

    if [[ "$result_code" -eq 401 || "$result_code" -eq 403 ]]; then
      return 41
    fi

    if [[ "$result_code" -eq 200 ]] && echo "$result_body" | grep -q "erros\|valido\|hash\|guia"; then
      break
    fi

    if [[ "$i" -lt 10 ]]; then
      sleep 2
    fi
  done

  echo ""
  echo "═══════════════════════════════════════════════════"
  echo "  Resultado da Validação TISS"
  echo "  ID: $validation_id"
  echo "═══════════════════════════════════════════════════"
  echo ""
  echo "$result_body"
}

XML_FILE="${1:?Uso: validate-tiss.sh <arquivo.xml> [bearer_token]}"

if [[ ! -f "$XML_FILE" ]]; then
  die "arquivo '$XML_FILE' não encontrado"
fi

TOKEN="$(read_token_from_sources "$XML_FILE" "${2:-}" || true)"

if [[ -n "$TOKEN" ]] && token_is_probably_valid "$TOKEN"; then
  log "Usando token existente (parece válido)."
else
  if [[ -n "$TOKEN" ]]; then
    log "Token existente expirado/inválido. Gerando novo token..."
  else
    log "Token ausente. Gerando novo token..."
  fi
  TOKEN="$(authenticate_and_get_token)"
fi

if run_validation_with_token "$TOKEN"; then
  exit 0
fi

RC=$?
if [[ "$RC" -eq 41 ]]; then
  log "Token rejeitado pela API (401/403). Tentando reautenticar e reenviar..."
  TOKEN="$(authenticate_and_get_token)"
  run_validation_with_token "$TOKEN"
  exit $?
fi

exit "$RC"
