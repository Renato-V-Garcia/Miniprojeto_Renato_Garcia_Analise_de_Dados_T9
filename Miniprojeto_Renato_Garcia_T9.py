# ==========================================================
# Mini-Projeto Semana 07 - Análise Exploratória (Varejo)
# Autor: Renato Garcia
# ==========================================================
import csv
import os
import re
from datetime import datetime

import pandas as pd

CAMINHO_CSV = "base_dados/Base Varejo.csv"
CAMINHO_SAIDA = "dados/df_limpo.csv"

COLUNAS_TEXTO = ["CL_GENERO", "CL_SEG", "PR_CAT", "PR_NOME"]
COLUNAS_INTEIRAS = ["CO_ID", "CL_ID", "CL_EC", "CL_FHL", "PR_ID"]


def titulo(texto):
    print("\n" + "=" * 60)
    print(texto)
    print("=" * 60)


# ==========================================================
# SPRINT 1: Importação dos dados
# ==========================================================
titulo("SPRINT 1 - Importação dos dados")

# Lê o CSV com csv.DictReader (leitura estruturada, linha a linha)
with open(CAMINHO_CSV, encoding="utf-8", newline="") as arquivo:
    leitor = csv.DictReader(arquivo, delimiter=";")
    linhas = list(leitor)

# Converte a lista de dicionários em DataFrame do pandas
df = pd.DataFrame(linhas)

# Remove as colunas vazias criadas pelos ";;;;" no fim de cada linha
df = df.loc[:, df.columns != ""]

# Visão geral da base
print("Registros:", len(df))
print("Colunas:", list(df.columns))
print(df.dtypes)
print(df.head())


# ==========================================================
# SPRINT 2: Transformação de strings, inteiros e datas
# ==========================================================
titulo("SPRINT 2 - Transformação de strings, inteiros e datas")


def limpar_texto(serie):
    """Remove espaços nas pontas, colapsa espaços repetidos (regex) e põe em maiúsculas."""
    return serie.str.replace(r"\s+", " ", regex=True).str.strip().str.upper()


# Texto: padroniza as colunas categóricas
for coluna in COLUNAS_TEXTO:
    df[coluna] = limpar_texto(df[coluna])

# Inteiros: valida com regex (só dígitos) antes de converter
for coluna in COLUNAS_INTEIRAS:
    invalidos = (~df[coluna].str.fullmatch(r"\d+")).sum()
    print(f"{coluna}: {invalidos} valores não numéricos")
    # errors="coerce" transforma valores inválidos em nulo, sem quebrar o script
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce").astype("Int64")

# Data: valida o formato dd/mm/aaaa com regex e converte com o módulo datetime
formato_ok = df["DATA"].str.fullmatch(r"\d{2}/\d{2}/\d{4}")
print(f"DATA: {(~formato_ok).sum()} valores fora do formato dd/mm/aaaa")


def converter_data(texto):
    """Converte 'dd/mm/aaaa' em datetime; devolve NaT se a data for inválida."""
    try:
        return datetime.strptime(texto, "%d/%m/%Y")
    except ValueError:
        return pd.NaT


# Converte só as datas únicas (são poucas) e mapeia para a coluna inteira
mapa_datas = {d: converter_data(d) for d in df["DATA"].unique()}
df["DATA"] = pd.to_datetime(df["DATA"].map(mapa_datas))
print(f"DATA: {df['DATA'].isna().sum()} datas inválidas")
print(f"Período: {df['DATA'].min():%d/%m/%Y} a {df['DATA'].max():%d/%m/%Y}")
print(df.dtypes)


# ==========================================================
# SPRINT 3: Limpeza de nulos e duplicatas
