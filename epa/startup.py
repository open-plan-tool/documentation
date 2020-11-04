import os

from epa.settings import BASE_DIR
from django.db import connection


def load_data_from_sql(filename):

    file_path = os.path.join(BASE_DIR, filename)
    sql_statements = open(file_path).read()
    with connection.cursor() as c:
        for statement in sql_statements.split(";"):
            c.execute(statement)

