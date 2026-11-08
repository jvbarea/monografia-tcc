# Compilação com pdflatex + bibtex (o abntex2cite usa bibtex com abntex2-alf.bst).
# Uso local: latexmk        (gera main.pdf)
#            latexmk -C     (limpa auxiliares e PDF)
$pdf_mode = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode -file-line-error -synctex=1 %O %S';
$bibtex_use = 2;
@default_files = ('main.tex');
$clean_ext = 'synctex.gz run.xml bbl';
