# Projeto ETL orcamento SP

## 1.0 Visão Geral
O projeto ETL Orçamento SP automatiza o processo de extração, transformação e carga (ETL) de dados de despesas e receitas do orçamento de São Paulo. Utiliza técnicas para limpar, normalizar, enriquecer e converter dados, garantindo sua integridade e consistência ao serem carregados em um banco de dados PostgreSQL.

## 2.0 Estrutura do Projeto
O projeto é dividido em módulos que desempenham funções específicas em cada etapa do processo ETL:

**2.1. extract.py**
Responsável pela extração dos dados brutos de despesas e receitas do orçamento.

Funções:
extract_despesas: Conecta-se às fontes de dados de despesas e recupera os dados em um formato bruto.
extract_receitas: Conecta-se às fontes de dados de receitas e recupera os dados em um formato bruto.

**2.2 get_exchange_rate.py**
Contém funções para obter a taxa de câmbio do dia 22/06/2022.

Funções
get_exchange_rate_on_date: Conecta-se a um serviço de câmbio ou API para recuperar a taxa de câmbio específica para a data 22/06/2022.

**2.3. transform.py**
Responsável pela transformação dos dados extraídos em um formato padronizado.

Funções
clean_data: Limpa os dados brutos, removendo inconsistências, duplicidades e valores inválidos.
transform_despesas: Transforma os dados de despesas, ajustando formatos e aplicando conversão de moeda, se necessário.
transform_receitas: Transforma os dados de receitas, ajustando formatos e aplicando conversão de moeda, se necessário.

**2.4. load_data.py**
Gerencia a conexão com o banco de dados PostgreSQL e carrega os dados transformados na tabela final chamada "orcamento".

Funções
create_db_connection: Estabelece e valida a conexão com o banco de dados PostgreSQL.
load_to_orcamento: Insere os dados transformados na tabela "orcamento", garantindo a integridade e consistência dos dados.

**2.5. etl.py**
Script principal do pipeline ETL, responsável por orquestrar todas as etapas do processo de ETL.

Funcionalidades
Extração: Utiliza as funções em extract.py para extrair dados brutos de despesas e receitas.
Transformação: Utiliza as funções em transform.py para limpar, transformar e preparar os dados para carga.
Carga: Utiliza as funções em load_data.py para estabelecer conexão com o banco de dados e carregar os dados transformados na tabela "orcamento".
Gestão de Erros: Utiliza logging para registrar informações detalhadas sobre o processo, incluindo erros e status de execução.

Configuração
Antes de executar o script etl.py, certifique-se de configurar corretamente os parâmetros de conexão com o banco de dados PostgreSQL em load_data.py.

Execução do Script
Para iniciar o processo ETL, execute o script etl.py. Ele orquestrará todas as etapas de extração, transformação e carga dos dados.

Notas Adicionais
Gerenciamento de Erros: Cada módulo utiliza logging para registrar erros críticos, erros durante as etapas de transformação e carga de dados, e informações sobre o processo de extração e transformação.

Dependências: Verifique e instale as bibliotecas necessárias, como psycopg2, pandas e requests, antes de executar os scripts.


![Estrutura](estrutura.png)


## 3.0 Ferramentas

- Docker
- Docker Compose
- Git
- Airflow
- Python
- SQL


## 3.0 Instruções de configuração local

**3.1. Clone o repositório para a sua máquina local:**

```bash
git clone https://github.com/lariguim/etl_orcamento_sp.git
cd etl_orcamento_sp


```

**3.2. Configurar o ambiente virtual:**

```bash
python -m venv etl_orcamento_sp
source etl_orcamento_sp/bin/activate
pip install -r requirements.txt


```

**3.3. Configurar o Docker compose**

```bash
AIRFLOW__CORE__FERNET_KEY: 'fernet_key'
    
```

**3.4. Você pode gerar uma chave Fernet utilizando o script fernet_key.py:**

```bash
  python scripts/fernet_key.py

```

**3.5. Iniciar os serviços**

```bash
docker-compose up -d


```


**3.6. Configurar Airflow**

Acesse a interface web do Airflow em http://localhost:8080 e configure a conexão com o PostgreSQL:

- airflow_user: admin
- airflow_password: admin

**3.7. Conexao PostgreSQL**

- Connection ID: postgres_default
- Conn Type: Postgres
- Host: postgres
- Schema: orcamento_sp
- Login: larissa
- Password: larissa
- Port: 5432
Acesse a interface web do Airflow em http://localhost:8080 e ative a DAG orcamento_etl_dag


**3.8. Executando a DAG**
Acesse a interface do Airflow em http://localhost:8080, ative a DAG orcamento_etl_dag e execute-a manualmente para iniciar o processo ETL



## 4.0 Premissas de Negócio

  - Filtragem de valores nulos e zeros, considerando que fontes de recurso sem liquidação e sem arrecadação não são relevantes em análises.
  - Remoção de linhas onde a Fonte de Recurso está ausente.
  - Ambas as funções de transformação (`transform_despesas` e `transform_receitas`) são projetadas para lidar com erros de formatação nos valores numéricos, como pontos e vírgulas.
  - Após as transformações, os DataFrames resultantes (`df_despesas_transform` e `df_receitas_transform`) são utilizados para inserir os dados no banco de dados ou para outros fins de análise ou processamento.


## 5.0 Tabela final

| ID Fonte Recurso  | Nome Fonte Recurso | Total Liquidado | Total Arrecadado |
| ------------- | ------------- | ------------- | ------------- |
| 001  | TESOURO-DOT.INICIAL E CRED.SUPLEMENTAR  | 9999.99 | 9999.99 |



## 6.0 Dicionário de Dados

- ID Fonte Recurso: Código da fonte de recurso segundo arquivo fonte
- Nome da Fonte de Recurso: Nome da Fonte de Recurso segundo arquivo fonte
- Total Liquidado: Valor da liquidação da despesa em Real
- Total Arrecadado: Valor da arrecadação da receita em real




## 7.0 Questões de Negócio

Uma vez que os dados estejam carregados na tabela, você pode utilizar as seguintes consultas SQL para responder às perguntas:

**1. Quais são as 5 fontes de recursos que mais arrecadaram?**

```sql
select id_fonte_recurso, nome_fonte_recurso, total_arrecadado 
from orcamento
order by total_arrecadado DESC
limit 5;
```
- 001	TESOURO-DOT.INICIAL E CRED.SUPLEMENTAR
- 006	OUTRAS FONTES DE RECURSOS
- 005	RECURSOS VINCULADOS FEDERAIS
- 082	RECURSOS VINCULADOS ESTADUAIS-INTRA
- 007	OP.CRED.E CONTRIB.DO EXTERIOR-DOT.INIC.CR.SU


**2. Quais são as 5 fontes de recursos que mais gastaram?**

```sql
select id_fonte_recurso, nome_fonte_recurso, total_liquidado
from orcamento
order by total_liquidado DESC
limit 5;
```

- 041	TESOURO - CREDITO POR SUPERAVIT FINANCEIRO
- 082	RECURSOS VINCULADOS ESTADUAIS-INTRA
- 006	OUTRAS FONTES DE RECURSOS
- 005	RECURSOS VINCULADOS FEDERAIS
- 047	REC.OPERAC. DE CREDITO-P/SUPERAVIT FINANCEIR




**3. Quais são as 5 fontes de recursos com a melhor margem bruta?**

```sql
SELECT id_fonte_recurso, nome_fonte_recurso, total_liquidado, total_arrecadado
FROM orcamento ORDER BY (total_arrecadado - total_liquidado) DESC LIMIT 5;

```
- 001	TESOURO-DOT.INICIAL E CRED.SUPLEMENTAR
- 006	OUTRAS FONTES DE RECURSOS
- 005	RECURSOS VINCULADOS FEDERAIS
- 086	OUTRAS FONTES DE RECURSOS-INTRA
- 007	OP.CRED.E CONTRIB.DO EXTERIOR-DOT.INIC.CR.SU


**4. Quais são as 5 fontes de recursos que menos arrecadaram?**

```sql
SELECT id_fonte_recurso, nome_fonte_recurso, total_arrecadado
FROM orcamento ORDER BY total_arrecadado ASC
LIMIT 5;
```

- 041	TESOURO - CREDITO POR SUPERAVIT FINANCEIRO
- 045	REC.VINC.TRANSF.FEDERAL/SUPERAVIT FINANC.
- 044	REC.PROP.ADM.IND-CRED.P/SUPERVAVIT FINANCEIR
- 042	REC.VINC.ESTADUAIS-CRED.SUPERAVIT FINANCEIRO
- 004	REC.PROPRIO-ADM.IND.-DOT.INIC.CR.SUPL.



**5.Quais são as 5 fontes de recursos que menos gastaram?**

```sql
SELECT id_fonte_recurso, nome_fonte_recurso, total_liquidado
FROM orcamento ORDER BY total_liquidado ASC
LIMIT 5;
```
- 043	F.E.D - CREDITO POR SUPERAVIT FINANCEIRO
- 084	REC.PROPRIO-ADM.IND.-DOT.INIC.CR.SUPL.-INTRA
- 083	RECURSOS VINCULADOS-FUNDO ESP. DESPESA-INTRA
- 044	REC.PROP.ADM.IND-CRED.P/SUPERVAVIT FINANCEIR
- 002	RECURSOS VINCULADOS ESTADUAIS


**6. Quais são as 5 fontes de recursos com a pior margem bruta?**

```sql
SELECT id_fonte_recurso, nome_fonte_recurso, total_arrecadado, total_liquidado
FROM orcamento ORDER BY (total_arrecadado - total_liquidado) ASC
LIMIT 5;

```
- 043	F.E.D - CREDITO POR SUPERAVIT FINANCEIRO
- 084	REC.PROPRIO-ADM.IND.-DOT.INIC.CR.SUPL.-INTRA
- 083	RECURSOS VINCULADOS-FUNDO ESP. DESPESA-INTRA
- 044	REC.PROP.ADM.IND-CRED.P/SUPERVAVIT FINANCEIR
- 002	RECURSOS VINCULADOS ESTADUAIS



**7. Qual a média de arrecadação por fonte de recurso?**

```sql
  SELECT AVG(total_arrecadado) FROM orcamento;

```

1.394.670.977,53



**8. Qual a média de gastos por fonte de recurso?**

```sql
SELECT AVG(total_liquidado) FROM orcamento;

```
222.860.257,96


## 8.0 Observações

O projeto foi salvo em um banco PostgreSQL por ser uma versao gratuita de banco de dados. Não utilizei o BigQuery conforme preferencia devido a falta de recursos para acessar a Cloud. 


## 9.0 Documentação

- [Docker](https://docs.docker.com/manuals/)
- [Airflow](https://airflow.apache.org/docs/)



## 10.0 Próximos Passos


Essa projeto foi dividido em ciclos e essa entrega corresponde ao ciclo 1 do projeto, a primeira versao do nosso pipeline de etl para orçamentos do estado de SP. O ciclo 1 tem, tem o objetivo de estruturar uma entrega rápida pensado estratégicamente para munir o negócio de informações.
Sendo assim, com essa versão, já é possível extrair algumas informações úteis para nortear as decisões de negócio. 

Para dar continuidade ao projeto, entraremos no **ciclo 2, 3 e 4**, que contemplam as melhorias listadas abaixo:

**Teste Unitario:** 
- Escrever testes unitários para os scripts extract.py, get_exchange_rate.py, transform.py e load_data.py usando unittest ou pytest.

**Melhoria do Pipeline:**
- Implementar logs detalhados nos scripts para monitorar o progresso e diagnosticar problemas.
- Configurar monitoramento e alertas no Airflow para notificações em caso de falhas no pipeline.


**Automatização e CI/CD**
- CI/CD: Configurar um pipeline de CI/CD usando GitHub Actions, Jenkins, ou outra ferramenta de CI/CD para automatizar testes e implantações.

**Melhoria de Desempenho**
- Otimização de Consultas: Revisar e otimizar as consultas SQL para melhorar o desempenho.
- Escalabilidade: Verificar a escalabilidade do pipeline, especialmente se o volume de dados aumentar.

**Deploy em Produção**
- BigQuery: Finalizar a integração com o BigQuery e testar a carga de dados em produção.
- Segurança: Implementar práticas de segurança, como o gerenciamento adequado de segredos e variáveis de ambiente.

**Feedback e Iteração**
- Feedback: Obter feedback do time sobre os resultados e possíveis melhorias.
- Iteração: Iterar sobre o pipeline com base no feedback, adicionando novas features ou melhorando as existentes.

**Escalonamento**
- Novas Fontes de Dados: Adicionar novas fontes de dados se necessário.
- Manutenção Contínua: Estabelecer um plano de manutenção contínua para monitorar e atualizar o pipeline conforme necessário.
