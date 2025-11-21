from datetime import timedelta, datetime
import textwrap
from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator

with DAG(
    "Test_examples",
default_args={
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function, # or list of functions
        # 'on_success_callback': some_other_function, # or list of functions
        # 'on_retry_callback': another_function, # or list of functions
        # 'sla_miss_callback': yet_another_function, # or list of functions
        # 'on_skipped_callback': another_function, #or list of functions
        # 'trigger_rule': 'all_success'
    },
    start_date=datetime(2020, 1, 1),
    description="DAG tasks",
    schedule=timedelta(minutes=5),
    catchup=False,
    tags={"tasks"},
) as dag:

    ops1 = BashOperator(
        task_id="ar_dag_test_1",
        bash_command="date",
    )

    ops2 = BashOperator(
        task_id="ar_dag_test_2",
        bash_command="echo hello",
        retries=2,
    )

    ops1.doc_md = textwrap.dedent("""\
    ### Task definition
    You can run various test using `doc_md`
                                  
                                  """)
    dag.doc_md = __doc__
    dag.doc_md = """
    This is an example DAG
    """

    ops3 = BashOperator(
        task_id="ar_dag_test_3",
        depends_on_past=False,
        bash_command="echo final_level",
    )

    ops1 >> [ops2, ops3]