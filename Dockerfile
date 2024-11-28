FROM apache/airflow:2.1.2

USER airflow

ADD requirements.txt .
RUN pip install -r requirements.txt