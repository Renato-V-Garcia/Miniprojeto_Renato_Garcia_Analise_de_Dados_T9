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
# ==========================================================
titulo("SPRINT 3 - Limpeza de nulos e duplicatas")

# --- 3.1 Nulos ---------------------------------------------
# Além de vazios reais, a base usa "#N/D" (erro do Excel) como "não disponível".
print("Nulos por coluna:")
print(df.isna().sum().to_string())
print("Valores '#N/D' por coluna (texto):")
print({c: int((df[c] == "#N/D").sum()) for c in COLUNAS_TEXTO})


def preencher_vazio(valor, padrao):
    """Se o valor for vazio ou '#N/D', devolve o padrão; senão mantém o valor."""
    if pd.isna(valor) or valor == "" or valor == "#N/D":
        return padrao
    return valor


# Imputação: os registros sem categoria correspondem a um único produto (PR_ID 107);
# remover perderia vendas, então o rótulo explícito mantém a linha e
# deixa o problema visível nos agrupamentos.
df["PR_CAT"] = df["PR_CAT"].map(lambda v: preencher_vazio(v, "SEM CATEGORIA"))
df["PR_NOME"] = df["PR_NOME"].map(lambda v: preencher_vazio(v, "PRODUTO NAO IDENTIFICADO"))
print("Categorias após tratamento:", df["PR_CAT"].value_counts().to_dict())

# --- 3.2 Regra de negócio do número de compra (CO_ID) -------
# Cada nota fiscal deve pertencer a um único cliente e a uma única data.
por_nota = df.groupby("CO_ID").agg(
    clientes=("CL_ID", "nunique"), datas=("DATA", "nunique")
)
print(f"Notas (CO_ID) únicas: {len(por_nota)}")
print(f"Notas com mais de 1 cliente: {(por_nota['clientes'] > 1).sum()}")
print(f"Notas com mais de 1 data: {(por_nota['datas'] > 1).sum()}")

# --- 3.3 Duplicatas: erro de carga ou compra repetida? -----
# A base não tem coluna de quantidade. Antes de remover as linhas repetidas,
# testamos se elas são cópias acidentais ou o mesmo produto lançado várias vezes.
chaves = list(df.columns)
repetida = df.duplicated()
print(f"Linhas repetidas (excedentes): {repetida.sum()}")

# Teste 1: alguma nota aparece em mais de um bloco do arquivo? (carga em dobro)
bloco = (df["CO_ID"] != df["CO_ID"].shift()).cumsum()
notas_em_varios_blocos = (bloco.groupby(df["CO_ID"]).nunique() > 1).sum()
print(f"Teste 1 - notas espalhadas em mais de um bloco: {notas_em_varios_blocos}")

# Teste 2: distância (em linhas) entre as repetições de um mesmo item
grupo = df.groupby(chaves, sort=False).ngroup()
posicao = pd.Series(range(len(df)), index=df.index)
distancia = posicao.groupby(grupo).diff().dropna()
tamanho_max_nota = df.groupby("CO_ID").size().max()
print(f"Teste 2 - distância máxima entre repetições: {int(distancia.max())} linhas "
      f"(maior nota tem {tamanho_max_nota} linhas)")

# Teste 3: quantas vezes cada item se repete na nota
print("Teste 3 - tamanho dos grupos repetidos:",
      df.groupby(chaves).size().value_counts().sort_index().to_dict())

# Teste 4: taxa de repetição cresce com o tamanho da nota?
tamanho_nota = df.groupby("CO_ID")["CO_ID"].transform("size")
faixa = pd.cut(tamanho_nota, [0, 20, 40, 60, 90])
taxa = repetida.groupby(faixa, observed=True).mean().round(3)
print("Teste 4 - taxa de repetição por tamanho da nota:")
print(taxa.to_string())

print(
    "\nConclusão: nenhuma nota é duplicada em bloco e as repetições ocorrem dentro "
    "da própria nota; tratamos como unidades do mesmo item."
)

# Cria a coluna 'quantidade' (nº de linhas iguais) e mantém uma linha por item
df["quantidade"] = df.groupby(chaves)["CO_ID"].transform("size")
df_limpo = df.drop_duplicates(subset=chaves).reset_index(drop=True)
print(f"\nRegistros antes: {len(df)} | depois: {len(df_limpo)}")
print(f"Soma de 'quantidade' (deve ser igual ao total original): {df_limpo['quantidade'].sum()}")

# Salva a base limpa para o repositório
os.makedirs(os.path.dirname(CAMINHO_SAIDA), exist_ok=True)
df_limpo.to_csv(CAMINHO_SAIDA, index=False, sep=";", date_format="%Y-%m-%d")
print(f"Base limpa salva em: {CAMINHO_SAIDA}")


# ==========================================================
# SPRINT 4: Estatística descritiva (número de filhos - CL_FHL)
