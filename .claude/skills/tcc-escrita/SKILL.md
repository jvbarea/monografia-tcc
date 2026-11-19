---
name: tcc-escrita
description: Guia de escrita e revisão da monografia do TCC "Implementação de Segurança Integrada em Redes LoRaWAN" (Poli-USP, frentes de infraestrutura, segurança e ML). Usar ao escrever, revisar ou padronizar qualquer capítulo .tex da tese, ao responder "este capítulo segue o padrão?", ao checar citações, referências, tempo verbal, numeração de requisitos ou pontuação, e antes de abrir um pull request. Aciona em pedidos como "revisa o Cap5", "padroniza minha seção", "roda a checagem da tese", "o que falta na minha parte".
allowed-tools: Read Bash Grep Glob
---

# Escrita da monografia

A tese é escrita por três pessoas, uma por frente (infraestrutura, segurança, ML), e o leitor
não pode sentir a costura. A organização por frente é mantida. O que é comum a todos é o
esqueleto de cada capítulo e as convenções abaixo. Este guia serve para escrever texto novo
e para revisar texto existente. Ele não muda o conteúdo técnico de ninguém.

As regras de trabalho do repositório, quem edita o quê, bibliografia, commits e
compilação, estão no `CLAUDE.md` da raiz e no de cada pasta de autor. Este guia
cobre só o padrão de escrita. Cada capítulo em `capitulos/` é um esqueleto que
faz `\input` dos fragmentos `<autor>/capN-*.tex`, e é sobre esses fragmentos que
a revisão acontece.

Ao revisar, o fluxo é sempre o mesmo.

1. Rodar `scripts/checar.py` na raiz do repositório (seção "Checagem automática").
2. Percorrer a lista de verificação manual da seção "Revisão de um capítulo".
3. Relatar o que não segue o padrão com arquivo e linha. Só editar quando o autor pedir.
   Nunca editar a seção de outra frente sem o autor dela pedir.

## Esqueleto comum

### 1. Mesma ordem em todo capítulo

As frentes aparecem sempre na ordem do caminho do dado. Sensor, enlace, proteção, análise.

1. Infraestrutura (nó, enlace LoRa, gateway)
2. Segurança (Ascon, biblioteca AsconSecure)
3. Machine Learning (dataset, modelo, detecção)

Nos capítulos 2, 3, 4 e 5 as subseções de frente aparecem nessa ordem, no mesmo nível de
título e com títulos paralelos. No esqueleto de cada capítulo isso é a ordem das linhas
`\input`, `barea/`, depois `felipe/`, depois `tadaki/`. Se a infra tem "Resultados da infraestrutura de comunicação",
as outras têm "Resultados da camada de segurança" e "Resultados do modelo de detecção", não
"Testes do Ascon" ou "Experimentos".

### 2. Parágrafo de ligação

Cada seção de frente começa com um parágrafo curto que diz o que ela recebe das outras
frentes e o que entrega, com `\ref` para as seções correspondentes. É aí que as costuras
ficam explícitas.

Modelo do parágrafo. "Esta seção trata de X. Ela parte de Y, definido na Seção~\ref{...} pela
frente de Z, e entrega W, usado na Seção~\ref{...}."

### 3. Tempo verbal fixo por capítulo

| Capítulo | Tempo | Exemplo |
|---|---|---|
| Cap1 Introdução | presente | "Este trabalho propõe" |
| Cap2 Conceitos | presente | "O LoRaWAN define" |
| Cap3 Método | presente | "A validação usa", "mede-se" |
| Cap4 Requisitos | presente | "O sistema deve" |
| Cap5 Resultados | passado | "Os testes mostraram" |
| Cap6 Considerações | passado para o feito, futuro só em Perspectivas | "ficam abertas três frentes" |

Fora do Cap6 não há "será realizado", "pretende-se", "em etapa futura", "ainda não foi".
O que não foi feito não aparece como promessa. Ou entra em Perspectivas do Cap6 ou sai.

### 4. Requisitos sem colisão

Os identificadores de requisito são únicos no documento inteiro, com prefixo de frente.

- Infraestrutura. RF-I1, RF-I2, ... e RNF-I1, RNF-I2, ...
- Segurança. RF-S1, ... e RNF-S1, ...
- Machine Learning. RF-M1, ... e RNF-M1, ...

Cada frente tem uma tabela de rastreabilidade no Cap4, com as mesmas colunas. Requisito,
onde é atendido (referência à seção de resultado no Cap5), situação (atendido,
parcialmente atendido, não verificado).

### 5. Fechamento uniforme das seções de resultado

Toda seção de resultado do Cap5 termina com dois blocos, nessa ordem.

- Um parágrafo ou tabela dizendo quais requisitos foram atendidos e quais não.
- Uma subseção "Limitações" com o que a medição não cobre, com esse mesmo título nas três.

### 6. Cap1 e Cap6 espelhados

Cada objetivo listado no Cap1 recebe um parágrafo de resposta no Cap6, na mesma ordem e com
as mesmas palavras-chave. O Cap6 não introduz objetivo novo. Títulos de capítulo e de seção
descrevem o conteúdo pronto, nunca o plano. Nada de "Preliminares", "Previstas" ou
"Propostas" em título.

### 7. Um termo por conceito

Cada conceito tem um único termo em todo o documento. Sem alternar entre sinônimos, sem
alternar entre português e inglês para a mesma coisa. Exemplos de como a regra se aplica.

| Adotado | Evitar |
|---|---|
| tag (de autenticação) | etiqueta, MAC |
| gateway | concentrador |
| nó sensor | nó final, dispositivo final, end device |
| payload | carga útil |
| quadro | frame |
| dataset | conjunto de dados, base |
| cifragem, decifragem | criptografia (como verbo), encriptação, decriptação |
| chave de sessão | session key |
| tempo no ar | airtime, ToA |

Termo estrangeiro vai em `\textit{}` em todas as ocorrências. Siglas aparecem por extenso
na primeira ocorrência de cada capítulo e constam na lista de siglas do `main.tex` uma
única vez.

### 8. Convenções de forma

- Legenda de tabela, quadro e figura. `\caption{...}` sempre acima, nos três casos, e a fonte
  abaixo, com `\legend{Fonte: elaborado pelos autores}` ou `\legend{Fonte: \cite{chave}}`.
  "elaborado" em minúscula.
- Tabela é para dado numérico. Quando o conteúdo é só texto, usar o ambiente `quadro`.
- Rótulos com prefixo. `fig:`, `tab:`, `qua:`, `sec:`, `subsec:`, `cap:`, `eq:`. Sem rótulos soltos
  como `messages_abc`.
- Referências cruzadas sempre com `\ref` ou `\autoref`, nunca número digitado.
- Citação com `\cite{chave}` entre parênteses no fim da frase. `\citeonline` só quando o
  autor é sujeito da frase.
- Números com vírgula decimal e separador de milhar com ponto, unidade com `~` antes
  (`87~ms`, `51~bytes`).
- Pontuação em prosa. Não usar ponto e vírgula, dois pontos nem travessão no corpo do
  texto. Frase longa vira duas frases. Lista em prosa usa vírgulas e "e". As únicas
  exceções são `\legend{Fonte:` e ambientes de código.
- Nada de texto de planejamento interno no `.tex`. Cronograma, "marcos", "a combinar" e
  comentários para o grupo ficam fora do documento.
- Não mencionar testes feitos no computador do autor quando o que vale é o teste na placa.

## Revisão de um capítulo

Lista de verificação manual, depois do script.

- [ ] As frentes aparecem na ordem infra, segurança, ML, no mesmo nível de título.
- [ ] Cada seção de frente abre com o parágrafo de ligação e cita as seções das outras.
- [ ] Tempo verbal do capítulo respeitado, sem promessa fora do Cap6.
- [ ] Nenhum identificador de requisito sem prefixo de frente ou repetido.
- [ ] Seções de resultado fecham com requisitos atendidos e "Limitações".
- [ ] Um termo por conceito, estrangeirismo em itálico.
- [ ] Toda tabela, quadro e figura tem `\caption` acima, `\legend{Fonte:` abaixo e rótulo com prefixo.
- [ ] Nenhuma subseção duplicada no capítulo.
- [ ] Nenhum título com "Preliminares", "Previstas", "Propostas".
- [ ] Cap1 e Cap6, se tocados, continuam espelhados.

Ao relatar, agrupar por tipo de problema e dar `Arquivo.tex:linha`. Uma frase por item.
Sugerir a frase corrigida só quando o problema for de forma. Quando for de conteúdo
(ligação ausente, limitação não declarada), apontar e deixar o autor escrever.

## Checagem automática

```bash
python3 .claude/skills/tcc-escrita/scripts/checar.py                     # tudo
python3 .claude/skills/tcc-escrita/scripts/checar.py --autor felipe      # só uma pasta
python3 .claude/skills/tcc-escrita/scripts/checar.py --cap 5             # só um capítulo
python3 .claude/skills/tcc-escrita/scripts/checar.py --sem-pontuacao     # só as demais checagens
```

O script lê os esqueletos em `capitulos/`, os fragmentos de cada autor, o `main.tex` e
todos os `.bib`, e reporta.

- `\input` das frentes fora da ordem infra, segurança, ML nos esqueletos.

- Chaves de `\cite` que não existem no `.bib`.
- `\ref` e `\autoref` sem `\label` correspondente, e rótulos que ninguém referencia.
- Rótulos sem prefixo conhecido.
- Títulos de seção ou subseção repetidos dentro do mesmo capítulo.
- Identificadores RF e RNF sem prefixo de frente ou definidos em mais de uma seção do Cap4.
- Linguagem de planejamento fora do Cap6 e títulos com "Preliminares", "Previstas", "Propostas".
- Ponto e vírgula, dois pontos e travessão em linhas de prosa.
- Tabelas e figuras sem `\legend{Fonte:`.

O script só lê. Ele não altera arquivo nenhum. Ele também não compila o LaTeX, e a
compilação com `latexmk`, local ou pela Action, continua sendo a verificação final.

## O que este guia não faz

- Não decide conteúdo técnico de nenhuma frente.
- Não substitui a leitura do orientador.
