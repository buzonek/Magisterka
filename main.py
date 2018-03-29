from AVBTree import AVBTree
from Database_connection import DatabaseConnector
from Sensor import Sensor

sensory_input_fields = {}
db = DatabaseConnector('5CG6383BLC\MATEUSZ', 'Studenci')
tb = db.get_tables_without_fk()
for table in tb:
    all_columns = db.get_table_columns(table)
    fk_columns = db.select_fk(table)
    pk_columns = db.select_pk(table)
    no_pk_fk_columns = [x for x in all_columns if x not in fk_columns and x not in pk_columns]
    for column in no_pk_fk_columns:
        if column not in sensory_input_fields:
            sensory_input_fields[column] = AVBTree(column)

    for row in db.fetch_data_from_table(table):
        for column in no_pk_fk_columns:
            value = row.__getattribute__(column)
            if value is None:
                continue
            sensor = Sensor(value)
            sensory_input_fields[column].insert(sensor)
            #TODO
            #podmienić tak, żeby sensor wskazywał na obiekt który już istnieje jeśli już istnieje

    for column in no_pk_fk_columns:
        sensory_input_fields[column].print()
        print('-'*30)
