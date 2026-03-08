---
name: validate-tiss
description: "Valida arquivos XML TISS usando a API do validadortiss.com.br. USE QUANDO: o usuário pedir para validar XML TISS, verificar conformidade TISS, testar XML gerado, corrigir erros de validação TISS. Envia o XML para o validador online e retorna os erros encontrados."
---

# Validar arquivo XML TISS

Skill para validar arquivos XML TISS 3.x contra o validador oficial em `validadortiss.com.br`.

## Pré-requisitos

### Arquivos externos (fora da skill)

1. Token opcional em `~/.tiss-token` (apenas o token, sem quebra de linha)
2. Credenciais para relogin automático em `~/.tiss-credentials`:

```bash
cat > ~/.tiss-credentials <<'CFG'
TISS_VALIDATOR_EMAIL='seu-email@dominio.com'
TISS_VALIDATOR_PASSWORD='sua-senha'
CFG
chmod 600 ~/.tiss-credentials
```

Também pode usar variáveis de ambiente:
- `TISS_VALIDATOR_TOKEN`
- `TISS_VALIDATOR_EMAIL`
- `TISS_VALIDATOR_PASSWORD`

## Fluxo de autenticação (automático)

O script `validate-tiss.sh` agora faz este fluxo:

1. Lê token de: argumento > `TISS_VALIDATOR_TOKEN` > `~/.tiss-token`
2. Se o token existir, verifica validade pelo `exp` do JWT
3. Se token ausente/expirado/inválido, faz login com usuário e senha e gera token novo (OAuth2 + PKCE)
4. Salva token novo em `~/.tiss-token`
5. Se upload/consulta responder `401/403`, refaz login e tenta novamente

## Dados da API

| Campo              | Valor                                                      |
|--------------------|-------------------------------------------------------------|
| Auth Issuer        | `https://auth.validadortiss.com.br`                        |
| Authorization URL  | `https://auth.validadortiss.com.br/oauth/authorize`        |
| Token endpoint     | `https://auth.validadortiss.com.br/oauth/token`            |
| API Base           | `https://api.validadortiss.com.br/tiss/validador`          |
| Client ID          | `c0a9f4021dc514e0dbc111b3420dfeb8`                         |
| Upload endpoint    | `POST /validacoes` (multipart, campo `fileUpload`)         |
| Resultado endpoint | `GET /validacoes/'<uuid>'/`                                |
| Origin obrigatório | `https://app.validadortiss.com.br`                         |

## Workflow

### Passo 1 — Preparar credenciais (uma vez)

```bash
cat > ~/.tiss-credentials <<'CFG'
TISS_VALIDATOR_EMAIL='seu-email@dominio.com'
TISS_VALIDATOR_PASSWORD='sua-senha'
CFG
chmod 600 ~/.tiss-credentials
```

### Passo 2 — Validar o XML

Use o script incluído:

```bash
~/.codex/skills/validate-tiss/validate-tiss.sh /caminho/do/arquivo.xml
```

Cópia equivalente (ambiente `.agents`):

```bash
~/.agents/skills/validate-tiss/validate-tiss.sh /caminho/do/arquivo.xml
```

### Passo 3 — Resultado

O script:
- envia o XML para `POST /validacoes`
- extrai o UUID
- consulta `GET /validacoes/'<uuid>'/` até obter o resultado
- imprime o JSON retornado pelo validador

## Erros comuns de validação TISS

| Erro | Causa | Correção |
|------|-------|----------|
| `namespace "ans" nas tags` | Tags sem prefixo `ans:` | Usar `prefixAns()` em `gerador-xml.ts` |
| `Element X is unexpected` | Elemento fora de ordem ou com nome errado | Verificar ordem dos elementos no XSD TISS 3.05 |
| `violates maxLength` | Valor com mais chars que o permitido | Mapear para código (ex: `CRM` → `06`) |
| `violates enumeration` | Valor fora do domínio permitido | Usar código IBGE para UF, código numérico para conselho |
| `hash informado está inválido` | Hash MD5 calculado incorretamente | Hash = MD5 da concatenação de todos os text nodes entre `<ans:mensagemTISS>` e `<ans:epilogo>` |
| `not declared in the DTD/Schema` | Elemento não existe no XSD | Verificar nome correto (ex: `procedimentosExecutados` não `procedimentosRealizados`) |

Quando houver erros, edite `src/lib/gerador-xml.ts` para corrigir a estrutura XML conforme o XSD TISS 3.05.

## Referência rápida de domínios TISS

### dm_conselhoProfissional (maxLength: 2)
| Sigla | Código |
|-------|--------|
| CRM | 06 |
| CRO | 07 |
| CRF | 08 |
| CREFITO | 09 |
| COREN | 10 |

### dm_UF (código IBGE)
| UF | Código |
|----|--------|
| SP | 35 |
| RJ | 33 |
| MG | 31 |
| PR | 41 |
| RS | 43 |
| BA | 29 |
| DF | 53 |

(Lista completa no mapeamento `UF_IBGE` em `src/lib/gerador-xml.ts`)
