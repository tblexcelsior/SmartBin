from datetime import datetime
import mysql.connector as mdb
HOST = 'localhost'
DATABASE = 'smart_bin'
USER = 'tblexcel'
PASSWORD = 'tblexcelsior'
# a = datetime.today().strftime('%Y-%m-%d')
# print(a)


# conn = mdb.connect(host = HOST,
#                     database = DATABASE,
#                     user = USER,
#                     password = PASSWORD)
# curr = conn.cursor()
# # query = """select * from daily_statistic where id = (select max(id) from daily_statistic);"""
# query = """SELECT * FROM (
#             SELECT * FROM daily_statistic ORDER BY id DESC LIMIT 3) as r ORDER BY id"""
# curr.execute(query)
# current_date = list(curr.fetchall())
# data_1 = list(current_date[0])[2:]
# print(current_date)
# print(data_1)
a = datetime.today().strftime('%y,%m,%d')
# a = [int(i) for i in a]
# # print(type(a))
print(a)
# # print(a == current_date)
# # query = """insert into daily_statistic (time, g7, g8, g9, g10, g11, g12, g13, g14, g15, g16, g17) 
#                                     # values ("2022-08-17", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);"""
# # curr.execute(query)
# # conn.commit()
# curr.close()
# conn.close()

# conn = mdb.connect(host = HOST,
#                     database = DATABASE,
#                     user = USER,
#                     password = PASSWORD)
# curr = conn.cursor()
# query = """select g_type, month(updated_time) as month, count(g_type) as total 
#            from garbage_statistic where year(updated_time) = year(current_date())  
#            group by  g_type, month(updated_time);"""
# curr.execute(query)
# current_date = list(curr.fetchall())
# curr.close()
# conn.close()
# print(current_date)
# init_data = [0,0,0,0,0,0,0,0,0,0,0,0]
# data_list = {'1':init_data, '2':init_data, '3': init_data}
# # # print(type(data_list['1']))
# for item in current_date:
#     if item[0] == '2':
#         data_list['2'][item[1] - 1] = item[2]

# print(data_list['2'])

# def num_daily_garbage(type):
#     conn = mdb.connect(host = HOST,
#                     database = DATABASE,
#                     user = USER,
#                     password = PASSWORD)
#     curr = conn.cursor()
#     query = """select g_type, hour(updated_time) as hour, count(g_type) as 
#             total from garbage_statistic where day(updated_time) = day(current_date()) 
#             and hour(updated_time) between 8 and 19 group by g_type, hour(updated_time);"""
#     curr.execute(query)
#     current_date = list(curr.fetchall())
#     curr.close()
#     conn.close()
#     init_data = [0,0,0,0,0,0,0,0,0,0,0,0]
#     data_list = {'1':init_data, '2':init_data, '3': init_data}
#     for item in current_date:
#         if item[0] == type:
#             data_list[type][item[1] - 8] = item[2]
#     return data_list[type]

# type1_data = num_daily_garbage('3')
# print(type1_data)

# conn = mdb.connect(host = HOST,
#                     database = DATABASE,
#                     user = USER,
#                     password = PASSWORD)
# curr = conn.cursor()
# # query = """select * from daily_statistic where id = (select max(id) from daily_statistic);"""
# query = """SELECT * FROM processing"""
# curr.execute(query)
# current_date = list(curr.fetchall()[0])[1]
# print(current_date)