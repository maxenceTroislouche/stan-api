import mysql.connector

class DatabaseConnection:
    def __init__(self) -> None:
        self.__host = "localhost"
        self.__user = "stan"
        self.__passwd = "stan"
        self.__database = "stan"

        self.__conn = mysql.connector.connect(
            host=self.__host,
            user=self.__user,
            passwd=self.__passwd,
            database=self.__database
        )

    def execute_select(self, query: str):
        cursor = self.__conn.cursor()
        cursor.execute(query)

        array = []
        for x in cursor:
            array.append(x)

        return array
    
    def execute_query(self, query: str):
        cursor = self.__conn.cursor()

        cursor.execute(query)
        self.__conn.commit()