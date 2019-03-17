from AVBTree import AVBTree
from Database_connection import Database
from Sensor import Sensor
from ValueNeuron import ObjectNeuron


config = {
    'server': 'PL-00001716',
    'database': 'studenci'
}


class DASNG(object):
    # __shared_state = {} #zmienna współdzielona między wszystkimi klasami
    database = None

    def __init__(self):
        self.sensory_input_fields = {}

    def print(self):
        for field_name, field_avb_tree in self.sensory_input_fields.items():
            print(field_name)
            field_avb_tree.print()
            print("*"*50)

    def convert_db(self, server, database):
        if not self.database:
            self.database = Database(server, database)
        tables = self.database.get_tables_without_fk()
        tables.extend(self.database.get_tables_with_one_fk())
        tables.extend(self.database.get_tables_with_many_fk())
        for table in tables:
            self.retrieve_sensory_input_fields(table)
            self.convert_table(table)

    def retrieve_sensory_input_fields(self, table):
        for column in table.non_key_columns:
            if column not in self.sensory_input_fields:
                self.sensory_input_fields[column] = AVBTree(column)

    def convert_table(self, table):
        rows = self.database.fetch_data_from_table(table.name)
        for row in rows:
            # Fetch ID of table entry
            id = row.__getattribute__(table.pk)

            # creates Neuron with ID value
            ID = ObjectNeuron(id)

            # iterate over each column which is neither primary key nor foreign key
            for column in table.non_key_columns:
                value = row.__getattribute__(column)
                if value is None:
                    continue

                # creates and inserts sensor into SIF
                sensor = self.sensory_input_fields[column].insert(Sensor(value))

                # connects each sensor with ID neuron
                sensor.value_neuron.connect(ID)

            # iterates over each column which is foreign key
            for column in table.fk:
                fk_value = row.__getattribute__(column)
                if not fk_value:
                    continue
                fk_detail = self.database.get_fk_detail(column)
                tb_detail = self.database.get_tb_detail(fk_detail.referenced_table)
                if fk_detail.referenced_table != fk_detail.table:
                    sql_query = '''Select [{5}] from [{0}]
                          LEFT JOIN [{1}]
                          ON [{0}].[{2}] = [{1}].[{3}]
                          WHERE [{0}].[{2}] = '{4}';'''.format(fk_detail.referenced_table, fk_detail.table, fk_detail.referenced_column, fk_detail.column, fk_value, tb_detail.non_key_columns[0])
                else:
                    sql_query = '''Select [{3}] from {0}
                                              WHERE [{1}] = '{2}';'''.format(fk_detail.referenced_table,
                                                                           fk_detail.referenced_column, fk_value, tb_detail.non_key_columns[0])
                res = self.database.cursor.execute(sql_query).fetchall()[0][0]
                try:
                    ref_IDNeuron = self.sensory_input_fields[tb_detail.non_key_columns[0]].search(res).value_neuron.connections[fk_value]
                except Exception as e:
                    print(e)
                    rows.append(row)
                else:
                    ID.connect(ref_IDNeuron)


if __name__ == "__main__":
    dasng = DASNG()
    dasng.convert_db(server=config['server'], database=config['database'])
    dasng.print()
