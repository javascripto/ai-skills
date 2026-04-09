---
name: local-tts-ptbr
description: Gere texto para fala local em português brasileiro com Piper ou Kokoro. Use quando o usuário quiser TTS offline, leitura em pt-BR, geração rápida de áudio, narração natural, ou uma escolha prática entre velocidade e qualidade de voz sem custo de API externa.
---

# Local TTS PT-BR

Use esta skill para texto para fala offline em português brasileiro.

Prefira `Piper` quando velocidade, previsibilidade e sotaque brasileiro explícito forem mais importantes. Prefira `Kokoro` quando o usuário quiser uma voz pronta mais leve e mais natural. Se o usuário pedir um experimento mais próximo de clonagem dentro desta skill, trate `Qwen3-TTS Base` como fallback experimental. Esta skill é para síntese, não para clonagem de voz.

Para o mapa completo do stack local de voz, incluindo clonagem e benchmarks, leia [references/local-voice-stack.md](../_shared/references/local-voice-stack.md).

## Início rápido

Recomendação padrão:

1. Se o usuário pedir a saída pt-BR mais rápida e prática, comece com `Piper`.
2. Se o usuário pedir uma voz pronta mais natural, comece com `Kokoro`.
3. Gere primeiro uma amostra curta.
4. Se o resultado estiver bom, gere o texto completo.
5. Se o resultado estiver fraco, troque de motor antes de ajustar detalhes pequenos.

## Guia de decisão

Escolha `Piper` quando:
- o usuário quiser explicitamente português do Brasil
- vazão e velocidade forem importantes
- a máquina for mais modesta
- pronúncia estável for mais importante que prosódia expressiva

Escolha `Kokoro` quando:
- o usuário quiser uma voz mais agradável já de saída
- a saída for curta ou média
- velocidade ainda importar, mas não como único critério

Saia desta skill quando:
- o usuário quiser clonagem de voz
- o fluxo exigir condicionamento com `ref_audio` e `ref_text`
- o usuário quiser fidelidade a uma pessoa específica em vez de uma voz pronta
- o usuário quiser usar `Qwen3-TTS Base` como caminho principal

Para detalhes dos motores e notas de benchmark, leia [references/engines.md](references/engines.md).

## Vozes

Vozes recomendadas com base nos testes registrados:

- `Piper`: `pt_BR-cadu-medium`
- `Kokoro`: `pm_alex`
- `Kokoro`: `pm_santa`

## Fluxo

1. Confirme se o objetivo é `speed` ou `naturality`.
2. Escolha `Piper` ou `Kokoro` de acordo com isso.
3. Gere primeiro uma frase curta.
4. Ouça qualidade do sotaque, ritmo e pronúncia.
5. Gere novamente o texto completo.
6. Se o áudio sair vazio ou claramente quebrado, rode mais uma vez antes de trocar de motor.

## Exemplos de prompt

- "Gere este texto em áudio local com sotaque brasileiro e a opção mais rápida."
- "Leia este roteiro em pt-BR com uma voz natural sem usar API externa."
- "Compare uma amostra curta em `Piper` e `Kokoro` e escolha a melhor."

## Observações

- Não use esta skill como padrão para clonar a voz do próprio usuário.
- `Piper` venceu a comparação de velocidade registrada por pequena margem.
- `Kokoro` continuou muito competitivo e soou muito bem em pt-BR.
- Se o usuário pedir fluxo estritamente offline e sem custo externo, esta skill é uma ótima opção.
- `Piper` também ficou muito bom na reprodução final, não só rápido.
- `Qwen3-TTS Base` só entra aqui como fallback experimental; para clonagem guiada por referência, use `voice-clone-local`.
- Se o usuário pedir clonagem ou fidelidade à voz de uma pessoa específica, saia desta skill e use `voice-clone-local`.
