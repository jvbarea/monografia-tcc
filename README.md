# Monografia do TCC

Fonte LaTeX (abnTeX2) da monografia. Substitui o projeto do Prism a partir de
08/11/2026; o Prism fica como leitura até sair de circulação em janeiro de
2027. **Depois desta data, só este repositório vale.**

Trabalho de conclusão de curso sobre detecção de anomalias e criptografia
leve em redes LoRaWAN, em três frentes: infraestrutura de comunicação (João),
camada criptográfica Ascon (Felipe) e detecção por aprendizado de máquina
(Celso). Código e dados da infraestrutura:
[tcc-lora-infra](https://github.com/jvbarea/tcc-lora-infra).

## Estrutura

Uma pasta por autor. Cada capítulo em `capitulos/` é um esqueleto (título,
parágrafos de abertura) que faz `\input` dos fragmentos de cada autor, na
ordem das seções. Assim cada um edita só a própria pasta e os conflitos de
merge ficam restritos aos arquivos do grupo.

```
main.tex                  capa, resumo, siglas, inclusão dos capítulos      grupo
capitulos/Cap1-Intro.tex  introdução inteira                                 grupo
capitulos/Cap2..Cap6.tex  esqueletos com \input                              grupo
capitulos/refs-comuns.bib entradas citadas por mais de uma frente            quem cita
barea/                    infraestrutura LoRa (João)                         João
felipe/                   criptografia leve e Ascon (Felipe)                 Felipe
tadaki/                   detecção por aprendizado de máquina (Celso)        Celso
<autor>/capN-*.tex        fragmentos, um por seção                           autor
<autor>/refs.bib          entradas citadas só por esta frente                autor
<autor>/figuras/          figuras das seções do autor                        autor
<autor>/CLAUDE.md         regras e fontes da frente, para o Claude do autor  autor
abntex2*, *.bst           classe abnTeX2, versionada para compilar igual     ninguém
ficha.pdf                 ficha catalográfica provisória                     grupo, após a defesa
```

Para acrescentar uma seção nova: criar `<autor>/capN-nome.tex` e uma linha
`\input{<autor>/capN-nome}` no esqueleto do capítulo, no lugar certo. Para
citar: a entrada vai no `refs.bib` da própria pasta; se outra frente já cita
a mesma chave, ela vai para `capitulos/refs-comuns.bib` (o bibtex avisa
"repeated entry" se ficar nos dois). Figura nova: `<autor>/figuras/`, com o
caminho completo no `\includegraphics`.

A divisão foi feita em 08/11/2026 por corte nas fronteiras de seção; o PDF
antes e depois tem as 107 páginas com o mesmo texto, sumário, listas e
bibliografia.

## Como compilar

Instalação passo a passo (Git, MiKTeX, Perl, VS Code, fluxo): **[SETUP.md](SETUP.md)**.

**Sem instalar nada.** Cada push dispara a Action "Compilar PDF". O PDF fica
em *Actions > execução > Artifacts*. Se a compilação falhar, o `main.log`
está no mesmo artefato.

**Na própria máquina (Windows).** O `latexmk` é um script Perl e o MiKTeX
não traz Perl, então são dois pacotes:

```powershell
winget install MiKTeX.MiKTeX
winget install StrawberryPerl.StrawberryPerl
```

Depois, ligar a instalação automática de pacotes e compilar na pasta do
repositório (abrir um terminal novo para o PATH atualizar):

```powershell
initexmf --set-config-value "[MPM]AutoInstall=1"
latexmk          # gera main.pdf
latexmk -C       # limpa auxiliares e PDF
```

O `.latexmkrc` já configura pdflatex e bibtex. A primeira compilação leva
uns 3 minutos porque o MiKTeX baixa pacotes; as seguintes, cerca de 20 s.

**No VS Code.** Extensão LaTeX Workshop (`James-Yu.latex-workshop`), com os
dois pacotes acima instalados. `Ctrl+Alt+B` compila, `Ctrl+Alt+V` abre o PDF
ao lado, `Ctrl+clique` no PDF vai para a linha do `.tex`. Reiniciar o VS
Code depois de instalar o Perl, para a extensão enxergar o PATH novo.

## Como trabalhar

- **Um branch por alteração**, com nome curto (`joao/cap5-resultados`,
  `felipe/cap6-futuro`), e pull request para `main`. Quem abriu o PR faz o
  merge depois que a Action passa. Mudanças de uma linha podem ir direto em
  `main`.
- **Cada um edita a própria seção.** O Cap. 1, o Cap. 6 e o `main.tex` são
  do grupo: avisar antes de mexer.
- **Compilar antes de dar merge.** A Action faz isso; se ficar vermelha, o
  `main.log` diz a linha.
- **Só citar o que existe.** Toda `\cite` precisa de entrada no `.bib`; toda
  `\ref` precisa de `\label`; toda figura precisa estar em `figuras/`.
- **Sem travessão** no texto (nem `--`, nem `---`). Usar vírgula, dois
  pontos ou ponto.
- **Figuras** com nome que diga o conteúdo (`cadencia_coletas.png`), em PNG,
  sem versões duplicadas.
- **Commits** curtos em português dizendo o que mudou e onde:
  `Cap. 5, 5.2: acrescenta coletas de 08/10 e 12 a 13/10`.

## Histórico

- 08/11/2026: primeiro commit com a cópia do Prism desta data.
