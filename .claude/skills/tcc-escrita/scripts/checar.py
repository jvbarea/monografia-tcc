#!/usr/bin/env python3
"""Checagem de forma dos capítulos .tex da monografia.

Uso, na raiz do repositório da monografia:
    python3 .claude/skills/tcc-escrita/scripts/checar.py [RAIZ] [--autor PASTA] [--cap N] [--sem-pontuacao]

Entende as duas organizações: uma pasta por autor (capitulos/CapN-*.tex com
\input de <autor>/capN-*.tex) e a antiga, com os CapN-*.tex soltos na raiz.
Só lê os arquivos. Não altera nada e não compila LaTeX.
"""
import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

PREFIXOS_LABEL = ("fig:", "tab:", "sec:", "subsec:", "subsubsec:", "cap:", "eq:", "qua:")
PLANEJAMENTO = re.compile(
    r"\b(ser[áa]o?\s+(realizad|implementad|incorporad|avaliad|validad|medid|testad|feit)|"
    r"pretende-se|pretendemos|planeja-se|planejamos|futuramente|em\s+etapa\s+futura|"
    r"ainda\s+n[ãa]o\s+(foi|foram)|a\s+ser\s+(realizad|definid|implementad)|"
    r"dever[áa]o?\s+ser|est[áa]\s+previst[oa]|prev[êe]-se|cronograma|marcos?\s+do\s+projeto)",
    re.IGNORECASE,
)
LINHA_NAO_PROSA = re.compile(
    r"^\s*(\\(begin|end|legend|includegraphics|input|include|usepackage|newcommand|"
    r"bibliography|hline|toprule|midrule|bottomrule|cline|centering|item\s*$))|&|\\\\\s*$"
)
COMANDOS_SEM_PROSA = re.compile(
    r"\\(label|ref|autoref|cite|citeonline|url|href|texttt|verb|includegraphics|"
    r"chapter|section|subsection|subsubsection)\*?\{[^}]*\}|\$[^$]*\$"
)
NOME_SINAL = {";": "ponto e vírgula", ":": "dois pontos", "\u2014": "travessão", "\u2013": "travessão", "--": "travessão"}
TITULO = re.compile(r"\\(chapter|section|subsection|subsubsection)\*?\{")
# Ordem das frentes em todo capítulo: infraestrutura, segurança, ML.
ORDEM_FRENTES = ["barea", "felipe", "tadaki"]
IGNORAR_PASTAS = {"capitulos", ".git", ".github", ".claude", ".vscode"}
REQ = re.compile(r"\b(RNF|RF)(?:-([ISM]))?\s?(\d+)\b")


def strip_comment(line: str) -> str:
    out, prev = [], ""
    for ch in line:
        if ch == "%" and prev != "\\":
            break
        out.append(ch)
        prev = ch
    return "".join(out)


def titulo(line: str):
    """Devolve (nível, texto) do título na linha, respeitando chaves aninhadas."""
    m = TITULO.search(line)
    if not m:
        return None
    depth, start = 1, m.end()
    for i in range(start, len(line)):
        if line[i] == "{" and line[i - 1] != "\\":
            depth += 1
        elif line[i] == "}" and line[i - 1] != "\\":
            depth -= 1
            if depth == 0:
                return m.group(1), line[start:i]
    return m.group(1), line[start:]


def titulo_limpo(t: str) -> str:
    t = re.sub(r"\\label\{[^}]*\}", "", t)
    t = re.sub(r"\\textit\{([^}]*)\}", r"\1", t)
    return re.sub(r"\s+", " ", t).strip().lower()


def num_cap(path: Path):
    m = re.match(r"[Cc]ap(\d)", path.name)
    return int(m.group(1)) if m else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("raiz", nargs="?", default=".")
    ap.add_argument("--autor", help="relatar só os arquivos desta pasta (ex.: felipe)")
    ap.add_argument("--cap", help="relatar só este capítulo (ex.: 5 ou Cap5)")
    ap.add_argument("--sem-pontuacao", action="store_true")
    args = ap.parse_args()

    raiz = Path(args.raiz)
    rel = lambda f: str(f.relative_to(raiz))
    esqueletos = sorted((raiz / "capitulos").glob("Cap*.tex")) if (raiz / "capitulos").is_dir() else []
    if esqueletos:
        fragmentos = sorted(
            f for d in raiz.iterdir() if d.is_dir() and d.name not in IGNORAR_PASTAS
            for f in d.glob("cap[0-9]*.tex")
        )
        todos_caps = esqueletos + fragmentos
    else:
        todos_caps = sorted(raiz.glob("Cap*.tex"))
    if not todos_caps:
        print(f"nenhum capítulo .tex encontrado em {raiz}", file=sys.stderr)
        return 2

    caps = todos_caps
    if args.autor:
        caps = [f for f in caps if f.parent.name == args.autor]
    if args.cap:
        n_cap = int(re.sub(r"\D", "", args.cap))
        caps = [f for f in caps if num_cap(f) == n_cap]
    if not caps:
        print("nenhum arquivo corresponde ao filtro", file=sys.stderr)
        return 2
    relatados = {rel(f) for f in caps}

    bib_keys = set()
    for b in raiz.rglob("*.bib"):
        if ".git" in b.parts:
            continue
        bib_keys |= set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", b.read_text(errors="replace")))

    # Labels e refs de todos os arquivos, para referências cruzadas entre capítulos e frentes.
    labels, refs = {}, defaultdict(list)
    for f in todos_caps + sorted(raiz.glob("main.tex")):
        for n, raw in enumerate(f.read_text(errors="replace").splitlines(), 1):
            line = strip_comment(raw)
            for lab in re.findall(r"\\label\{([^}]*)\}", line):
                labels.setdefault(lab, (rel(f), n))
            for r in re.findall(r"\\(?:auto)?ref\{([^}]*)\}", line):
                for one in r.split(","):
                    refs[one.strip()].append((rel(f), n))

    problemas = defaultdict(list)
    titulos_vistos = defaultdict(list)   # (capítulo, nível, título) -> [arquivo:linha]
    req_por_secao = defaultdict(set)     # id -> {arquivo: seção}

    # Ordem das frentes nos esqueletos dos capítulos.
    for f in esqueletos:
        if args.cap and num_cap(f) != int(re.sub(r"\D", "", args.cap)):
            continue
        vistos, anterior = set(), None
        for n, raw in enumerate(f.read_text(errors="replace").splitlines(), 1):
            m = re.search(r"\\input\{([^/}]+)/", strip_comment(raw))
            if not m or m.group(1) not in ORDEM_FRENTES:
                continue
            atual = m.group(1)
            if anterior and ORDEM_FRENTES.index(atual) < ORDEM_FRENTES.index(anterior):
                recomeco = atual == ORDEM_FRENTES[0] and atual in vistos
                if not recomeco:
                    problemas["frentes fora da ordem infra, segurança, ML"].append(
                        f"{rel(f)}:{n} {atual} depois de {anterior}")
            vistos.add(atual)
            anterior = atual

    for f in todos_caps:
        nome = rel(f)
        relatar = nome in relatados
        cap = num_cap(f)
        secao_atual = "(início)"
        em_float, float_tem_fonte, float_inicio = None, False, 0
        em_verbatim = False

        for n, raw in enumerate(f.read_text(errors="replace").splitlines(), 1):
            line = strip_comment(raw)
            if re.search(r"\\begin\{(verbatim|lstlisting|minted)", line):
                em_verbatim = True
            if re.search(r"\\end\{(verbatim|lstlisting|minted)", line):
                em_verbatim = False
                continue
            if em_verbatim:
                continue

            m = titulo(line)
            if m:
                nivel, bruto = m
                t = titulo_limpo(bruto)
                if nivel == "section":
                    secao_atual = t
                if nivel in ("section", "subsection", "subsubsection"):
                    titulos_vistos[(cap, nivel, t)].append((nome, n))
                if relatar and re.search(r"\bpreliminar|\bprevist|\bpropost", t):
                    problemas["título ainda com cara de planejamento"].append(f"{nome}:{n} {bruto}")

            if cap == 4:
                for pref, frente, num in REQ.findall(line):
                    if relatar and not frente:
                        problemas["requisito sem prefixo de frente (RF-I, RF-S, RF-M)"].append(f"{nome}:{n} {pref}{num}")
                    req_por_secao[f"{pref}-{frente}{num}" if frente else f"{pref}{num}"].add(f"{nome}: {secao_atual}")

            if not relatar:
                continue

            for key in re.findall(r"\\cite(?:online)?\{([^}]*)\}", line):
                for k in key.split(","):
                    k = k.strip()
                    if k and k not in bib_keys:
                        problemas["cite sem entrada no .bib"].append(f"{nome}:{n} {k}")

            for lab in re.findall(r"\\label\{([^}]*)\}", line):
                if not lab.startswith(PREFIXOS_LABEL):
                    problemas["label sem prefixo (fig:, tab:, sec:, subsec:, cap:, eq:)"].append(f"{nome}:{n} {lab}")

            if cap != 6 and PLANEJAMENTO.search(line):
                problemas["linguagem de planejamento fora do Cap6"].append(f"{nome}:{n} {line.strip()[:90]}")

            if not args.sem_pontuacao and not LINHA_NAO_PROSA.search(line):
                prosa = COMANDOS_SEM_PROSA.sub("", line)
                for sinal in (";", ":", "\u2014", "\u2013", "--"):
                    if sinal in prosa:
                        problemas[f"'{NOME_SINAL.get(sinal, sinal)}' em prosa"].append(f"{nome}:{n} {line.strip()[:90]}")

            mb = re.search(r"\\begin\{(table|figure|quadro)\*?\}", line)
            if mb:
                em_float, float_tem_fonte, float_inicio = mb.group(1), False, n
            if em_float and "Fonte:" in line:
                float_tem_fonte = True
            if em_float and re.search(rf"\\end\{{{em_float}\*?\}}", line):
                if not float_tem_fonte:
                    problemas["tabela ou figura sem \\legend{Fonte:"].append(f"{nome}:{float_inicio}")
                em_float = None

    for (cap, nivel, t), onde in titulos_vistos.items():
        if len(onde) > 1 and any(a in relatados for a, _ in onde):
            locais = ", ".join(f"{a}:{n}" for a, n in onde)
            problemas["título repetido no mesmo capítulo"].append(f"Cap{cap} {nivel} '{t}' em {locais}")
    for rid, secs in req_por_secao.items():
        if len(secs) > 1 and any(s.split(": ")[0] in relatados for s in secs):
            problemas["requisito definido em mais de uma seção do Cap4"].append(f"{rid} em " + " | ".join(sorted(secs)))

    for r, onde in refs.items():
        if r not in labels:
            aqui = [f"{a}:{n}" for a, n in onde if a in relatados]
            if aqui:
                problemas["ref sem label"].append(f"{', '.join(aqui)} -> {r}")
    for lab, (arq, n) in labels.items():
        if arq in relatados and lab not in refs and not lab.startswith("cap:"):
            problemas["label que ninguém referencia"].append(f"{arq}:{n} {lab}")

    if not problemas:
        print("nenhum problema encontrado")
        return 0
    total = 0
    for tipo, itens in problemas.items():
        print(f"\n## {tipo} ({len(itens)})")
        for it in itens:
            print("  " + it)
        total += len(itens)
    print(f"\n{total} ocorrências em {len(problemas)} categorias")
    return 1


if __name__ == "__main__":
    sys.exit(main())
