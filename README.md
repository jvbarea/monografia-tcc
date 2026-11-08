# Monografia do TCC

Fonte LaTeX (abnTeX2) da monografia. Substitui o projeto do Prism a partir de
08/11/2026; o Prism fica como leitura até sair de circulação em janeiro de
2027. **Depois desta data, só este repositório vale.**

Trabalho de conclusão de curso sobre detecção de anomalias e criptografia
leve em redes LoRaWAN, em três frentes: infraestrutura de comunicação (João),
camada criptográfica Ascon (Felipe) e detecção por aprendizado de máquina
(Celso). Código e dados da infraestrutura:
[tcc-lora-infra](https://github.com/jvbarea/tcc-lora-infra).

## Arquivos

| Arquivo | Conteúdo | Quem edita |
|---|---|---|
| `main.tex` | Capa, folha de rosto, resumo, siglas, inclusão dos capítulos, bibliografia | grupo |
| `Cap1-Intro.tex` | Introdução, motivação, objetivos | grupo |
| `Cap2-Conceitos.tex` | LoRa e LoRaWAN (João), criptografia leve (Felipe), aprendizado de máquina (Celso) | por seção |
| `Cap3-Metodo.tex` | Arquitetura (João), datasets e modelos (Celso), biblioteca e testes do Ascon (Felipe) | por seção |
| `Cap4-Especificacao.tex` | Requisitos da infraestrutura (João), da detecção (Celso), de segurança (Felipe) | por seção |
| `Cap5-Desenvolvimento.tex` | Implementação e resultados das três frentes | por seção |
| `Cap6-Consideracoes.tex` | Considerações finais e trabalhos futuros | grupo |
| `abntex2-modelo-references.bib` | Bibliografia | quem cita |
| `figuras/` | Figuras em PNG | quem usa |
| `abntex2*.cls`, `*.sty`, `*.bst` | Classe abnTeX2, versionada junto para compilar igual em qualquer máquina | ninguém |
| `ficha.pdf` | Ficha catalográfica provisória | grupo, após a defesa |

## Como compilar

**Sem instalar nada.** Cada push dispara a Action "Compilar PDF". O PDF fica
em *Actions > execução > Artifacts*. Se a compilação falhar, o `main.log`
está no mesmo artefato.

**Na própria máquina (Windows).** Instalar o MiKTeX
(`winget install MiKTeX.MiKTeX`), deixar o MiKTeX instalar pacotes
faltantes automaticamente na primeira compilação, e rodar na pasta do
repositório:

```powershell
latexmk          # gera main.pdf
latexmk -C       # limpa auxiliares e PDF
```

O `.latexmkrc` já configura pdflatex e bibtex. A primeira compilação demora
porque o MiKTeX baixa pacotes; as seguintes levam menos de um minuto.

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
