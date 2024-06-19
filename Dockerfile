FROM apache/airflow:2.9.2

USER root


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        default-libmysqlclient-dev \
        libpq-dev


USER airflow


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY dags /opt/airflow/dags
COPY scripts /opt/airflow/scripts

ENTRYPOINT ["bash", "/entrypoint.sh"]
