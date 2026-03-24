---
name: play-audio
description: Reproduza arquivos de audio locais no macOS, Linux ou Windows com um comando nativo da plataforma. Use quando o usuario pedir para tocar, reproduzir, ouvir, testar ou validar um arquivo de audio local, e tambem como etapa final depois de gerar um arquivo de text-to-speech com outra skill.
---

# Play Audio

Use `scripts/play_audio.py` para reproduzir um arquivo de audio existente no computador atual.

Priorize este fluxo quando o pedido envolver ouvir o resultado, testar um arquivo gerado localmente, ou tocar o audio imediatamente apos uma skill de TTS salvar o arquivo.

## Workflow

1. Confirmar qual arquivo deve ser reproduzido.
2. Verificar se o arquivo existe.
3. Executar `python3 scripts/play_audio.py <arquivo>`.
4. Relatar qual backend foi usado pela plataforma.

## Platform Rules

- No macOS, usar `afplay`.
- No Linux, tentar nesta ordem: `pw-play`, `paplay`, `aplay`, `ffplay`.
- No Windows, usar PowerShell com `System.Windows.Media.MediaPlayer`.
- Se nenhum backend estiver disponivel, explicar o bloqueio claramente em vez de fingir que o audio foi reproduzido.

## TTS Integration

Quando outra skill gerar um arquivo de text-to-speech e o usuario quiser ouvir o resultado, chamar este playback no mesmo turno logo apos a geracao do arquivo. Nao encerrar o trabalho no arquivo gerado sem tentar tocar o resultado quando o pedido implicar audicao do material.

Exemplos de pedidos que devem acionar esta skill:

- "Reproduz esse audio."
- "Toca o mp3 que voce acabou de gerar."
- "Faz um text-to-speech e depois toca o resultado."
- "Quero ouvir esse wav."

## Command

Executar a partir da pasta da skill:

```bash
python3 scripts/play_audio.py /caminho/para/audio.wav
```

Ou, se precisar chamar sem trocar de diretório, resolver primeiro o caminho da skill no ambiente atual e entao executar o mesmo script por esse caminho.

Saida esperada:

- `Playing via afplay: ...`
- `Playing via paplay: ...`
- `Playing via powershell-mediaplayer: ...`

## Notes

- Manter o comportamento bloqueante por padrao para o audio terminar antes da conclusao do turno.
- Aceitar caminhos absolutos ou relativos.
- Preservar mensagens de erro objetivas quando o arquivo nao existir ou o sistema nao tiver backend compativel.
