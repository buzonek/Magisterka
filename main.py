from AVBTree import AVBTree
from Database_connection import DatabaseConnector
from Sensor import Sensor
from ValueNeuron import ValueNeuron, IDNeuron


class DASNG(object):
    def __init__(self, server, database):
        self.sensory_input_fields = {}
        self.db = DatabaseConnector(server, database)
        self.convert_db()

    def print(self):
        for field_name, items in self.sensory_input_fields.items():
            print(field_name)
            items.print()
            print("*"*50)

    def convert_db(self, ):
        tables = self.db.get_tables_without_fk()
        for table in tables:
            self.convert_table(table)
        tables = self.db.get_tables_with_one_fk()
        for table in tables:
            self.convert_table(table)
        tables = self.db.get_tables_with_many_fk()
        for table in tables:
            self.convert_table(table)

    def convert_table(self, table):
        for column in table.non_key_columns:
            if column not in self.sensory_input_fields:
                self.sensory_input_fields[column] = AVBTree(column)

        rows = self.db.fetch_data_from_table(table.name)
        for row in rows:
            id = row.__getattribute__(table.pk)
            ID = IDNeuron(id)
            for column in table.non_key_columns:
                value = row.__getattribute__(column)
                if value is None:
                    continue
                sensor = self.sensory_input_fields[column].insert(Sensor(value))
                if sensor.count == 1:
                    val_neuron = ValueNeuron(value)
                    sensor.value_neuron = val_neuron
                    val_neuron.connections[sensor.value] = sensor
                sensor.value_neuron.connections[id] = ID
                ID.connections[sensor.value_neuron.value] = sensor.value_neuron
            for column in table.fk:
                fk_value = row.__getattribute__(column)
                if fk_value:
                    fk = self.db.get_fk_detail(column)
                    tb_detail = self.db.create_table(fk.referenced_table)
                    if fk.referenced_table != fk.table:
                        sql = '''Select [{5}] from [{0}]
                              LEFT JOIN [{1}]
                              ON [{0}].[{2}] = [{1}].[{3}]
                              WHERE [{0}].[{2}] = '{4}';'''.format(fk.referenced_table, fk.table, fk.referenced_column, fk.column, fk_value, tb_detail.non_key_columns[0])
                    else:
                        sql = '''Select [{3}] from {0}
                                                  WHERE [{1}] = '{2}';'''.format(fk.referenced_table,
                                                                               fk.referenced_column, fk_value, tb_detail.non_key_columns[0])
                    res = self.db.cursor.execute(sql).fetchall()[0][0]
                    try:
                        referenced_IDNeuron = self.sensory_input_fields[tb_detail.non_key_columns[0]].search(res).value_neuron.connections[fk_value]
                    except Exception as e:
                        #TODO W Northwind wywala się do czasu do czasu(?)
                        print(e)
                        rows.append(row)
                    else:
                        ID.connections[referenced_IDNeuron.value] = referenced_IDNeuron
                        referenced_IDNeuron.connections[ID.value] = ID
                        # print(ID, ID.connections)

if __name__ == "__main__":
    dasng = DASNG('5CG6383BLC\MATEUSZ', 'Northwind')
    dasng.print()
