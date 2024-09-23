from __future__ import annotations

import datetime
import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="dags_bash_operator",                             # Dag이름, DAG 파일명과 Dag id는 일치시키자 
    schedule="0 0 * * *",                                    # 5개 항목, 분, 시, 일, 월, 요일 
    start_date=pendulum.datetime(2024, 9, 23, tz="Asia/Seoul"),
    catchup=False,                                          # False: start_date 설정에서 현재 시간 누락된 이미 지난 시간의 스케쥴은 run하지 않음 
    dagrun_timeout=datetime.timedelta(minutes=60),          # 60분이상 수행못하면 실패 
    tags=["example", "example2"],                           # DAG의 태그를 걸어줌 
    params={"example_key": "example_value"},                # task들에게 전달해줄 공통된 파라미터
) as dag:
    # [START howto_operator_bash]
    # task 객체 명 
    bash_t1 = BashOperator(
        task_id="bash_t1",                                       # task id로 task id도 task 객체명과 동일하게 두자 
        bash_command="echo whoami",                              # task를 통해 어떤 쉘 스크립트를 수행할 것이냐
    )
    
    bash_t2 = BashOperator(
        task_id="bash_t2",                                       
        bash_command="echo $HOSTNAME",                              
    )
    
    bash_t1 >> bash_t2                                              # bash_t1을 수행하고 bash_t2를 수행하자 
    