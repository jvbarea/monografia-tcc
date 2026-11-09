# Guia de instalação (Windows)

Passo a passo para compilar e editar a monografia na própria máquina. Leva
uns 20 minutos, a maior parte em downloads. Depois disso, a compilação
incremental leva cerca de 20 segundos.

Se preferir não instalar nada: edite no VS Code, faça push, e baixe o PDF
gerado pela Action em *GitHub > Actions > execução mais recente >
Artifacts*. Tudo o que está abaixo é opcional para esse caminho, exceto o
passo 1.

## 1. Git e acesso ao repositório

1. Aceite o convite do repositório `jvbarea/monografia-tcc` (chega por
   e-mail do GitHub).
2. Instale o Git, se ainda não tiver:
   ```powershell
   winget install Git.Git
   ```
3. Configure nome e e-mail (aparecem nos commits):
   ```powershell
   git config --global user.name "Seu Nome"
   git config --global user.email "seu@email"
   ```
4. Clone **fora do OneDrive, Google Drive ou Dropbox**. Esses serviços
   sincronizam arquivos abertos e brigam com o Git e com o LaTeX.
   ```powershell
   mkdir C:\dev
   cd C:\dev
   git clone https://github.com/jvbarea/monografia-tcc.git
   ```

## 2. MiKTeX e Perl

O MiKTeX é a distribuição LaTeX. O `latexmk`, que a extensão do VS Code usa
para compilar na ordem certa (pdflatex, bibtex, pdflatex, pdflatex), é um
script Perl, e o MiKTeX não traz Perl.

```powershell
winget install MiKTeX.MiKTeX
winget install StrawberryPerl.StrawberryPerl
```

Feche e abra o terminal (o PATH só atualiza em terminal novo) e ligue a
instalação automática de pacotes, para o MiKTeX baixar sozinho o que
faltar na primeira compilação:

```powershell
initexmf --set-config-value "[MPM]AutoInstall=1"
```

Primeira compilação, na pasta do repositório:

```powershell
cd C:\dev\monografia-tcc
latexmk
```

Demora uns 3 minutos baixando pacotes. Termina com
`Output written on main.pdf (107 pages` no fim do `main.log`. Se aparecer
`MiKTeX could not find the script engine 'perl'`, o Perl não está no PATH:
abra outro terminal ou reinicie a máquina.

Para limpar os arquivos gerados: `latexmk -C`.

## 3. VS Code

1. Instale o VS Code, se ainda não tiver: `winget install Microsoft.VisualStudioCode`.
2. Abra a pasta `C:\dev\monografia-tcc` (*File > Open Folder*).
3. O VS Code vai sugerir instalar a extensão **LaTeX Workshop**
   (recomendação em `.vscode/extensions.json`). Aceite. Se não sugerir,
   procure `James-Yu.latex-workshop` em *Extensions*.
4. Reinicie o VS Code depois de instalar o MiKTeX e o Perl, para a
   extensão enxergar os dois.

As configurações da extensão já vêm no repositório
(`.vscode/settings.json`): compilar ao salvar com `latexmk`, PDF em uma aba
ao lado, fim de linha LF.

Atalhos:

| Ação | Atalho |
|---|---|
| Compilar | `Ctrl+Alt+B` (ou salvar qualquer `.tex`) |
| Abrir o PDF ao lado | `Ctrl+Alt+V` |
| Do PDF para a linha do `.tex` | `Ctrl+clique` no PDF |
| Do `.tex` para o PDF | `Ctrl+Alt+J` |
| Ver erros e avisos | painel *Problems* (`Ctrl+Shift+M`) |

Citação sem entrada no `.bib` e `\ref` sem `\label` aparecem em *Problems*
como *undefined*. Não deixe nenhum novo.

## 4. Onde cada um edita

| Pasta | Autor |
|---|---|
| `barea/` | João (infraestrutura LoRa) |
| `felipe/` | Felipe (criptografia leve, Ascon) |
| `tadaki/` | Celso (detecção por aprendizado de máquina) |
| `capitulos/`, `main.tex` | grupo: avisar antes de mexer |

Dentro da sua pasta: um arquivo por seção (`capN-nome.tex`), `figuras/` e
`refs.bib`. Os arquivos em `capitulos/` só fazem `\input` dos seus. Para
acrescentar uma seção, crie o arquivo e uma linha `\input{sua-pasta/arquivo}`
no esqueleto do capítulo. Detalhes no `README.md`.

## 5. Fluxo de trabalho

```powershell
git checkout main
git pull
git checkout -b felipe/cap5-energia        # um branch por alteração
# ... editar, compilar, conferir o PDF ...
git add felipe/
git commit -m "Cap. 5, 5.3.4: acrescenta medição de energia do ESP32-S3"
git push -u origin felipe/cap5-energia
```

Depois, no GitHub, *Compare & pull request*. A Action compila o PDF; quando
ficar verde, quem abriu dá o merge. Mudanças de uma linha podem ir direto em
`main`, com `git pull` antes.

Regras do texto: só citar o que existe no `.bib`; sem travessão
(`--`, `---`, "—"); figuras em PNG na sua pasta `figuras/`. Tudo isso está
no `README.md` e no `CLAUDE.md`.

## 6. Claude Code (opcional)

Quem usa Claude Code abre a pasta do repositório. O `CLAUDE.md` da raiz tem
as regras comuns; cada autor pode criar um `CLAUDE.md` na própria pasta com
as regras e as fontes da sua frente (o de `barea/` serve de exemplo). O
Claude lê os dois quando trabalha dentro da pasta.

## Problemas conhecidos

| Sintoma | Causa e solução |
|---|---|
| `script engine 'perl' not found` | Perl não instalado ou terminal antigo. Instalar o Strawberry Perl e abrir terminal novo. |
| `you have not checked for MiKTeX updates` | Só aviso. Abrir o *MiKTeX Console* e clicar em *Check for updates* uma vez. |
| Pacote faltando (`File xxx.sty not found`) | `AutoInstall` desligado. Rodar o `initexmf` do passo 2 ou ligar em *MiKTeX Console > Settings*. |
| PDF não atualiza no VS Code | PDF aberto em outro programa travando o arquivo. Fechar e compilar de novo. |
| `repeated entry` do bibtex | A mesma chave está em dois `.bib`. Deixar só em `capitulos/refs-comuns.bib`. |
| Diff gigante com todas as linhas mudadas | Fim de linha CRLF. O `.gitattributes` força LF; rodar `git add --renormalize .` |

## macOS e Linux

Mesmo fluxo, trocando o passo 2 por TeX Live (`brew install --cask mactex`
ou `sudo apt install texlive-full latexmk`). Perl já vem no sistema.
