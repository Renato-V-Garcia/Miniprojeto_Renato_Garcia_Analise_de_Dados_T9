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
