from pathlib import Path

import pandas as pd
from great_tables import GT, md, loc, style

from formata import formatar_atributos_serie, formatar_atributos_df


def formatar_2H3b(gt: GT) -> GT:
    gt = gt.cols_move("DT", after="NPS")
    for label, cols in {
        "DIA": ["PRI", "SEC"],
        "DS": ["DS", "SUBV", "LOC"],
        "PRE": ["DIM"],
        "EC1": ["RA", "ED", "sd"],
        "NPS": ["NPS"],
        "aPRE": ["aSUBV", "aNP"],
    }.items():
        gt = gt.tab_spanner(label, columns=cols)
    return gt

def colorir_gt(gt: GT) -> GT:
    return gt.data_color(
        palette=["white", "#0f5132"],
        domain=[0, 100],
        na_color="white",
    )


def formatar_2H2d(gt: GT) -> GT:
    for label, cols in [(l, [f"{l}-proto", f"{l}-var"]) for l in "VWXYZvwxyz"]:
        gt = gt.tab_spanner(label, columns=cols)
    gt = gt.cols_label(**{f"{l}-proto": "p" for l in "VWXYZvwxyz"})
    gt = gt.cols_label(**{f"{l}-var": "v" for l in "VWXYZvwxyz"})
    return gt


def formatar_2H3e(gt: GT) -> GT:
    order = []
    rbfs = ["DIA|DIA", "DIA|CR", "CR|DIA", "CR|CR"]
    for rel in rbfs:
        order += [f"{rel}-unique-count", f"{rel}-dist"]
    for x in order:
        gt = gt.cols_move_to_end(x)
    for label, cols in [(l, [f"{l}-unique-count", f"{l}-dist"]) for l in rbfs]:
        gt = gt.tab_spanner(label, columns=cols)
    gt = gt.fmt_percent(columns=[f"{l}-dist" for l in rbfs])
    gt = gt.cols_label(**{f"{l}-unique-count": "n" for l in rbfs})
    gt = gt.cols_label(**{f"{l}-dist": "p" for l in rbfs})
    return gt


def formatar_1M(gt: GT) -> GT:
    gt = gt.tab_spanner("1M1a", ["1M1a (maior)", "1M1a (menor)"])
    gt = gt.cols_label(**{"1M1a (maior)": "maior", "1M1a (menor)": "menor"})
    return gt


def formatar_extra(gt: GT) -> GT:
    gt = gt.cols_label(
        **{
            "extra-H1-H": "Acordes",
            "extra-M1-M": "Ataques",
            "extra-M2-M": "Notas-funções",
        }
    )

    return gt


ATRIB_PARA_FORMATADOR_GT = {
    "2H3b": formatar_2H3b,
    "2H2d": formatar_2H2d,
    "2H3e": formatar_2H3e,
    "extra": formatar_extra,
}

ATRIB_COLORIDOS = [
    "2H1b",
    "2H1c",
    "2H2b",
    "2H2c",
    "2H2d",
    "2H3b",
    "2H3c",
    "2H3c-DIA",
    "2H3c-DS",
    "2H3c-SUBV",
    "2H3c-EC1",
    "2H3c-EC2",
    "2M1b",
    "2M1c",
    "2M1d",
    "2M2a",
    "2M2b",
    "2M2c",
    "2M3a",
    "2M3b",
    "2M3c",
]


def exibir_tabela_atributos(
    atributo: str, colunas: list[str] = None, titulo="", subtitulo="", rodape=""
):
    df = pd.read_csv(
        Path(__file__).parents[1] / "resultados" / (atributo + ".csv"), index_col=0
    )
    if colunas:
        df = df[colunas]
    df = formatar_atributos_df(df, atributo)
    df = formatar_atributos_serie(df)
    df = df.reset_index(names="Corpus")
    df = df.assign(group=["Controle"] * 3 + ["MPB"] * (len(df) - 3))
    df = df.reindex(df.index.tolist()[3:] + df.index.tolist()[:3]).reset_index(
        drop=True
    )  # mover corpora de controle para o fim
    table = (
        GT(df)
        .tab_header(title=md(titulo or atributo), subtitle=md(subtitulo))
        .tab_stub(rowname_col="Corpus", groupname_col="group")
        .tab_style(
            style.text(weight="bold", size="small", align="center"), loc.row_groups()
        )
        .tab_stubhead(label="Corpus")
        .tab_options(data_row_padding_horizontal="20px")
        .cols_align("center")
        .sub_missing()
    )

    if rodape:
        table = table.tab_source_note(rodape)

    if atributo in ATRIB_PARA_FORMATADOR_GT:
        table = ATRIB_PARA_FORMATADOR_GT[atributo](table)

    if atributo in ATRIB_COLORIDOS:
        table = colorir_gt(table)

    table.show()


def join_resultados(nome_tabelas: list[str], nome_resultado: str) -> None:
    dfs = []
    for nome in nome_tabelas:
        df = pd.read_csv(
            Path(__file__).parents[1] / "resultados" / (nome + ".csv"), index_col=0
        )
        df.columns = df.columns + f"-{nome.replace(nome_resultado + '-', '')}"
        dfs.append(df)

    df = pd.concat(dfs, axis=1)
    df.to_csv(Path(__file__).parents[1] / "resultados" / (nome_resultado + ".csv"))
