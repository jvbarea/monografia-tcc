# Monografia do TCC (LaTeX, abnTeX2)

Fonte da monografia de três autores. Cada um é dono de uma frente e do texto
dela; o Claude de cada um edita só a parte do seu usuário, salvo pedido
explícito.

| Autor | Frente | Pasta | Seções |
|---|---|---|---|
| João Barea (`barea`) | infraestrutura LoRa: nó, gateway, backend, coletas | `barea/` | Cap. 2 §2.1; Cap. 3 §3.1; Cap. 4 §4.1; Cap. 5 §5.1.1, §5.1.4, §5.2; Cap. 6 parágrafos de infraestrutura |
| Felipe Korbes (`felipe`) | criptografia leve, Ascon, biblioteca AsconSecure | `felipe/` | Cap. 2 §2.2; Cap. 3 §3.2.5 e §3.3; Cap. 4 §4.2; Cap. 5 §5.1.2, §5.3; Cap. 6 parágrafos de segurança |
| Celso Tadaki (`tadaki`) | detecção de anomalias por aprendizado de máquina | `tadaki/` | Cap. 2 §2.3; Cap. 3 §3.2.1 a §3.2.4; Cap. 4 §4.3; Cap. 5 §5.1.3; Cap. 6 §6.1 perspectivas |
| Grupo | | `main.tex`, `capitulos/` | Cap. 1 inteiro; esqueletos dos capítulos (título, parágrafos de abertura, `\input`); Cap. 6 parágrafos 1 e 2; `refs-comuns.bib` |

Cada capítulo em `capitulos/` é um esqueleto que faz `\input` dos fragmentos
de cada autor, na ordem das seções. Figuras em `<autor>/figuras/`.
Bibliografia: `<autor>/refs.bib` para o que só aquela frente cita;
`capitulos/refs-comuns.bib` para o que mais de uma frente ou o grupo cita.
Chave citada por duas frentes vai para a comum (bibtex avisa "repeated
entry" se ficar em dois arquivos).

**Descubra quem é o usuário** antes de editar: `git config user.name`, ou
pergunte. Regras próprias de cada autor ficam no `CLAUDE.md` da sua pasta.

## Regras comuns

- **Só a parte do usuário.** Problema no texto de outro autor: apontar
  (arquivo, seção, o que está errado), não editar. Arquivos do grupo: avisar
  os outros dois antes de mexer.
- **Melhorar, não substituir.** Manter a voz e a estrutura do que existe;
  trocar um parágrafo inteiro só quando o fato mudou.
- **Nada inexistente.** Toda `\cite` com entrada no `.bib`, criada junto e
  conferida (URL, data de acesso, autores); toda `\ref` com `\label`; toda
  figura presente em `figuras/`. Se a fonte não existe, não citar.
- **Padrão de escrita na skill `tcc-escrita`.** Ordem das frentes, tempo
  verbal, numeração de requisitos, termos, legendas e pontuação estão em
  `.claude/skills/tcc-escrita/SKILL.md`, e valem para os três autores.
  Carregar a skill antes de escrever ou revisar texto e rodar
  `python3 .claude/skills/tcc-escrita/scripts/checar.py --autor <pasta>` antes
  do pull request. Regra de escrita nova entra na skill, não neste arquivo nem
  no `CLAUDE.md` das pastas, para não haver duas versões.
- **Números** vêm dos dados e documentos de cada frente, com a fonte
  anotada; não inventar nem arredondar além do que a fonte dá.
- **Pergunta não altera arquivo.** Dúvida do usuário: ler e responder;
  oferecer a mudança no fim.
- **Interfaces entre frentes** são fatos compartilhados; ao mudar um,
  sinalizar aos outros: quadro de 26 B com teto de 29 B de aplicação; tempo
  no ar de 61,7 ms em SF7; contador da biblioteca Ascon é o FCnt do log;
  os 12 metadados de recepção são as variáveis candidatas dos modelos; as
  coletas de 08/10 e 12 a 13/10/2026 são a execução da biblioteca nas
  placas.
- **Commit só quando o usuário pedir.** Mensagem curta em português com
  capítulo, seção e o que mudou. Um branch por alteração
  (`barea/cap5-resultados`), pull request para `main`, merge depois que a
  Action passa.

## Compilação

Local: MiKTeX + Strawberry Perl + `latexmk` (`.latexmkrc` já configurado).
Na raiz: `latexmk -pdf -interaction=nonstopmode main.tex`, cerca de 20 s
incremental. Conferir no `main.log` as linhas `Output written` (páginas) e
`undefined` (citações e referências quebradas). A Action `Compilar PDF`
roda a cada push e publica `main.pdf` e `main.log` como artefato. Classe
abnTeX2 e `.bst` estão versionados: não instalar outra versão.

Antes de abrir um pull request: compilar, zero `undefined` novos, número de
páginas coerente com a mudança.
