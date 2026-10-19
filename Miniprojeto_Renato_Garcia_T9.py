# ==========================================================
# Mini-Projeto Semana 07 - Análise Exploratória (Varejo)
# Autor: Renato Garcia
# ==========================================================
import csv
import pandas as pd

CAMINHO_CSV = "base_dados/Base Varejo.csv"

# --- SPRINT 1: Importação dos dados ---
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
