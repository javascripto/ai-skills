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

### Escapando caracteres especiais

Alguns shells interativos (especialmente `zsh` e `bash` com history expansion ativado) podem interpretar caracteres como `!` quando você passa texto como argumento. Como este script espera o texto como argumento, recomenda-se sempre escapar ou usar aspas que previnam expansões antes de chamar o script.

Recomendações ao passar o texto como argumento:

- Use aspas simples quando possível (evita expansão de histórico e expansão de variáveis):

```bash
./scripts/say_fernanda.sh 'Olá! Este texto tem exclamação!'
```

- Se precisar usar aspas duplas, escape o `!` com `\!` para evitar history expansion:

```bash
./scripts/say_fernanda.sh "Olá\! Teste com exclamação"
```

- Alternativamente, escape apenas o `!` dentro de aspas duplas:

```bash
./scripts/say_fernanda.sh "Isso é uma exclamação: \!"
```

Observação: o `say` wrapper aqui aceita o texto via argumento (`$*`). Se preferir evitar quaisquer problemas de expansão ao construir a string dinamicamente, construa e passe o argumento de forma segura no cliente que chama o script (por exemplo, usando APIs que evitem a passagem direta pela linha de comando).

#### Outros caracteres problemáticos

Além de `!`, vários outros caracteres podem causar interpretação pelo shell ou pela camada que constrói a linha de comando. Exemplos comuns:

- `$` (expansão de variáveis)
- `` ` `` (command substitution)
- `"` e `'` (aspas não fechadas)
- `\` (escape)
- `|`, `&`, `;` (operadores de pipeline/background/terminador)
- `<`, `>`, `(`, `)`, `*`, `?`, `[`, `]` (redirecionamento/globbing)
- `~` e `#` (expansões e comentários em alguns shells)
- Quebras de linha e caracteres NUL

Se o texto que será lido puder conter qualquer um desses, prefira uma das estratégias a seguir para evitar problemas:

- Use aspas simples ao passar o argumento: `./scripts/say_fernanda.sh 'Texto com $ e ! sem expansão'`.
- Escape apenas os caracteres problemáticos dentro de aspas duplas: `"` -> `\"`, `!` -> `\!`, etc.
- Use um arquivo temporário e o `say -f <file>` (forma robusta):

```bash
printf '%s' "Texto com chars problemáticos: $ ` \ " ' | &" > /tmp/msg.txt
say -v "Fernanda" -r 300 -f /tmp/msg.txt
```

Observação: `say` aceita a opção `-f <file>` que lê o texto do arquivo, evitando a maior parte das interpretações da linha de comando.

- Outra opção é criar o arquivo temporário e chamar o wrapper lendo o conteúdo via `cat` para uma substituição segura no cliente, mas preferimos `say -f` quando possível.

Escolha a estratégia que melhor se adapta ao seu fluxo: para strings curtas e controladas, aspas simples ou escape pontual bastam; para conteúdo livre do usuário (ou que contenha muitas marcas), use `-f` com um arquivo temporário.

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
