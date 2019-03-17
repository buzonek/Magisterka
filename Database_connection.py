import pyodbc


class Table(object):
    def __init__(self, name):
        self.name = name
        self.pk = None
        self.fk = []
        self.non_key_columns = []


class Database:
    ''' Singleton design pattern '''
    def __new__(cls, server, database):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def __init__(self, server, database):
        self.database = database
        self.server = server
        self.connection = pyodbc.connect(r"DRIVER={SQL Server Native Client 11.0};"
                                         r'SERVER=' + server + r';'
                                                               r';DATABASE=' + database + r';'
                                                                                          r'Trusted_Connection=yes')
        self.cursor = self.connection.cursor()

    def get_tb_detail(self, name):
        tb = Table(name)
        tb.pk = self.select_pk(tb.name)
        tb.fk = self.select_fk(tb.name)
        tb.non_key_columns = [key for key in self.get_table_columns(tb.name) if key not in tb.fk and key not in tb.pk]
        return tb

    def select_fk(self, table):
        sql_query = '''SELECT
                            COL_NAME(fc.parent_object_id,
                            fc.parent_column_id) AS ColumnName
                            FROM sys.foreign_keys AS f
                            LEFT JOIN sys.foreign_key_columns AS fc
                            ON f.OBJECT_ID = fc.constraint_object_id
                            WHERE OBJECT_NAME(fc.parent_object_id) = '{0}';'''.format(table)
        self.cursor.execute(sql_query)
        fk = [x.ColumnName for x in self.cursor.fetchall()]
        return fk

    def select_pk(self, table):
        sql_query = '''SELECT COLUMN_NAME
                        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                        WHERE OBJECTPROPERTY(OBJECT_ID(CONSTRAINT_SCHEMA + '.' 
                        + QUOTENAME(CONSTRAINT_NAME)), 'IsPrimaryKey') = 1
                        AND TABLE_NAME = '{0}' '''.format(table)
        self.cursor.execute(sql_query)
        pk = [x.COLUMN_NAME for x in self.cursor.fetchall()]
        # if len(pk) > 1:
        #     raise ValueError("Table {0} has more than one PK: {1}.".format(table, pk))
        return pk.pop()

    def get_tables_without_fk(self):
        """This function returns list of all tables names which don't have fk."""
        sql_query = '''SELECT tbl.name
        FROM sys.tables AS tbl
            LEFT JOIN sys.foreign_key_columns AS fKey
            ON tbl.object_id = fKey.parent_object_id
        WHERE fKey.parent_object_id IS NULL'''
        self.cursor.execute(sql_query)
        tables = [self.get_tb_detail(record.name) for record in self.cursor.fetchall()]
        return tables

    def get_tables_with_one_fk(self):
        """This function returns list of all tables names which have one fk."""
        sql_query = "SELECT TABLE_NAME from INFORMATION_SCHEMA.TABLE_CONSTRAINTS" \
                    " WHERE CONSTRAINT_TYPE = 'FOREIGN KEY'"
        self.cursor.execute(sql_query)
        all_tables = [x.TABLE_NAME for x in self.cursor.fetchall()]
        tables_names = [x for x in all_tables if all_tables.count(x) == 1]
        tables = [self.get_tb_detail(name) for name in tables_names]
        return tables

    def get_tables_with_many_fk(self):
        """This function returns list of all tables names which have many fk."""
        sql_query = "SELECT TABLE_NAME from INFORMATION_SCHEMA.TABLE_CONSTRAINTS" \
                    " WHERE CONSTRAINT_TYPE = 'FOREIGN KEY'"
        self.cursor.execute(sql_query)
        all_tables = [x.TABLE_NAME for x in self.cursor.fetchall()]
        tables_names = set([x for x in all_tables if all_tables.count(x) > 1])
        tables = [self.get_tb_detail(name) for name in tables_names]
        return tables

    def fetch_data_from_table(self, table_name):
        """This function gets table name as an argument and return iterator to all table rows."""
        sql_query = 'Select * from [{0}]'.format(table_name)
        self.cursor.execute(sql_query)
        row = self.cursor.fetchall()
        return row

    def get_table_columns(self, table):
        """This functions gets table name as an argument and returns list of all columns of this table."""
        sql_query = "SELECT COLUMN_NAME FROM {0}.INFORMATION_SCHEMA.COLUMNS" \
                    " WHERE TABLE_NAME = '{1}'".format(self.database, table)
        self.cursor.execute(sql_query)
        columns = [x.COLUMN_NAME for x in self.cursor.fetchall()]
        return columns

    def get_number_of_all_tables(self):
        """This functions returns number of all tables in the database."""
        sql_query = "SELECT COUNT(tbl.name) FROM sys.tables AS tbl"
        self.cursor.execute(sql_query)
        return self.cursor.fetchone()[0]

    def get_fk_detail(self, column):
        sql_query = '''SELECT
                tab1.name AS [table],
                col1.name AS [column],
                tab2.name AS [referenced_table],
                col2.name AS [referenced_column]
                FROM sys.foreign_key_columns fkc
                INNER JOIN sys.objects obj
                ON obj.object_id = fkc.constraint_object_id
                INNER JOIN sys.tables tab1
                ON tab1.object_id = fkc.parent_object_id
                INNER JOIN sys.schemas sch
                ON tab1.schema_id = sch.schema_id
                INNER JOIN sys.columns col1
                ON col1.column_id = parent_column_id AND col1.object_id = tab1.object_id
                INNER JOIN sys.tables tab2
                ON tab2.object_id = fkc.referenced_object_id
                INNER JOIN sys.columns col2
                ON col2.column_id = referenced_column_id AND col2.object_id = tab2.object_id
                WHERE col1.name = '{0}';'''.format(column)
        return self.cursor.execute(sql_query).fetchone()






# def get_columns(self, table, type):
    #     if type == 'pk':
    #         sql_query = '''SELECT COLUMN_NAME
    #                                 FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
    #                                 WHERE OBJECTPROPERTY(OBJECT_ID(CONSTRAINT_SCHEMA + '.' + QUOTENAME(CONSTRAINT_NAME)), 'IsPrimaryKey') = 1
    #                                 AND TABLE_NAME = '{0}' '''.format(table)
    #     elif type == 'fk':
    #         sql_query = '''SELECT
    #                                     COL_NAME(fc.parent_object_id,
    #                                     fc.parent_column_id) AS ColumnName
    #                                     FROM sys.foreign_keys AS f
    #                                     LEFT JOIN sys.foreign_key_columns AS fc
    #                                     ON f.OBJECT_ID = fc.constraint_object_id
    #                                     WHERE OBJECT_NAME(fc.parent_object_id) = '{0}';'''.format(table)
    #     elif type == 'normal':
    #         sql_query = '''
    #                         SELECT CONSTRAINT_COLUMN_USAGE from INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE WHERE TABLE_NAME = '{0}';'''.format(table)