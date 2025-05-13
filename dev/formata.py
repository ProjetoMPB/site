import ast

import numpy as np
import pandas as pd


def _formata_moda_linha(linha: str) -> str:
    linha = ast.literal_eval(linha)
    return f"{linha[0]} ({linha[1] * 100:.1f})"


def formata_int(series: pd.Series) -> pd.Series:
    return series.astype(int)


def formata_moda(df: pd.DataFrame) -> pd.Series:
    return df.apply(_formata_moda_linha)


def formata_moda_df(df: pd.DataFrame) -> pd.DataFrame:
    return df.map(_formata_moda_linha)


def formata_indice(indice: float) -> str:
    return f"{indice:.2f}"


def formata_proporcao_df(df: pd.DataFrame):
    return df.replace(0, np.nan).map(lambda p: float(f"{p * 100:.1f}"))


def formata_proporcao(series: pd.Series):
    return series.apply(lambda p: f"{p * 100:.1f}").replace("nan", "-")


def formata_indices(series: pd.Series):
    return series.apply(formata_indice)


def formata_moda_grau(series: pd.Series):
    def formata_linha(linha: str) -> str:
        grau, prop = ast.literal_eval(linha)
        return f"{int(grau)} ({prop * 100:.1f})"

    return series.map(formata_linha)


def formata_1M1a(series: pd.Series):
    return "^" + formata_moda_grau(series)


def formata_1M1b(series: pd.Series):
    def formata_linha(linha: str) -> str:
        nome, prop = ast.literal_eval(linha)
        return f"{nome.capitalize()} ({prop * 100:.1f})"

    return series.map(formata_linha)


def formata_1H1b(series: pd.Series):
    def formata_linha(linha: str) -> str:
        fund, prop = ast.literal_eval(linha)
        fund, modo = fund[:-1], fund[-1]
        fund = {
            "0": "dó",
            "1": "dó#",
            "2": "ré",
            "3": "mib",
            "4": "mi",
            "5": "fá",
            "6": "fá#",
            "7": "sol",
            "8": "láb",
            "9": "lá",
            "10": "sib",
            "11": "si",
        }[fund]
        if modo == "M":
            fund = fund.upper()
        return f"{fund} ({prop * 100:.1f})"

    return series.map(formata_linha)


ATR_TO_FORMATTER = {
    "1M1a-maior": formata_1M1a,
    "1M1a-menor": formata_1M1a,
    "1M1b": formata_1M1b,
    "1M1c": formata_moda_grau,
    "1M1d": formata_indices,
    "1M2a": formata_moda,
    "1M2b": formata_moda,
    "1M2c": formata_moda,
    "1M2d": formata_indices,
    "1M2e": formata_indices,
    "1M3a": formata_moda,
    "1M3b": formata_moda,
    "1M3c": formata_moda,
    "1M3d": formata_indices,
    "1H1a": formata_moda,
    "1H1b": formata_1H1b,
    "1H2a": formata_moda,
    "1H2b": formata_moda,
    "1H3a": formata_moda,
    "1H3b": formata_moda,
    "1H3c": formata_moda,
    "1H4a": formata_proporcao_df,
    "1H4c": formata_moda,
    "1H4d": formata_moda,
    "1H1e": formata_moda,
    "2H1a": formata_moda_df,
    "2H1b": formata_proporcao_df,
    "2H1c": formata_proporcao_df,
    "2H2a": formata_moda_df,
    "2H2b": formata_proporcao_df,
    "2H2c": formata_proporcao_df,
    "2H2d": formata_proporcao_df,
    "2H3a": formata_moda_df,
    "2H3b": formata_proporcao_df,
    "2H3c": formata_proporcao_df,
    "2H3c-DIA": formata_proporcao_df,
    "2H3c-DS": formata_proporcao_df,
    "2H3c-SUBV": formata_proporcao_df,
    "2H3c-EC1": formata_proporcao_df,
    "2H3c-EC2": formata_proporcao_df,
    "2H3d": formata_int,
    "2M1a": formata_proporcao_df,
    "2M1b": formata_proporcao_df,
    "2M1c": formata_proporcao_df,
    "2M1d": formata_proporcao_df,
    "2M2a": formata_proporcao_df,
    "2M2b": formata_proporcao_df,
    "2M3a": formata_proporcao_df,
    "2M3b": formata_proporcao_df,
    "2M3c": formata_proporcao_df,
}

ATR_TO_COLUMN_NAME = {
    "1M1a-maior": "1M1a (maior)",
    "1M1a-menor": "1M1a (menor)",
}


def formatar_atributos_serie(df):
    for c in df.columns:
        try:
            df[c] = ATR_TO_FORMATTER[c](df[c])
        except KeyError:
            pass
        if c in ATR_TO_COLUMN_NAME:
            df.rename(columns={c: ATR_TO_COLUMN_NAME[c]}, inplace=True)
    return df


def formatar_atributos_df(df: pd.DataFrame, atributo: str):
    if atributo in ATR_TO_FORMATTER:
        df = ATR_TO_FORMATTER[atributo](df)
    return df
