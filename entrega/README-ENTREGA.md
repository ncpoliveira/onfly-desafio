# Entrega do desafio técnico Onfly

## Estudo independente

Antes de começar o desenvolvimento com IA, dediquei dois dias a estudar o código, revisar conceitos e entender a estrutura do projeto. Como o prazo permitia, fiz esse estudo à mão, com anotações em papel, pesquisas e leitura. Queria entender o máximo possível do caminho entre a leitura dos CSVs, o cálculo dos totais e a geração do relatório JSON antes de começar a alterar o código.

Meu objetivo de estudo hoje é reservar tempo para fazer por conta própria as tarefas que consolidam meu aprendizado. Quando a IA pode agilizar o trabalho ou ajudar a verificar uma mudança, uso suas sugestões como ponto de partida para uma decisão que eu consiga explicar e testar.

## Investigação e desenvolvimento com IA

Usei o Codex para entender melhor o projeto, tirar dúvidas que ainda restavam e avaliar alternativas que eu não havia considerado. Queria avançar com agilidade e entregar uma solução confiável. Começamos cruzando as regras do README com o código, os CSVs e os testes fornecidos. Na execução inicial, os cinco testes falharam. Reproduzimos as divergências com entradas pequenas e também executamos o CLI na base principal. A base completa revelou que o relatório contava apenas 200 das 300 reservas. Os testes fornecidos usavam amostras menores.

Dividi a implementação em cinco blocos na branch `codex/correcoes-relatorio`. Em cada bloco, discuti a causa, avaliei as opções e aprovei a mudança antes de o Codex implementá-la. Os testes de regressão reproduziram os defeitos com o código anterior à correção e passaram após o ajuste. Rodei a suíte completa com o Codex ao fechar cada bloco para acompanhar as falhas que ainda aguardavam correção. Cada correção foi registrada em um commit com seu teste.

## Defeitos corrigidos

| Defeito | Causa raiz | Correção e validação | Commit |
| --- | --- | --- | --- |
| Leitura incompleta | O leitor interrompia o laço ao atingir 200 reservas e descartava as linhas seguintes. | Removemos o corte e verificamos que a última linha de um CSV com 201 reservas entra no total geral e na contagem de canceladas. | `213d921` |
| Faturamento por status | A condição aceitava todo status diferente de `CANCELLED`, incluindo `NO_SHOW`. | Restringimos as agregações a `CONFIRMED` e testamos os grupos por mês e por hotel com os três status. | `d0ee8d0` |
| Noites na virada de mês ou ano | O cálculo subtraía os números dos dias do mês, perdendo as informações de mês e ano. | Passamos a subtrair as datas completas e multiplicar pelos quartos. Um teste cobre a virada de ano com dois quartos e confere a atribuição ao mês do check-in. | `7a114f2` |
| Conversão para BRL | O conversor transformava o valor e a taxa em `float` e dividia pela taxa. | Multiplicamos os valores em `Decimal` e verificamos a soma antes do arredondamento e a média arredondada com *half-up*. | `67ff4d8` |
| Ordem do ranking | A chave de ordenação colocava os menores totais em BRL nas primeiras posições. | Ordenamos pelo total decrescente e pelo ID crescente no empate. Um teste cobre dois hotéis empatados na última vaga de `--top 2`. | `b717d39` |

## Como validar

Na raiz do repositório, prepare o ambiente com Python 3.11 e execute os testes.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
pytest -q
```

Com Python 3.11.18 e pytest 8.3.4, o resultado foi **10 testes aprovados**, sendo cinco fornecidos e cinco de regressão. A análise estática com `ruff check src tests` também passou.

Execute o CLI na amostra e na base principal.

```bash
PYTHONPATH=src python -m onfly_report \
  --input data/exemplo-validacao.csv \
  --rates data/taxas_cambio.csv \
  --output output/exemplo.json

PYTHONPATH=src python -m onfly_report \
  --input data/reservas_hoteis.csv \
  --rates data/taxas_cambio.csv \
  --output output/report.json
```

| Campo | Amostra | Base principal |
| --- | ---: | ---: |
| Total de reservas | 12 | 300 |
| Confirmadas | 9 | 235 |
| Canceladas | 2 | 31 |
| `NO_SHOW` | 1 | 34 |
| Noites de quarto | 28 | 1.347 |
| Total em BRL | R$ 7.566,00 | R$ 396.170,00 |
| Média por noite | R$ 270,21 | R$ 294,11 |

Na validação final, conferimos o resumo, os agrupamentos mensais e o ranking da amostra com os valores do README. Para a base principal, comparamos o JSON com um cálculo independente a partir dos CSVs. Também verificamos o caminho de saída padrão, o offset `-03:00`, a média `"0.00"` quando não há noites e os códigos de saída em casos de argumentos inválidos e falha de gravação. A revisão do diff confirmou a preservação do README original, dos CSVs, dos testes fornecidos e da interface do CLI.

## Melhorias futuras

- **CSV com UTF-8 inválido.** Um arquivo de teste com bytes inválidos retornou código `1`. O CLI poderia identificar o arquivo afetado na mensagem e retornar `2` por entrada inválida.
- **Moeda sem taxa de câmbio.** Uma tabela de teste sem a taxa de uma moeda usada por uma reserva confirmada também resultou em código `1`. O CLI poderia informar a moeda ausente e retornar `2`.

Esses cenários foram reproduzidos com arquivos temporários criados para a investigação. Os CSVs fornecidos foram processados com sucesso e têm taxas para todas as moedas usadas.

O uso de IA está documentado no [registro da sessão](uso-de-ia/sessao.md) e na [declaração](uso-de-ia/declaracao.md).
