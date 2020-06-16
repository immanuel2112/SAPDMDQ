from imichael.wipro.datanxt.model.config_models import Table
from imichael.wipro.datanxt.persistence.persistence import Connection


def test_connection(sessiondetails) -> str:
    connection = Connection(sessiondetails)
    error_message = connection.test_connection()
    return error_message


def check_application_installation_Status(sessiondetails) -> int:
    connection = Connection(sessiondetails)
    app_db_exists = connection.check_application_installation_Status()
    print("appdbexists: " + str(app_db_exists))
    return app_db_exists


def install(sessiondetails) -> None:
    connection = Connection(sessiondetails)
    connection.install()


def get_table(sessiondetails, table_name) -> Table:
    connection = Connection(sessiondetails)
    table = connection.get_table(table_name)
    print("Table: " + str(table))
    return table