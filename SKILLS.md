# Índice de Skills

## Objetivo
Índice central das skills disponíveis neste repositório.

## Categorias

Categorias oficiais para classificar skills atuais e futuras:

| Categoria | Uso |
|---|---|
| `frontend` | Setup, UI e experiência em aplicações web frontend |
| `backend` | APIs, serviços, integrações de servidor e lógica de negócio |
| `fullstack` | Fluxos que cobrem frontend e backend |
| `tools` | Automações de CLI, utilitários e fluxos de engenharia |
| `media` | Captura, extração, transcrição e processamento de mídia |
| `docs` | Documentação, padronização e geração de conteúdo técnico |
| `meta` | Skills para criação, manutenção e governança de outras skills |

## Skills Disponíveis

| Skill | Caminho | Categorias | Status | Notas |
|---|---|---|---|---|
| Manus Skill Creator | `skills/manus-skill-creator/SKILL.md` | `meta`, `docs` | estável | Skill de criação de skills orientada ao ecossistema Manus |
| Codex Skill Creator | `skills/codex-skill-creator/SKILL.md` | `meta`, `docs` | estável | Skill de criação/atualização de skills para o fluxo Codex |
| Init Vite React TS | `skills/init-vite-react-ts/SKILL.md` | `frontend`, `tools` | estável | Cria/limpa a base de projeto Vite React TypeScript |
| Add Tailwind + shadcn | `skills/add-tailwind-shadcn/SKILL.md` | `frontend`, `tools` | estável | Setup não-destrutivo de Tailwind v4 + shadcn |
| Add shadcn Darkmode Theme | `skills/add-shadcn-darkmode-theme/SKILL.md` | `frontend` | estável | Provider e toggle de tema light/dark/system |
| Frontend Aesthetic Guard | `skills/frontend-aesthetic-guard/SKILL.md` | `frontend` | estável | Guia para interfaces frontend premium, responsivas e não-genéricas |
| Frontend Design | `skills/frontend-design/SKILL.md` | `frontend` | estável | Criação de interfaces frontend memoráveis com direção estética ousada e execução de nível produção |
| Web Design Guidelines | `skills/web-design-guidelines/SKILL.md` | `frontend`, `tools` | estável | Revisa arquivos de interface web contra diretrizes atualizadas e reporta findings em formato `file:line` |
| Web Artifacts Builder | `skills/web-artifacts-builder/SKILL.md` | `frontend`, `tools` | estável | Criação de artifacts HTML complexos com React + Tailwind + shadcn e bundle final em arquivo único |
| Generate Favicons RFG | `skills/generate-favicons-rfg/SKILL.md` | `tools`, `frontend` | estável | Gera pacote de favicons/manifest via RealFaviconGenerator e integra no projeto com atualização idempotente do `index.html` |
| YouTube Caption Fetcher | `skills/youtube-caption-fetcher/SKILL.md` | `media`, `tools` | estável | Busca legendas do YouTube com fallback para download de áudio |
| YouTube Thumbnail Links | `skills/youtube-thumbnail-links/SKILL.md` | `media`, `tools` | estável | Gera links de thumbnails do YouTube em múltiplos tamanhos a partir de URL ou video ID, com saída plain/Markdown/JSON |
| YouTube Video Info | `skills/youtube-video-info/SKILL.md` | `media`, `tools` | estável | Extrai metadados comuns de vídeos do YouTube (título, descrição, canal, duração, data e contadores) em formatos plain/Markdown/JSON |
| Instagram Caption Fetcher | `skills/instagram-caption-fetcher/SKILL.md` | `media`, `tools` | estável | Extrai legendas do Instagram com fallback para transcrição de áudio |
| Local Faster Whisper Transcribe | `skills/local-faster-whisper-transcribe/SKILL.md` | `media`, `tools` | estável | Transcreve áudio/vídeo localmente com faster-whisper (offline) |

## Convenções
- Manter uma skill por diretório em `skills/<skill-name>/SKILL.md`.
- Classificar toda nova skill com pelo menos uma categoria oficial desta página.
- Preferir instruções não-destrutivas em projetos existentes.
- Atualizar este índice ao adicionar, descontinuar ou renomear qualquer skill.
