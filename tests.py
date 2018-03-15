from unittest import TestCase, main
from Database_connection import DatabaseConnector
from AVBTree import AVBTree


class DatabaseConnection(TestCase):
    def test_getting_tables_northwind(self):
        connection = DatabaseConnector('5CG6383BLC\MATEUSZ', 'Northwind')
        tb_no_fk = connection.get_tables_without_fk()
        tb_one_fk = connection.get_tables_with_one_fk()
        tb_many_fk = connection.get_tables_with_many_fk()
        self.assertEqual(connection.get_number_of_all_tables(), len(tb_no_fk)+len(tb_many_fk)+len(tb_one_fk))

    def test_getting_tables_adventure(self):
        connection = DatabaseConnector('5CG6383BLC\MATEUSZ', 'AdventureWorks2012')
        tb_no_fk = connection.get_tables_without_fk()
        tb_one_fk = connection.get_tables_with_one_fk()
        tb_many_fk = connection.get_tables_with_many_fk()
        self.assertEqual(connection.get_number_of_all_tables(), len(tb_no_fk)+len(tb_many_fk)+len(tb_one_fk))

    def test_strings_ok(self):
        values = ['Amy', 'Rose', 'Kate', 'Lisa', 'Sara', 'Kate', 'Tom', 'Jack', 'Lisa', 'Tom', 'Kate', 'Amy', 'Jack',
                  'Nina', 'Tom', 'Tom', 'Emy', 'Lisa', 'Paula']
        tree = AVBTree()
        for value in values[:]:
            tree.insert(value)
        for value in values[:]:
            self.assertEqual(tree.search(value).value, value)

    def test_strings_nok(self):
        values = ['Amy', 'Rose', 'Kate', 'Lisa', 'Sara', 'Kate', 'Tom', 'Jack', 'Lisa', 'Tom', 'Kate', 'Amy', 'Jack',
                  'Nina', 'Tom', 'Tom', 'Emy', 'Lisa', 'Paula']
        tree = AVBTree()
        for value in values[:]:
            tree.insert(value)
        for value in values[:]:
            self.assertNotEqual(tree.search('Mateusz'), value)

    def test_numbers_ok(self):
        import random
        values = []
        tree = AVBTree()
        for i in range(100):
            values.append(random.randint(0, 100000))
            tree.insert(values[i])
        for value in values:
            self.assertEqual(tree.search(value).value, value)

    def test_numbers_nok(self):
        import random
        values = []
        tree = AVBTree()
        for i in range(200):
            values.append(random.randint(0, 100))
            tree.insert(values[i])
        self.assertEqual(tree.search(101), None)

if __name__ == '__main__':
    main()


