# Mini-Projeto Semana 07 - Análise Exploratória do Varejo

Projeto de aprendizado do curso de Análise de Dados (SC Tech, turma T9).

Script em Python (pandas) que faz a análise exploratória da base **Varejo** (830.000 registros de compras):
importa o CSV, padroniza textos, números e datas, trata nulos e duplicatas, calcula estatísticas descritivas
do número de filhos dos clientes e explora padrões de agrupamento.

## Como executar

1. Baixe a base no [Kaggle](https://www.kaggle.com/datasets/namespaiva/base-varejo/data) e salve como `base_dados/Base Varejo.csv`.
2. Instale as dependências e rode o script:

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python Miniprojeto_Renato_Garcia_T9.py
```

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `Miniprojeto_Renato_Garcia_T9.py` | script da análise, dividido em sprints |
| `dados/df_limpo.csv` | base limpa gerada pelo script |
| `README_RenatoGarcia_T9.md` | passo a passo, insights e reflexão sobre ETL e qualidade de dados |
| `Mini_projeto.md` | enunciado |
| `requirements.txt` | dependências |

Autor: Renato Garcia
