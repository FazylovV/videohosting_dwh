FROM apache/airflow:2.1.2

USER airflow

ADD requirements.txt .
RUN pip install --no-cache-dir "apache-airflow==2.8.0" -r requirements.txt