
# ETL Orçamento SP

Este projeto consiste em desenvolver um pipeline ETL para processar os dados do orçamento do Estado de São Paulo de 2022, convertendo valores dolarizados para reais e armazenando-os em um formato adequado para responder às perguntas de negócio.






## Estrutura do Projeto

![Estrutura](estrutura.png)


## Pré Requisitos

- Docker
- Docker Compose
- Git
- Airflow
- Python
- SQL


## Instruções de Configuração

**1. Clone o repositório para a sua máquina local:**

```bash
git clone https://github.com/lariguim/etl_orcamento_sp.git
cd etl_orcamento_sp


```

**2. Configurar o ambiente virtual:**

```bash
python -m venv etl_orcamento_sp
source etl_orcamento_sp/bin/activate
pip install -r requirements.txt


```

**3. Configurar o Docker compose**

```bash
version: '3.7'
services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: orcamento_sp  
      POSTGRES_USER: larissa
      POSTGRES_PASSWORD: larissa
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  webserver:
    build: .
    depends_on:
      - postgres
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://larissa:larissa@postgres/orcamento_sp
      AIRFLOW__CORE__FERNET_KEY: 'fernet_key'
      AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: 'true'
      AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
    volumes:
      - ./dags:/opt/airflow/dags
      - ./scripts:/opt/airflow/scripts
      - ./entrypoint.sh:/entrypoint.sh
    ports:
      - "8080:8080"
    command: ["/entrypoint.sh"]

  scheduler:
    build: .
    depends_on:
      - postgres
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://larissa:larissa@postgres/orcamento_sp
      AIRFLOW__CORE__FERNET_KEY: 'fernet_key'
    volumes:
      - ./dags:/opt/airflow/dags
      - ./scripts:/opt/airflow/scripts
      - ./entrypoint.sh:/entrypoint.sh
    command: ["/entrypoint.sh"]

volumes:
  postgres_data:



```

**4. Você pode gerar uma chave Fernet utilizando o script fernet_key.py:**

```bash
  python scripts/fernet_key.py

```

**5. Iniciar os serviços**

```bash
docker-compose up -d


```


**6. Configurar Airflow**

Acesse a interface web do Airflow em http://localhost:8080 e configure a conexão com o PostgreSQL:

- airflow_user: admin
- airflow_password: admin

**Conexao PostgreSQL**

- Connection ID: postgres_default
- Conn Type: Postgres
- Host: postgres
- Schema: orcamento_sp
- Login: larissa
- Password: larissa
- Port: 5432
Acesse a interface web do Airflow em http://localhost:8080 e ative a DAG orcamento_etl_dag


## Executando a DAG
Acesse a interface do Airflow em http://localhost:8080, ative a DAG orcamento_etl_dag e execute-a manualmente para iniciar o processo ETL


## Scripts em ordem de execução: 

- extract.py: Contém funções para extração de dados de despesas e receitas.

- get_exchange_rate.py: Contém funções para obter a taxa de câmbio no dia 22/06/2022.

- transform.py: Contém funções para a transformação de dados de despesas e receitas.

- load_data.py: Contem funçoes que criam conexoes com o banco PostgreSQL, e carregam os dados transformados em uma tabela final chamada orcamento.

- etl.py: script principal do pipeline.

## Premissas de Negócio

- Transformaçoes realizadas: conversao das colunas Total Liquidado e Total Arrecadado para numerico;
- Filtragem de valores nulos e zeros, considerando que, fonte de recurso sem liquidacao e sem arrecadacao nao sao relevantes em análises. 
- Remoçao de linhas onde Fonte de Recurso está ausente.
## Respondendo Perguntas de négocio com SQL

Uma vez que os dados estejam carregados na tabela, você pode utilizar as seguintes consultas SQL para responder às perguntas:

**1. Quais são as 5 fontes de recursos que mais arrecadaram?**

```sql
  SELECT * FROM orcamento ORDER BY Total_Arrecadado DESC LIMIT 5;
```
- 001	TESOURO-DOT.INICIAL E CRED.SUPLEMENTAR
- 006	OUTRAS FONTES DE RECURSOS
- 005	RECURSOS VINCULADOS FEDERAIS
- 082	RECURSOS VINCULADOS ESTADUAIS-INTRA
- 007	OP.CRED.E CONTRIB.DO EXTERIOR-DOT.INIC.CR.SU


**2. Quais são as 5 fontes de recursos que mais gastaram?**

```sql
  SELECT * FROM orcamento ORDER BY Total_Liquidado DESC LIMIT 5;

```

- 041	TESOURO - CREDITO POR SUPERAVIT FINANCEIRO
- 082	RECURSOS VINCULADOS ESTADUAIS-INTRA
- 006	OUTRAS FONTES DE RECURSOS
- 005	RECURSOS VINCULADOS FEDERAIS
- 047	REC.OPERAC. DE CREDITO-P/SUPERAVIT FINANCEIR




**3. Quais são as 5 fontes de recursos com a melhor margem bruta?**

```sql
  SELECT * FROM orcamento ORDER BY (Total_Arrecadado - Total_Liquidado) DESC LIMIT 5;

```
- 001	TESOURO-DOT.INICIAL E CRED.SUPLEMENTAR
- 006	OUTRAS FONTES DE RECURSOS
- 005	RECURSOS VINCULADOS FEDERAIS
- 086	OUTRAS FONTES DE RECURSOS-INTRA
- 007	OP.CRED.E CONTRIB.DO EXTERIOR-DOT.INIC.CR.SU


**4. Quais são as 5 fontes de recursos que menos arrecadaram?**

```sql
  SELECT * FROM orcamento ORDER BY Total_Arrecadado ASC LIMIT 5;
```

- 041	TESOURO - CREDITO POR SUPERAVIT FINANCEIRO
- 045	REC.VINC.TRANSF.FEDERAL/SUPERAVIT FINANC.
- 044	REC.PROP.ADM.IND-CRED.P/SUPERVAVIT FINANCEIR
- 042	REC.VINC.ESTADUAIS-CRED.SUPERAVIT FINANCEIRO
- 004	REC.PROPRIO-ADM.IND.-DOT.INIC.CR.SUPL.



**5.Quais são as 5 fontes de recursos que menos gastaram?**

```sql
SELECT * FROM orcamento ORDER BY Total_Liquidado ASC LIMIT 5;
```
- 043	F.E.D - CREDITO POR SUPERAVIT FINANCEIRO
- 084	REC.PROPRIO-ADM.IND.-DOT.INIC.CR.SUPL.-INTRA
- 083	RECURSOS VINCULADOS-FUNDO ESP. DESPESA-INTRA
- 044	REC.PROP.ADM.IND-CRED.P/SUPERVAVIT FINANCEIR
- 002	RECURSOS VINCULADOS ESTADUAIS


**6. Quais são as 5 fontes de recursos com a pior margem bruta?**

```sql
  SELECT * FROM orcamento ORDER BY (Total_Arrecadado - Total_Liquidado) ASC LIMIT 5;

```
- 043	F.E.D - CREDITO POR SUPERAVIT FINANCEIRO
- 084	REC.PROPRIO-ADM.IND.-DOT.INIC.CR.SUPL.-INTRA
- 083	RECURSOS VINCULADOS-FUNDO ESP. DESPESA-INTRA
- 044	REC.PROP.ADM.IND-CRED.P/SUPERVAVIT FINANCEIR
- 002	RECURSOS VINCULADOS ESTADUAIS



**7. Qual a média de arrecadação por fonte de recurso?**

```sql
  SELECT AVG(Total_Arrecadado) FROM orcamento;

```

1.394.670.977,53



**8. Qual a média de gastos por fonte de recurso?**

```sql
SELECT AVG(Total_Liquidado) FROM orcamento;

```
222.860.257,96


## Observações

O projeto foi salvo em um banco PostgreSQL por ser uma versao gratuita de banco de dados. Não utilizei o BigQuery conforme preferencia devido a falta de recursos para acessar a Cloud. 


## Documentation

- [Docker](https://docs.docker.com/manuals/)
- [Airflow](https://airflow.apache.org/docs/)



## Próximos Passos


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
