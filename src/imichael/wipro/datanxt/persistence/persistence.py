import pypyodbc as pyodbc

from imichael.wipro.datanxt.model.app_models import Table
from imichael.wipro.datanxt.persistence import queryconstants
from imichael.wipro.datanxt.utilities import applicationutility
from imichael.wipro.datanxt.utilities.applicationconstants import ApplicationConstants


class Connection:
    def __init__(self, sessiondetails):
        self.sessiondetails = sessiondetails
        self.buildconnectionstring()
        self.appconstants = ApplicationConstants()

    def buildconnectionstring(self) -> None:
        if len(self.sessiondetails.getUser()) == 0:
            self.connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=' + self.sessiondetails.getHost() + ';Database=master;Trusted_Connection=yes;'
        else:
            self.connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=' + self.sessiondetails.getHost() + ';Database=master;UID=' + self.sessiondetails.getUser() + ';PWD=' + self.sessiondetails.getPassword() + ';'

    def test_connection(self) -> str:
        errormessage = ""
        try:
            self.connection = pyodbc.connect(self.connection_string)
            self.connection.close()
        except (Exception) as error:
            errormessage = str(error)
        return errormessage

    def check_application_installation_Status(self) -> int:
        returnvalue = 0
        self.connection = pyodbc.connect(self.connection_string)
        cursor = self.connection.cursor()
        row = cursor.execute(
            queryconstants.APPLICATION_DB_EXISTS_SQL.format(
                APPLICATION_SYSTEM_DATABASE=queryconstants.APPLICATION_SYSTEM_DATABASE_VALUE)).fetchone()
        if row:
            print("db_name: " + str(row[0]))
            returnvalue = 1
        cursor.close()
        self.connection.close()
        return returnvalue

    def install(self) -> None:
        try:
            # Step 1: Create sdvSystemMaster database
            self.sessiondetails.writeToLog(
                msg="Start: Create application database: " + queryconstants.APPLICATION_SYSTEM_DATABASE_VALUE)
            self.create_database()
            self.sessiondetails.writeToLog(msg="Stop: Application database created successfully.")
            # Step 2: Create sdv System Master tables
            # self.sessiondetails.writeToLog("Create application tables.")
            # self.sessiondetails.writeToLog("Application tables created successfully.")
            # Step 2: Insert sdv System Master tables data
            # self.sessiondetails.writeToLogm,writeToLogm("Populate application default data.")
            # self.sessiondetails.writeToLog("Application default data populated successfully.")
        except (Exception) as error:
            errormessage = str(error)
            self.sessiondetails.writeToLog(msg=errormessage, error=True)

    def create_database(self) -> None:
        try:
            connection = pyodbc.connect(self.connection_string, autocommit=True)
            cursor = connection.cursor()
            # 1. Creating database
            self.sessiondetails.writeToLog(msg="1. Creating database")
            query = queryconstants.CREATE_DATABASE.format(DatabaseName=queryconstants.APPLICATION_SYSTEM_DATABASE_VALUE)
            SQL = queryconstants.EXECUTE_QUERY_IN_DB.format(
                DatabaseName=queryconstants.APPLICATION_SYSTEM_MASTER_DATABASE, query=query)
            print("SQL: " + SQL)
            cursor.execute(SQL)
            # 2. Set Collation property for the database
            self.sessiondetails.writeToLog(msg="2. Setting database collation property")
            query = queryconstants.DATABASE_COLLATE_PROPERTY.format(
                DatabaseName=queryconstants.APPLICATION_SYSTEM_DATABASE_VALUE)
            SQL = queryconstants.EXECUTE_QUERY_IN_DB.format(
                DatabaseName=queryconstants.APPLICATION_SYSTEM_MASTER_DATABASE, query=query)
            print("SQL: " + SQL)
            cursor.execute(SQL)
            # 3. Enable broker property for the database
            self.sessiondetails.writeToLog(msg="3. Setting database Enable broker property")
            query = queryconstants.DATABASE_ENABLE_BROKER_PROPERTY.format(
                DatabaseName=queryconstants.APPLICATION_SYSTEM_DATABASE_VALUE)
            SQL = queryconstants.EXECUTE_QUERY_IN_DB.format(
                DatabaseName=queryconstants.APPLICATION_SYSTEM_MASTER_DATABASE, query=query)
            print("SQL: " + SQL)
            cursor.execute(SQL)
            connection.close()
        except (Exception) as error:
            errormessage = str(error)
            self.sessiondetails.writeToLog(msg=errormessage, error=True)

    def get_table(self, page) -> Table:
        name = page.table
        table = Table(name)
        self.connection = pyodbc.connect(self.connection_string)
        cursor = self.connection.cursor()

        query = queryconstants.GET_OBJECT_COLUMNS.format(
            DatabaseName=queryconstants.APPLICATION_SYSTEM_DATABASE_VALUE, Object=name)
        header_row = cursor.execute(query).fetchall()
        formatted_header_row = applicationutility.convert_resultset_to_list(header_row)
        table.set_fields(formatted_header_row)

        where_clause = ""
        if page.filter_field is not None:
            where_clause = "WHERE "+page.filter_field+ " = '"+page.filter_field_value+"'"

        query = queryconstants.GET_OBJECT_DATA.format(
            DatabaseName=queryconstants.APPLICATION_SYSTEM_DATABASE_VALUE, Object=name,
            WhereClause=where_clause)

        print(query)
        data_row = cursor.execute(query).fetchall()
        table.set_data(data_row)

        if data_row is not None:
            table.set_record_count(len(data_row))

        cursor.close()
        self.connection.close()
        return table