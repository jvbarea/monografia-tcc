# Monografia do TCC (LaTeX, abnTeX2)

Fonte da monografia de três autores: João (infraestrutura LoRa), Felipe
(criptografia Ascon) e Celso (detecção por aprendizado de máquina). Este
repositório substituiu o Prism em 08/11/2026. O usuário desta sessão é o João.

Contexto, fatos, números e plano de trabalho ficam no repositório de código:

`C:/Users/joaob/OneDrive/Documentos/2026/TCC/tcc-lora-infra/docs/`:

- `plano-monografia-defesa.md` (tarefas T0.1 a T4.4)
- `diagnostico-monografia-2026-11-08.md` (fatos e números)
- `mapa-alteracoes-prism.md` (cada alteração, por lote)

## Regras

- **Só a parte do João**, salvo pedido explícito: seções de LoRa e LoRaWAN
  (Cap. 2, 2.1), arquitetura (Cap. 3, 3.1), requisitos e rastreabilidade da
  infraestrutura (Cap. 4, 4.1), implementação e resultados da infraestrutura
  (Cap. 5, 5.1.1, 5.1.4, 5.2) e os parágrafos de infraestrutura do Cap. 1 e
  do Cap. 6. Texto do Felipe e do Celso: apontar o problema, não editar.
- **Melhorar, não substituir.** Manter a voz e a estrutura do que existe;
  trocar o parágrafo inteiro só quando o fato mudou.
- **Nada inexistente.** Toda `\cite` com entrada verificada no `.bib`
  (criar a entrada junto, com URL e data de acesso conferidas); toda `\ref`
  com `\label`; toda figura em `figuras/`. Se a fonte não existe, não citar.
- **Sem travessão** (`--`, `---`, "—"). Vírgula, dois pontos ou ponto.
- **Números** vêm do diagnóstico ou dos arquivos de dados do
  `tcc-lora-infra`; não inventar nem arredondar além do que a fonte dá.
- **Pergunta não altera arquivo.** Dúvida do usuário: ler e responder;
  oferecer a mudança no fim.
- Não usar custo como justificativa do enlace ponto a ponto.
- Commit só quando o usuário pedir; mensagem curta em português dizendo
  capítulo, seção e o que mudou.

## Compilação

Sem LaTeX local (08/11/2026). A Action `Compilar PDF` roda a cada push e
publica `main.pdf` e `main.log` como artefato. Local: MiKTeX + `latexmk`
(`.latexmkrc` já configurado). Classe e `.bst` estão versionados.

## Impactos a sinalizar

Ao mudar algo da infraestrutura, dizer se afeta texto dos colegas (por
exemplo: tempo no ar de 61,7 ms contra "87 ms" no texto do Felipe; teto de
29 B de aplicação; coletas de 08/10 e 12 a 13/10 como execução da biblioteca
nas placas).
