---
name: macos-say-fernanda
description: Skill simples para rodar o comando `say` no macOS usando a voz "Fernanda".
---

# macOS `say` — voz Fernanda

Esta skill expõe um uso simples do utilitário nativo `say` do macOS para ler texto em voz alta usando a voz `Fernanda` com velocidade configurada para `300`.

Use quando o usuário quiser que o agente fale uma mensagem diretamente no macOS local do desenvolvedor/operador.

Observações importantes:
- Funciona apenas em macOS com o comando `say` disponível.
- A voice name é `Fernanda` e a taxa padrão (`-r`) é `300`.

## Arquivos
- `scripts/say_fernanda.sh` — wrapper simples que aceita uma string e chama `say`.

## Uso
1. Do diretório da skill, executar:

```bash
./scripts/say_fernanda.sh "Texto que será lido"
```

2. Ou, se preferir, chamar diretamente o comando:

```bash
say -v "Fernanda" -r 300 "Texto que será lido"
```

### Parar a fala

Se precisar interromper a fala em execução:

- Pressione `Ctrl+C` se o `say` estiver rodando em primeiro plano.
- Para interromper todas as instâncias do `say` no sistema:

```bash
killall say
# ou
pkill -f 'say -v "Fernanda"'
```

Adicionei também um script de conveniência `scripts/stop_say_fernanda.sh` que mata apenas as instâncias iniciadas com a voz `Fernanda`.

```bash
./scripts/stop_say_fernanda.sh
```


## Exemplo de integração com outras skills
- Para fluxos que geram TTS como arquivo, use `play-audio` quando o usuário preferir ouvir um arquivo.
- Use esta skill quando for aceitável rodar `say` localmente no host do agente.

## Perguntas de segurança / privacidade
- Deixe claro ao usuário que o áudio será reproduzido no computador onde a skill é executada.

---
