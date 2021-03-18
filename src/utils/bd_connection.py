import psycopg2
import pandas as pd

# Параметры подключения к БД каталога
C_DB_NAME = "catalog_service_db"
C_USER_NAME = "catalog_service_reader"
C_PASSWD = "readonly"
C_HOST = "77.234.215.138"
C_PORT = "18095"

param_dict_catalog = {
    "database" : C_DB_NAME,
    "user" : C_USER_NAME,
    "password" : C_PASSWD,
    "host" : C_HOST,
    "port" : C_PORT
}

# Параметры подключения к нашей БД
M_DB_NAME = "ml3_recommendation_service_db"
M_USER_NAME = "ml3_recommendation_service"
M_PASSWD = "ml3_recommendation_pass"
M_HOST = "77.234.215.138"
M_PORT = "18095"


param_dict_ml3 = {
    "database" : M_DB_NAME,
    "user" : M_USER_NAME,
    "password" : M_PASSWD,
    "host" : M_HOST,
    "port" : M_PORT
}


## Основные функции для работы с БД ##

# Подключение
def connect(param_dict):
    connection = None
    
    try:
        print("Connecting to PostgreSQL database server...")
        connection = psycopg2.connect(**param_dict)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return -1
    
    print("Connection successfull")
    return connection


# Получение DataFrame по запросу к БД
def postgresql_to_dataframe(conn, select_query, column_names):
    cursor = conn.cursor()
    
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return -1
    
    rows = cursor.fetchall()
    cursor.close()
    
    df = pd.DataFrame(rows, columns=column_names)
    return df


# Создание таблицы в базе данных (не проверял на работоспособность!)
def create_table(conn, create_query):
    cursor = conn.cursor()
    
    try:
        cursor.execute(create_query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        print(error)
    
    cursor.close()
    print("Table created successfully!")
    

# Добавление (одной) новой строки в таблицу
def single_insert(conn, insert_query, params):
    cursor = conn.cursor()
    
    try:
        cursor.execute(insert_query, params)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        cursor.close()
        return -1
    
    cursor.close()
    
## Примеры работы с базой данных ##

# Просмотр доступных (public) таблиц в нашей БД
# ml3_conn = connect(param_dict_ml3)
# cursor = ml3_conn.cursor()
#
# cursor.execute("Select table_schema, table_name from information_schema.tables WHERE table_schema = 'public'")
# for table_info in cursor.fetchall():
#     print(" -", *table_info)
#     # Должны увидеть 2 таблицы:
#     # -wine_catalog_info — таблица данных из катлога (id, name, description, gastronomy)
#     # -wine_vectors — таблица векторизованных данных (id, name, vector)
#
# cursor.close()
# ml3_conn.close()
#
#
# # Получение векторизованных вин из нашей БД
# ml3_conn = connect(param_dict_ml3)
# vector_select_query = "SELECT * FROM wine_vectors"
#
# columns=["id", "name", "vector"]
# wine_vectors = postgresql_to_dataframe(ml3_conn, vector_select_query, columns)
#
# ml3_conn.close()
# wine_vectors.head())
#
# ## Дополнительно ##
#
# # Как превратить строку из таблицы в БД в вектор (list)
# s = wine_vectors['vector'][0]
# res = s.strip('][').replace("\n", "").replace(" ", "").split(",")
# res = [float(x) for x in res]
# print(f"Type: {type(res)} of {type(res[0])}\nLength: {len(res)}")