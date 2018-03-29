import pyodbc


class DatabaseConnector:
    def __init__(self, server, database):
        self.database = database
        self.server = server
        self.connection = pyodbc.connect(r"DRIVER={SQL Server Native Client 11.0};"
                                         r'SERVER=' + server + r';'
                                         r';DATABASE=' + database + r';'
                                         r'Trusted_Connection=yes')
        self.cursor = self.connection.cursor()

    def select_fk(self, table):
        sql_statement = '''SELECT
                            COL_NAME(fc.parent_object_id,
                            fc.parent_column_id) AS ColumnName
                            FROM sys.foreign_keys AS f
                            LEFT JOIN sys.foreign_key_columns AS fc
                            ON f.OBJECT_ID = fc.constraint_object_id
                            WHERE OBJECT_NAME(fc.parent_object_id) = '{0}';'''.format(table)
        self.cursor.execute(sql_statement)
        fk = [x.ColumnName for x in self.cursor.fetchall()]
        return fk

    def select_pk(self, table):
        sql_statement = '''SELECT COLUMN_NAME
                        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                        WHERE OBJECTPROPERTY(OBJECT_ID(CONSTRAINT_SCHEMA + '.' + QUOTENAME(CONSTRAINT_NAME)), 'IsPrimaryKey') = 1
                        AND TABLE_NAME = '{0}' '''.format(table)

        self.cursor.execute(sql_statement)
        pk = [x.COLUMN_NAME for x in self.cursor.fetchall()]
        return pk

    # def get_columns(self, table, type):
    #     if type == 'pk':
    #         sql_statement = '''SELECT COLUMN_NAME
    #                                 FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
    #                                 WHERE OBJECTPROPERTY(OBJECT_ID(CONSTRAINT_SCHEMA + '.' + QUOTENAME(CONSTRAINT_NAME)), 'IsPrimaryKey') = 1
    #                                 AND TABLE_NAME = '{0}' '''.format(table)
    #     elif type == 'fk':
    #         sql_statement = '''SELECT
    #                                     COL_NAME(fc.parent_object_id,
    #                                     fc.parent_column_id) AS ColumnName
    #                                     FROM sys.foreign_keys AS f
    #                                     LEFT JOIN sys.foreign_key_columns AS fc
    #                                     ON f.OBJECT_ID = fc.constraint_object_id
    #                                     WHERE OBJECT_NAME(fc.parent_object_id) = '{0}';'''.format(table)
    #     elif type == 'normal':
    #         sql_statement = '''
    #                         SELECT CONSTRAINT_COLUMN_USAGE from INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE WHERE TABLE_NAME = '{0}';'''.format(table)

    def get_tables_without_fk(self):
        """This function returns list of all tables names which don't have fk."""
        sql_statement = '''SELECT tbl.name
        FROM sys.tables AS tbl
            LEFT JOIN sys.foreign_key_columns AS fKey
            ON tbl.object_id = fKey.parent_object_id
        WHERE fKey.parent_object_id IS NULL'''
        self.cursor.execute(sql_statement)
        tables_names = [x.name for x in self.cursor.fetchall()]
        return tables_names

    def get_tables_with_one_fk(self):
        """This function returns list of all tables names which have one fk."""
        sql_statement = "SELECT TABLE_NAME from INFORMATION_SCHEMA.TABLE_CONSTRAINTS" \
                        " WHERE CONSTRAINT_TYPE = 'FOREIGN KEY'"
        self.cursor.execute(sql_statement)
        all_tables = [x.TABLE_NAME for x in self.cursor.fetchall()]
        tables_names = [x for x in all_tables if all_tables.count(x) == 1]
        return tables_names

    def get_tables_with_many_fk(self):
        """This function returns list of all tables names which have many fk."""
        sql_statement = "SELECT TABLE_NAME from INFORMATION_SCHEMA.TABLE_CONSTRAINTS" \
                        " WHERE CONSTRAINT_TYPE = 'FOREIGN KEY'"
        self.cursor.execute(sql_statement)
        all_tables = [x.TABLE_NAME for x in self.cursor.fetchall()]
        tables_names = set([x for x in all_tables if all_tables.count(x) > 1])
        return list(tables_names)

    def fetch_data_from_table(self, table_name):
        """This function gets table name as an argument and return iterator to all table rows."""
        sql_statement = 'Select * from {0}'.format(table_name)
        self.cursor.execute(sql_statement)
        row = self.cursor.fetchone()
        while row:
            yield row
            row = self.cursor.fetchone()

    def get_table_columns(self, table):
        """This functions gets table name as an argument and returns list of all columns of this table."""
        sql_statement = "SELECT COLUMN_NAME FROM {0}.INFORMATION_SCHEMA.COLUMNS" \
                        " WHERE TABLE_NAME = '{1}'".format(self.database, table)
        self.cursor.execute(sql_statement)
        columns = [x.COLUMN_NAME for x in self.cursor.fetchall()]
        return columns

    def get_number_of_all_tables(self):
        """This functions returns number of all tables in the database."""
        sql_statement = "SELECT COUNT(tbl.name) FROM sys.tables AS tbl"
        self.cursor.execute(sql_statement)
        return self.cursor.fetchone()[0]
