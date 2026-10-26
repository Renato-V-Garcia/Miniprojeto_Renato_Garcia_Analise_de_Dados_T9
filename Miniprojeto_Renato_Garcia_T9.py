# ==========================================================
# Mini-Projeto Semana 07 - Análise Exploratória (Varejo)
# Autor: Renato Garcia
# ==========================================================
import csv
import os
import re
from datetime import datetime

import matplotlib
import pandas as pd

matplotlib.use("Agg")  # só grava arquivos, não abre janela
import matplotlib.pyplot as plt

CAMINHO_CSV = "base_dados/Base Varejo.csv"
CAMINHO_SAIDA = "dados/df_limpo.csv"
PASTA_GRAFICOS = "graficos"

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
# ==========================================================
titulo("SPRINT 4 - Estatística descritiva do número de filhos")

# CL_FHL é um atributo do cliente, não da compra. Se usássemos as linhas da base,
# quem compra mais itens pesaria mais. Por isso olhamos um registro por cliente.
clientes = df_limpo.drop_duplicates(subset="CL_ID")
filhos = clientes["CL_FHL"].astype(int)
print(f"Clientes únicos: {len(filhos)}")

print(f"Contagem:      {filhos.count()}")
print(f"Média:         {filhos.mean():.2f}")
print(f"Mediana:       {filhos.median():.1f}")
print(f"Desvio padrão: {filhos.std():.2f}")
print(f"Moda:          {filhos.mode().tolist()}")
print(f"Mínimo:        {filhos.min()}")
print(f"Máximo:        {filhos.max()}")
print(f"Quartis:       Q1={filhos.quantile(0.25):.1f} | Q2={filhos.quantile(0.50):.1f} "
      f"| Q3={filhos.quantile(0.75):.1f}")

print("\nResumo do describe():")
print(filhos.describe().round(2).to_string())

print("\nClientes por número de filhos:")
dist_filhos = filhos.value_counts().sort_index()
print(pd.DataFrame({"clientes": dist_filhos, "%": (dist_filhos / len(filhos) * 100).round(1)}))


# ==========================================================
# SPRINT 5: Agrupamentos, relatório e conclusões
# ==========================================================
titulo("SPRINT 5 - Agrupamentos e relatório final")

# Cada linha de df_limpo representa 'quantidade' itens vendidos,
# então as vendas são a soma de 'quantidade' (e não a contagem de linhas).

# --- 5.1 Vendas por gênero ---------------------------------
por_genero = df_limpo.groupby("CL_GENERO").agg(
    itens=("quantidade", "sum"),
    compras=("CO_ID", "nunique"),
    clientes=("CL_ID", "nunique"),
)
por_genero["itens_por_compra"] = (por_genero["itens"] / por_genero["compras"]).round(1)
print("Vendas por gênero:")
print(por_genero)

# --- 5.2 Vendas por categoria ------------------------------
por_categoria = df_limpo.groupby("PR_CAT")["quantidade"].sum().sort_values(ascending=False)
participacao = (por_categoria / por_categoria.sum() * 100).round(1)
print("\nItens vendidos por categoria:")
print(pd.DataFrame({"itens": por_categoria, "%": participacao}))

# --- 5.3 Categoria x gênero (pivot_table) ------------------
cat_genero = pd.pivot_table(
    df_limpo, index="PR_CAT", columns="CL_GENERO",
    values="quantidade", aggfunc="sum",
)
print("\nItens por categoria e gênero:")
print(cat_genero)

# --- 5.4 Evolução por ano ----------------------------------
por_ano = df_limpo.groupby(df_limpo["DATA"].dt.year).agg(
    itens=("quantidade", "sum"), compras=("CO_ID", "nunique"),
)
print("\nVendas por ano:")
print(por_ano)

# Meses mais fracos: ajuda a achar buracos na base
por_mes = df_limpo.groupby(df_limpo["DATA"].dt.to_period("M"))["quantidade"].sum()
piores_meses = por_mes.nsmallest(2).sort_index()
print("\nMeses com menos vendas:")
print(piores_meses.to_string())

# --- 5.5 Perfil de compra por número de filhos -------------
itens_por_filhos = df_limpo.groupby("CL_FHL")["quantidade"].sum()
clientes_por_filhos = clientes.groupby("CL_FHL")["CL_ID"].count()
media_por_cliente = (itens_por_filhos / clientes_por_filhos).round(0)
print("\nMédia de itens comprados por cliente, segundo o nº de filhos:")
print(media_por_cliente.to_string())

# --- 5.6 Gráficos ------------------------------------------
os.makedirs(PASTA_GRAFICOS, exist_ok=True)

# Gráfico 1: itens vendidos por categoria (barras horizontais)
fig, ax = plt.subplots(figsize=(8, 4.5))
ordenado = por_categoria.sort_values()
ax.barh(ordenado.index, ordenado.values, color="#2a6f97")
for i, valor in enumerate(ordenado.values):
    ax.text(valor, i, f" {participacao[ordenado.index[i]]}%", va="center")
ax.set_title("Itens vendidos por categoria")
ax.set_xlabel("Itens vendidos")
ax.set_xlim(0, ordenado.max() * 1.12)
fig.tight_layout()
fig.savefig(f"{PASTA_GRAFICOS}/itens_por_categoria.png", dpi=150)
plt.close(fig)

# Gráfico 2: vendas por mês (linha), destacando os meses com buraco
fig, ax = plt.subplots(figsize=(10, 4.5))
datas_mes = por_mes.index.to_timestamp()
ax.plot(datas_mes, por_mes.values, color="#2a6f97")
ax.scatter(piores_meses.index.to_timestamp(), piores_meses.values, color="#d62828", zorder=3)
ax.annotate("queda em set/out de 2022", xy=(piores_meses.index[0].to_timestamp(), piores_meses.iloc[0]),
            xytext=(-150, 30), textcoords="offset points", color="#d62828",
            arrowprops={"arrowstyle": "->", "color": "#d62828"})
ax.set_title("Itens vendidos por mês")
ax.set_ylabel("Itens vendidos")
ax.set_ylim(bottom=0)
fig.tight_layout()
fig.savefig(f"{PASTA_GRAFICOS}/vendas_por_mes.png", dpi=150)
plt.close(fig)

# Gráfico 3: clientes por número de filhos (barras), com média e mediana
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(dist_filhos.index, dist_filhos.values, color="#2a6f97")
ax.axvline(filhos.mean(), color="#d62828", linestyle="--", label=f"média = {filhos.mean():.2f}")
ax.axvline(filhos.median(), color="#333333", linestyle=":", label=f"mediana = {filhos.median():.0f}")
ax.set_title("Clientes por número de filhos")
ax.set_xlabel("Número de filhos")
ax.set_ylabel("Clientes")
ax.set_xticks(dist_filhos.index)
ax.legend()
fig.tight_layout()
fig.savefig(f"{PASTA_GRAFICOS}/clientes_por_filhos.png", dpi=150)
plt.close(fig)
print(f"\nGráficos salvos em: {PASTA_GRAFICOS}/")

# --- 5.7 Relatório final -----------------------------------
titulo("RELATÓRIO FINAL")
total_itens = int(df_limpo["quantidade"].sum())
print(f"Linhas originais:          {len(df)}")
print(f"Linhas após consolidação:  {len(df_limpo)}")
print(f"Itens vendidos:            {total_itens}")
print(f"Compras (notas):           {df_limpo['CO_ID'].nunique()}")
print(f"Clientes:                  {len(clientes)}")
print(f"Produtos distintos:        {df_limpo['PR_ID'].nunique()}")
print(f"Período:                   {df_limpo['DATA'].min():%d/%m/%Y} a {df_limpo['DATA'].max():%d/%m/%Y}")

genero_top = por_genero["itens"].idxmax()
print("\nCONCLUSÕES")
print(f"1. {por_categoria.index[0]} lidera as vendas com {participacao.iloc[0]}% dos itens; "
      f"{por_categoria.index[1]} e {por_categoria.index[2]} vêm em seguida.")
print(f"2. O gênero {genero_top} compra mais ({por_genero.loc[genero_top, 'itens']} itens), "
      "mas a diferença para o outro gênero é pequena.")
print(f"3. {(filhos == 0).mean() * 100:.0f}% dos clientes não têm filhos "
      f"(moda = {filhos.mode().iloc[0]}), mas a média é {filhos.mean():.2f} por causa da cauda até {filhos.max()}.")
print(f"4. {por_ano['itens'].idxmax()} foi o ano de maior venda; em {piores_meses.index[0]} e "
      f"{piores_meses.index[1]} as vendas despencam ({piores_meses.iloc[0]} e {piores_meses.iloc[1]} itens), "
      "o que sugere lacuna de dados.")
sem_cat = por_categoria.get("SEM CATEGORIA", 0)
print(f"5. Problema remanescente: {sem_cat} itens ({sem_cat / total_itens * 100:.1f}%) "
      "seguem sem categoria (produto PR_ID 107).")
print("6. A base não tem quantidade nem valor: 'quantidade' foi inferida das linhas "
      "repetidas, então não dá para medir faturamento.")
