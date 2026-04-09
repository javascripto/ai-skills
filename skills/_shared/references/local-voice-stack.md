# Stack local de voz

## Objetivo

Contexto prático para geração local de TTS, clonagem de voz e preparação de referência em pt-BR.

## Mapa rápido

| Caso | Melhor escolha registrada | Observação |
|---|---|---|
| Clonar a voz do usuário | `Qwen3-TTS-12Hz-0.6B-Base-4bit` | Melhor fidelidade e melhor sotaque pt-BR nos testes |
| TTS pt-BR rápido | `Piper` | Muito bom para leitura natural e previsível |
| TTS pt-BR leve | `Kokoro` | Muito rápido e natural, sem clonagem |
| Clonagem experimental por pipeline | `KokoClone` | Funciona, mas o sotaque ficou mais misto que o Qwen3 |
| Transcrição local | `faster-whisper` | Caminho prático para extrair `ref_text` |
| Transcrição nativa | `whisper.cpp` | Útil quando o ambiente já usa GGML/whisper-cli |

## Preparação da referência

Regras que melhoraram a clonagem:

1. Use uma gravação limpa do falante alvo.
2. Prefira `wav` mono, 24 kHz, sem eco nem música.
3. Use a transcrição literal como `ref_text`.
4. Não resuma, não traduza e não “polia” demais o texto.
5. Para arquivos `m4a`, converta antes de clonar.

Exemplo de conversão útil no macOS:

```bash
afconvert -f WAVE -d LEI16@24000 "input.m4a" output.wav
```

## Qwen3-TTS Base

Use este fluxo quando fidelidade importar mais do que velocidade.

Parâmetros que funcionaram melhor:

- `model = mlx-community/Qwen3-TTS-12Hz-0.6B-Base-4bit`
- `ref_audio =` gravação do usuário em `wav`
- `ref_text =` transcrição exata da gravação
- `lang_code = portuguese`

Observações dos testes:

- melhor resultado para clonagem da voz
- sotaque pt-BR melhor que `CustomVoice`
- mais lento e mais pesado que `Piper` e `Kokoro`
- pico de memória ficou na faixa de ~7 GB a ~9 GB, dependendo do tamanho da geração

## KokoClone

Use como alternativa experimental quando quiser voz clonada em cima de Kokoro + Kanade.

Notas importantes:

- o pipeline lê `wav`, não `m4a`
- em pt-BR o sotaque ficou bom, mas menos fiel do que o Qwen3
- a voz ouvida no teste foi mais próxima do timbre do falante, porém ainda com sotaque misto
- bom para validar a ideia, não como primeira escolha para clonagem

## Piper e Kokoro

Use estes motores quando a clonagem não for necessária.

### Piper

- voz recomendada: `pt_BR-cadu-medium`
- melhor opção quando velocidade e previsibilidade forem prioridade
- muito bom em pt-BR
- no teste final, o WAV vazio foi um erro de geração inicial; a versão corrigida funcionou

### Kokoro

- vozes testadas em pt-BR: `pm_alex`, `pm_santa`
- muito rápido e natural
- excelente para leitura pronta
- não é o melhor caminho para clonar a voz do usuário

## Benchmarks resumidos

### Kokoro vs Piper

Texto de teste:

> Este é um novo teste em português brasileiro para comparar a naturalidade e o sotaque.

| Motor | Voz | Tempo | Duração | RTF |
|---|---|---:|---:|---:|
| Kokoro | `pm_santa` | `1.398 s` | `5.425 s` | `0.258` |
| Piper | `pt_BR-cadu-medium` | `1.158 s` | `5.712 s` | `0.203` |

### Comparativo final

| Modelo | Clonagem | Sotaque pt-BR | Velocidade |
|---|---|---|---:|
| Qwen3-TTS Base | melhor | melhor | mais lento |
| KokoClone | bom, mas não perfeito | ok, porém com sotaque misto | intermediário |
| Kokoro | não clona | muito bom | rápido |
| Piper | não clona | muito bom | muito rápido |

## Fluxo recomendado

1. Se houver áudio do usuário, primeiro transforme em `wav` e transcreva.
2. Se o objetivo for clonagem, use `Qwen3-TTS Base`.
3. Se o objetivo for leitura em pt-BR, use `Piper`.
4. Se o usuário quiser uma voz pronta mais leve, use `Kokoro`.
5. Se houver interesse experimental em clonagem via Kokoro, teste `KokoClone` depois de validar Qwen3.
