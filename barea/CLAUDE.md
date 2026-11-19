# Pasta do João Barea: infraestrutura LoRa

Vale junto com o `CLAUDE.md` da raiz. Aqui ficam os fragmentos da frente de
infraestrutura (nó sensor, gateway, backend, coletas), as figuras e a
bibliografia que só esta frente cita.

| Arquivo | Entra em |
|---|---|
| `cap2-lora-lorawan.tex` | Cap. 2, §2.1 Redes IoT e o protocolo LoRaWAN |
| `cap3-arquitetura.tex` | Cap. 3, §3.1 Procedimento de definição da arquitetura |
| `cap4-requisitos-infra.tex` | Cap. 4, §4.1 Requisitos e rastreabilidade da infraestrutura |
| `cap5-implementacao-infra.tex` | Cap. 5, §5.1.1 Implementação da infraestrutura |
| `cap5-integracao.tex` | Cap. 5, §5.1.4 Integração progressiva |
| `cap5-resultados-infra.tex` | Cap. 5, §5.2 Resultados da infraestrutura |
| `cap6-conclusoes-infra.tex` | Cap. 6, conclusões da infraestrutura, antes das de segurança |
| `cap6-perspectivas-infra.tex` | Cap. 6, §6.1, entre as perspectivas de detecção e as de segurança |
| `refs.bib` | entradas citadas só aqui |
| `figuras/` | figuras destas seções |

Parágrafos de infraestrutura do Cap. 1 ficam no arquivo do grupo em
`capitulos/`; avisar os outros antes de mexer. O método da infraestrutura
(bancada, métricas e os sete marcos) está em §3.1.3, no fim de
`cap3-arquitetura.tex`.

## Fontes dos fatos e números

Repositório de código e dados:
`C:\Users\joaob\OneDrive\Documentos\2026\TCC\tcc-lora-infra`
(github.com/jvbarea/tcc-lora-infra). Em `docs/`:

- `plano-monografia-defesa.md`: tarefas T0.1 a T4.4 e calendário até 18/12.
- `diagnostico-monografia-2026-11-08.md`: fatos corretos e números de
  referência (seções 4 e 6), com a fonte de cada um.
- `mapa-alteracoes-prism.md`: cada alteração pendente, por lote, com
  arquivo, parágrafo e o que o texto novo diz.

Dados: `data/*.csv`, `analise/*-metricas.txt`, `tools/time_on_air.py`.

## Regras desta frente

- Números só do diagnóstico ou dos arquivos de dados; nada de memória.
- Não usar custo como justificativa do enlace ponto a ponto. A justificativa
  é o banco de ensaio (sem gateway multicanal nem servidor de rede) e o
  controle das duas pontas.
- Introdução diz o quê e por quê; Cap. 3 só o método essencial; números,
  implementação e cronologia no Cap. 5.
- Ao mudar um fato compartilhado (tamanho do quadro, tempo no ar, FCnt,
  metadados), listar no PR o que afeta `felipe/` e `tadaki/`.
- Secretos do firmware (`wifi_secrets.h`, `node_keys.h`, chaves) nunca
  entram no texto.
