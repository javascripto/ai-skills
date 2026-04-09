---
name: voice-clone-local
description: Clone uma voz localmente com Qwen3-TTS Base usando áudio de referência e a transcrição correspondente. Use quando o usuário quiser clonagem de voz sem custo de API externa, precisar de um fluxo com `ref_audio` e `ref_text`, ou quiser uma rotina offline prática para similaridade de voz em português brasileiro.
---

# Voice Clone Local

Use esta skill para clonagem de voz local com `mlx-community/Qwen3-TTS-12Hz-0.6B-Base-4bit`.

Esta skill é específica para clonar ou aproximar a voz de um falante alvo. Ela não é a melhor escolha para TTS barato e de alta vazão. Para narração comum em pt-BR, prefira `local-tts-ptbr`.

Para o mapa completo do stack local de voz, leia [references/local-voice-stack.md](../_shared/references/local-voice-stack.md).

## Início rápido

1. Comece com uma amostra limpa do falante alvo.
2. Gere a transcrição exata dessa mesma amostra.
3. Use a amostra como `ref_audio`.
4. Use a transcrição exata como `ref_text`.
5. Gere o novo áudio com `Qwen3-TTS-Base`.

Para detalhes de preparação da referência, leia [references/reference-prep.md](references/reference-prep.md).

## Fluxo

1. Valide se o usuário realmente quer clonagem, e não apenas TTS.
2. Inspecione a qualidade do áudio de referência.
3. Prepare ou confirme a transcrição exata.
4. Rode a geração da clonagem.
5. Compare fidelidade, sotaque e ritmo.
6. Se necessário, tente novamente com uma amostra de referência mais limpa antes de trocar de modelo.

## Guia de decisão

Use esta skill quando:
- o usuário disser "clone minha voz"
- o fluxo incluir `ref_audio` e `ref_text`
- o usuário quiser clonagem totalmente local
- fidelidade importar mais do que velocidade bruta

Não use esta skill como padrão quando:
- o usuário só precisar de uma voz pronta em português brasileiro
- a máquina estiver limitada demais para um modelo mais pesado
- tempo de resposta importar mais do que similaridade com a identidade vocal

## Escolha de modelo

Modelo preferido com base nos testes registrados:

- `mlx-community/Qwen3-TTS-12Hz-0.6B-Base-4bit`

Evite usar a variante `CustomVoice` como padrão para clonagem, porque os testes indicaram que a variante `Base` foi o caminho certo para clonagem guiada por referência.

## Skills relacionadas

- Use `local-faster-whisper-transcribe` se precisar extrair `ref_text` rapidamente.
- Use `whispercpp-transcribe` se o ambiente estiver centrado em `whisper.cpp`.
- Use `local-tts-ptbr` quando clonagem não for necessária e vozes prontas forem suficientes.

## Exemplos de prompt

- "Clone minha voz localmente a partir deste `m4a` e da transcrição correspondente."
- "Use `Qwen3-TTS-Base` com `ref_audio` e `ref_text` para gerar um WAV novo."
- "Prepare a transcrição da amostra e depois gere uma fala parecida com a voz original."

## Observações

- Os testes registrados mostraram `Qwen3-TTS-Base` como o melhor caminho para clonagem.
- A qualidade e aderência da transcrição importaram muito para a fidelidade final.
- Este fluxo é mais lento e mais pesado que `Piper` ou `Kokoro`, mas bem melhor para similaridade de voz.
- `KokoClone` pode servir como alternativa experimental, mas os testes mostraram menos fidelidade e mais sotaque misto que o `Qwen3-TTS-Base`.
