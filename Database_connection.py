import pyodbc

cnxn = pyodbc.connect(r"DRIVER={SQL Server Native Client 11.0};"
                      r'SERVER=5CG6383BLC\MATEUSZ;'
                      r'DATABASE=TestDatabase;'
                      r'Trusted_Connection=yes'
                      )
cursor = cnxn.cursor()
cursor.execute("Select * from Sales")
row = cursor.fetchone()
while row:
    print(row[0])
    row = cursor.fetchone()
