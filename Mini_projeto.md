# Análise de Dados com Python [T9]

## Mini-Projeto Avaliativo - Módulo 1 - Semana 07

## Sumário

1. Contextualização
2. Desafio
3. Resultados Esperados (Entrega)
4. Requisitos das Tarefas
5. Critérios de Avaliação

---

## 1. Contextualização

Você está desenvolvendo uma Análise Exploratória de Dados (AED) aplicada ao varejo para aprender como transformar dados brutos em informações úteis.

A base "Varejo" contém registros reais de compras (datas, clientes, produtos, categorias e valores). Aprender a verificar qualidade, limpar e sumarizar esses dados é uma habilidade prática essencial para quem trabalha com BI e Visualização de Dados.

Neste mini-projeto você vai praticar tarefas comuns no trabalho: identificar problemas nos dados (valores nulos, tipos incorretos, duplicados), tratar esses problemas com ferramentas como pandas e gerar estatísticas simples e funções de agrupamento, para responder perguntas operacionais (quem compra mais, quais categorias vendem mais, como variam as vendas ao longo do tempo).

O objetivo educacional é que, ao final, você saiba preparar uma base para análises mais avançadas ou para alimentar um dashboard: entender os dados, limpá-los, extrair estatísticas descritivas e comunicar os principais insights de forma objetiva.

## 2. Desafio

Entregar um script em Python que realize uma Análise Exploratória da base Varejo seguindo etapas claras, documentadas e reproduzíveis.

### Etapas obrigatórias

1. Carregar a base `Varejo.csv` com pandas e mostrar: número de registros, colunas e tipos de dados.
2. Verificar e reportar ao menos dois problemas básicos: valores nulos por coluna, duplicatas e possíveis inconsistências (ex.: datas inválidas ou categorias vazias).
3. Fazer as três etapas de limpeza mínima necessária: remover ou imputar nulos (explique a escolha), eliminar duplicatas relevantes e ajustar tipos de dados (ex.: converter coluna DATA para datetime).
4. Gerar estatísticas descritivas básicas para coluna de número de filhos do cliente (média; mediana; desvio padrão; moda; máximo; mínimo; e contagem, quartis).
5. Explorar padrões de agrupamento com pelo menos dois agrupamentos (por exemplo: gênero com mais vendas, compras), usando `groupby()` ou `pivot_table()`.
6. Produzir um pequeno bloco de conclusões (3–6 tópicos) com os principais insights obtidos e possíveis problemas remanescentes na base. Notebook Python, MD ou um "print".

### Requisitos técnicos mínimos

- O script deve ser executável em VsCode ou Google Colab (arquivo `.py`).
- Usar pandas; outras bibliotecas são opcionais (NumPy, Matplotlib, Seaborn).

Base de dados (varejo) sugerida no Kaggle: <https://www.kaggle.com/datasets/namespaiva/base-varejo/data>

## 3. Resultados Esperados (Entrega)

Para que sua avaliação seja concluída com sucesso, você deve entregar:

- **Código-Fonte (Python):** Um arquivo `.py` ou link do Google Colab contendo a lógica desenvolvida. O código deve estar comentado, explicando o que cada bloco de lógica realiza.
- **Repositório no GitHub:** O projeto deve ser enviado para um repositório público no seu GitHub. Espera-se que:
  - O repositório tenha um arquivo `README.md` básico explicando o projeto.
  - O histórico de commits demonstre o progresso do trabalho (não envie tudo em um único commit final!).
  - Arquivo `README_NomeDoAluno_Turma.md`, com instruções simples (ex.: "Abra no VsCode ou Colab e rode todas as células" ou `python Miniprojeto_…py`).
- Os arquivos com a solução do mini-projeto deverão ser inseridos no Repositório GitHub em modo público (repositório de sua conta pessoal do GitHub). Padrão de nome do Github: `Miniprojeto_NomeAluno_Turma` (Turma: `Analise_de_Dados_T1`).
- O link do Repositório GitHub deverá ser submetido na tarefa **Módulo 1 - Mini-Projeto Avaliativo**, presente na semana 07 do AVA até o dia **26/10/2026 às 22h**.

## 4. Requisitos das Tarefas

As tarefas devem seguir os seguintes sprints:

- **Sprint 1 (Importação dos dados):** Realização da importação dos dados na plataforma Kaggle para a IDE VsCode ou Colab, onde o script será executado.
- **Sprint 2 (Transformação de Strings, Integer e Float e Datetime):** Desenvolvimento das funções de limpeza de texto, inteiros e decimais usando métodos e expressões regulares.
- **Sprint 3 (Limpeza de Nulos e Duplicatas):** Aplicação das condicionais e funções para identificação e substituição de valores vazios e de str para valores de data tipo datetime, na tabela de varejo.
- **Sprint 4 (Estatística Descritiva):** Aplicação das funções estatísticas para coletar parâmetros da coluna de Número de filhos do cliente.
- **Sprint 5 (Relatório e Documentação):** Construção dos contadores do relatório final exibido no terminal, finalização do `README.md` com a reflexão teórica e submissão do link no AVA.
- **Sprint 6 (Versionamento):** Envio dos arquivos (script + `README.md` + df_limpo), via Git para o repositório no GitHub.

## 5. Critérios de Avaliação

A tabela abaixo apresenta os critérios que serão avaliados durante a correção do projeto. O mesmo possui variação de nota de 0 (zero) a 10 (dez) como nota mínima e máxima, e possui peso de 25% sobre a avaliação do módulo.

Serão desconsiderados e atribuída a nota 0 (zero) os projetos que apresentarem plágio de soluções encontradas na internet ou de outros colegas. Lembre-se: Você está livre para utilizar outras soluções como base, mas não é permitida a cópia.

### Documentação do Projeto (2,50)

| Nº | Critério de Avaliação | 0 | 1,25 |
|----|-----------------------|---|------|
| 1 | Versionamento | Não entregou o repositório no GitHub contendo os arquivos organizados e um README.md explicativo com a reflexão teórica obrigatória sobre ETL e qualidade de dados. | Entregou o repositório no GitHub contendo os arquivos organizados e um README.md explicativo com a reflexão teórica obrigatória sobre ETL e qualidade de dados. |
| 2 | Documentação | Não desenvolveu Arquivo README.md contendo de 3-6 tópicos com insights obtidos da análise dos dados. | Desenvolveu Arquivo README.md contendo de 3-6 tópicos com insights obtidos da análise dos dados. |

### Desenvolvimento do Projeto (7,50)

| Nº | Critério de Avaliação | 0 | 0,75 | 1,50 |
|----|-----------------------|---|------|------|
| 3 | Manipulação de Arquivos CSV | Não realizou a leitura e extração dos arquivos de dados de forma parcialmente estruturada (csv.DictReader). | Realizou a leitura e extração dos arquivos de dados de forma parcialmente estruturada (csv.DictReader). | Realizou a leitura e extração dos arquivos de dados de forma estruturada e nativa (csv.DictReader). |
| 4 | Tratamento de Nulos e Condicionais | Não implementou a lógica (if/else) para preencher categorias vazias com "Sem Categoria" e não tratou os nulos das dimensões físicas, justificando a escolha. | Implementou parcialmente a lógica (if/else) para preencher categorias vazias com "Sem Categoria" e tratou parcialmente os nulos das dimensões físicas, justificando a escolha. | Implementou a lógica (if/else) para preencher categorias vazias com "Sem Categoria" e tratou corretamente os nulos das dimensões físicas, justificando a escolha. |
| 5 | Regras de Negócio e Datas | Não validou a regra do identificador de número de compra separando os registros, e converteu parcialmente a string de data da compra utilizando o módulo datetime. | Validou parcialmente a regra do identificador de número de compra separando os registros, e converteu parcialmente a string de data da compra utilizando o módulo datetime. | Validou a regra do identificador de número de compra, e converteu com sucesso a string de data da compra utilizando o módulo datetime. |
| 6 | Padrões de Agrupamento | Não explorou padrões de agrupamento com pelo menos duas combinações. | Explorou parcialmente padrões de agrupamento com uma combinação. | Explorou padrões de agrupamento com pelo menos duas combinações. |
| 7 | Geração de Estatísticas Básicas | Não gerou as estatísticas básicas de acordo com a coluna Número de filhos dos clientes, não contemplando os parâmetros elencados. | Gerou parcialmente as estatísticas básicas de acordo com a coluna Número de filhos dos clientes, contemplando parte dos parâmetros elencados. | Gerou as estatísticas básicas de acordo com a coluna Número de filhos dos clientes, contemplando todos os parâmetros elencados. |
