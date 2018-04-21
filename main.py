from AVBTree import AVBTree
from Database_connection import DatabaseConnector
from Sensor import Sensor
from ValueNeuron import ValueNeuron, ObjectNeuron


class DASNG(object):
    def __init__(self, server, database):
        self.sensory_input_fields = {}
        self.db = DatabaseConnector(server, database)
        self.convert_db()

    def print(self):
        for field_name, field_avb_tree in self.sensory_input_fields.items():
            print(field_name)
            field_avb_tree.print()
            print("*"*50)

    def convert_db(self, ):
        tables = self.db.get_tables_without_fk()
        tables.extend(self.db.get_tables_with_one_fk())
        tables.extend(self.db.get_tables_with_many_fk())
        for table in tables:
            self.convert_table(table)

    def convert_table(self, table):
        for column in table.non_key_columns:
            if column not in self.sensory_input_fields:
                self.sensory_input_fields[column] = AVBTree(column)

        rows = self.db.fetch_data_from_table(table.name)
        for row in rows:
            id = row.__getattribute__(table.pk)
            ID = ObjectNeuron(id)
            for column in table.non_key_columns:
                value = row.__getattribute__(column)
                if value is None:
                    continue
                sensor = self.sensory_input_fields[column].insert(Sensor(value))
                if sensor.count == 1:
                    sensor.value_neuron = ValueNeuron(value)
                    sensor.value_neuron.sensor = sensor
                sensor.value_neuron.connect(ID)
            for column in table.fk:
                fk_value = row.__getattribute__(column)
                if fk_value:
                    fk_detail = self.db.get_fk_detail(column)
                    tb_detail = self.db.get_tb_detail(fk_detail.referenced_table)
                    if fk_detail.referenced_table != fk_detail.table:
                        sql = '''Select [{5}] from [{0}]
                              LEFT JOIN [{1}]
                              ON [{0}].[{2}] = [{1}].[{3}]
                              WHERE [{0}].[{2}] = '{4}';'''.format(fk_detail.referenced_table, fk_detail.table, fk_detail.referenced_column, fk_detail.column, fk_value, tb_detail.non_key_columns[0])
                    else:
                        sql = '''Select [{3}] from {0}
                                                  WHERE [{1}] = '{2}';'''.format(fk_detail.referenced_table,
                                                                               fk_detail.referenced_column, fk_value, tb_detail.non_key_columns[0])
                    res = self.db.cursor.execute(sql).fetchall()[0][0]
                    try:
                        referenced_IDNeuron = self.sensory_input_fields[tb_detail.non_key_columns[0]].search(res).value_neuron.connections[fk_value]
                    except Exception as e:
                        #TODO W Northwind wywala się do czasu do czasu(?)
                        print(e)
                        rows.append(row)
                    else:
                        ID.connect(referenced_IDNeuron)

if __name__ == "__main__":
    dasng = DASNG('5CG6383BLC\MATEUSZ', 'Studenci')
    dasng.print()
