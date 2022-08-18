from datetime import datetime
import mysql.connector as mdb
HOST = 'localhost'
DATABASE = 'smart_bin'
USER = 'tblexcel'
PASSWORD = 'tblexcelsior'
# a = datetime.today().strftime('%Y-%m-%d')
# print(a)


conn = mdb.connect(host = HOST,
                    database = DATABASE,
                    user = USER,
                    password = PASSWORD)
curr = conn.cursor()
# query = """select * from daily_statistic where id = (select max(id) from daily_statistic);"""
query = """SELECT * FROM (
            SELECT * FROM daily_statistic ORDER BY id DESC LIMIT 3) as r ORDER BY id"""
curr.execute(query)
current_date = list(curr.fetchall())
data_1 = list(current_date[0])[2:]
print(current_date)
print(data_1)
# a = datetime.today().strftime('%Y-%m-%d')
# print(type(a))
# print(a)
# print(a == current_date)
# query = """insert into daily_statistic (time, g7, g8, g9, g10, g11, g12, g13, g14, g15, g16, g17) 
                                    # values ("2022-08-17", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);"""
# curr.execute(query)
# conn.commit()
curr.close()
conn.close()
