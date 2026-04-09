# Motores Recomendados

## Escolha Rápida

- Use `Piper` quando a prioridade for velocidade, previsibilidade e sotaque brasileiro claro.
- Use `Kokoro` quando a prioridade for naturalidade geral com baixa latência.
- Evite usar esta skill para clonagem de voz. Para isso, prefira `voice-clone-local`.

## Vozes e Presets Citados nos Testes

### Piper

- Voz recomendada: `pt_BR-cadu-medium`
- Ponto forte: melhor equilíbrio prático para leitura em português brasileiro

### Kokoro

- Vozes testadas: `pm_alex`, `pm_santa`
- Ponto forte: leitura leve e natural

## Heuristicas de Selecao

Escolha `Piper` por padrão quando:
- o usuário pedir pt-BR explícito
- a máquina tiver pouca memória
- a tarefa pedir lotes, velocidade ou previsibilidade

Escolha `Kokoro` por padrão quando:
- a tarefa pedir uma leitura mais agradável
- a saída for curta ou média
- a latência ainda precisar ser baixa

## Benchmarks Resumidos

Texto de teste: `Olá, este é um teste de velocidade para comparar Piper e Kokoro no português brasileiro.`

| Motor | Voz | Tempo de geração | Duração | RTF |
|---|---|---:|---:|---:|
| Kokoro | `pm_santa` | `1.398 s` | `5.425 s` | `0.258` |
| Piper | `pt_BR-cadu-medium` | `1.158 s` | `5.712 s` | `0.203` |

## Observacoes

- `Piper` ficou ligeiramente mais rápido no teste registrado.
- `Kokoro` continuou muito competitivo e com boa naturalidade.
- Se um WAV sair vazio ou corrompido, gere novamente antes de concluir que o motor falhou.
