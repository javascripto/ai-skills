# Preparacao da Referencia

## Meta

Maximizar fidelidade de voz e sotaque brasileiro no `Qwen3-TTS-Base`.

## Receita Recomendada

1. Escolha uma gravação limpa do falante alvo.
2. Extraia a transcrição exata dessa gravação.
3. Use a gravação como `ref_audio`.
4. Use a transcrição literal como `ref_text`.
5. Gere o novo áudio com `mlx-community/Qwen3-TTS-12Hz-0.6B-Base-4bit`.

## O Que Funcionou Melhor nos Testes

- O melhor resultado apareceu quando `ref_audio` era a própria voz do usuário.
- O melhor `ref_text` foi a transcrição exata do áudio, sem reescrever frases.
- Textos de saída um pouco mais longos ajudaram a avaliar melhor fidelidade e naturalidade.

## Preparacao do `ref_text`

- Preserve hesitações e pequenas pausas apenas se elas realmente estiverem na gravação e forem importantes para o timbre percebido.
- Não resuma o texto.
- Não traduza o texto.
- Não normalize demais números, abreviações ou nomes próprios se isso mudar como a fala foi produzida.

## STT Recomendado

Para preparar a transcrição local:
- prefira `faster-whisper` pela praticidade
- use `whisper.cpp` se o ambiente já estiver centrado nessa stack

Skills relacionadas:
- `local-faster-whisper-transcribe`
- `whispercpp-transcribe`

## Custos e Memoria

- O `Qwen3-TTS-Base` foi o melhor em clonagem, mas é mais pesado e lento que `Piper` e `Kokoro`.
- Nos testes resumidos, o pico de memória ficou na faixa de ~7 GB a ~9 GB, dependendo do tamanho da geração.
