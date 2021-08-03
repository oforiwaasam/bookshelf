import pandas as pd
import sqlalchemy
import os
from sqlalchemy import create_engine


def create_engine_function(dbName):
    # Create an engine
    return create_engine('mysql://root:codio@localhost/'
                         + dbName + '?charset=utf8', encoding='utf-8')


def save_data_to_file(dtfr, dbName, tableName, fileName):
    dtfr.to_sql(tableName, con=create_engine_function(dbName),
                if_exists='replace', index=False)
    os.system('mysqldump -u root -pcodio {} > /home/codio/workspace/bookshelf/{}.sql'.format(dbName, fileName))


def load_database(dbName, fileName):
    os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS '
              + dbName + '; "')
    os.system('mysql -u root -pcodio ' + dbName + ' < /home/codio/workspace/bookshelf/' + fileName + '.sql')


def create_personal_info_df():
    col_names = ['id', 'Username', 'Email']
    dataframe = pd.DataFrame(columns=col_names)
    return dataframe


# store user_data related to their activity on the website
def create_your_bookshelf_df():
    col_names = ['Username', 'Variable Type', 'Variable Value']
                 # 'Interests', 'Favorite Authors', 'Currently Reading']
    dataframe = pd.DataFrame(columns=col_names)
    return dataframe


def create_search_history_df():
    tableName = 'search_history'
    fileName = 'user_data'
    dbName = 'bookshelf_db'
    col_names = ['Username', 'Type of Search', 'Searched Item']
    dataframe = pd.DataFrame(columns=col_names)
    save_data_to_file(dataframe, dbName, tableName, fileName)
    return dataframe


def db_to_dataframe(dbName, tableName, fileName):
    load_database(dbName, fileName)
    dataframe = pd.read_sql_table(tableName,
                                  con=create_engine_function(dbName))
    return dataframe


def put_values_personal_info_df(dataframe, id, username, email):
    dataframe.loc[len(dataframe.index)] = (id, username, email)
    return dataframe


def put_values_your_bookshelf_df(dataframe, username, variable_type, variable_value):
    dataframe.loc[len(dataframe.index)] = (username, variable_type, variable_value)
    return dataframe


def put_values_search_history_df(dataframe, username, search_type, searched_item):
    dataframe.loc[len(dataframe.index)] = (username, search_type, searched_item)
    return dataframe


def new_user(id, username, email):
    personal_info_tableName = 'personal_info'
    your_bookshelf_tableName = 'your_bookshelf'
    fileName = 'user_data'
    dbName = 'bookshelf_db'

    # if our program has never been used, create dataframes
    if id == 1:
        personal_info_df = create_personal_info_df()
        your_bookshelf_df = create_your_bookshelf_df()
        create_search_history_df()
    else:
        personal_info_df = db_to_dataframe(dbName, personal_info_tableName, fileName)
        your_bookshelf_df = db_to_dataframe(dbName, your_bookshelf_tableName, fileName)

    # not sure why I had this here
    # dataframe.loc[len(dataframe.index)] = (id, username, 0, 0, 0)

    personal_info_df_final = put_values_personal_info_df(personal_info_df, id, username, email)
    your_bookshelf_df_final = put_values_your_bookshelf_df(your_bookshelf_df, username, None, None)

    # saving data to database and SQL file
    save_data_to_file(personal_info_df_final, dbName, personal_info_tableName, fileName)
    save_data_to_file(your_bookshelf_df_final, dbName, your_bookshelf_tableName, fileName)


def update_search_history(username, search_type, searched_item):
    tableName = 'search_history'
    fileName = 'user_data'
    dbName = 'bookshelf_db'
    dataframe = db_to_dataframe(dbName, tableName, fileName)

    # adding another row for this search
    dtfr_final = put_values_search_history_df(dataframe, username, search_type, searched_item)

    # saving the new dataframe into the database
    save_data_to_file(dtfr_final, dbName, tableName, fileName)


def update_bookshelf(username, variable_type, variable_value):
    tableName = 'your_bookshelf'
    fileName = 'user_data'
    dbName = 'bookshelf_db'
    dataframe = db_to_dataframe(dbName, tableName, fileName)

    # updating the bookshelf
    dtfr_final = put_values_your_bookshelf_df(dataframe, username, variable_type, variable_value)

    # saving the new dataframe into the database
    save_data_to_file(dtfr_final, dbName, tableName, fileName)


# to be called in main.py
def update_interests(username, variable_value):
    update_bookshelf(username, 'Interests', variable_value)
    

# to be called in main.py
def update_fav_authors(username, variable_value):
    update_bookshelf(username, 'Favorite Authors', variable_value)


# to be called in main.py
def update_currently_reading(username, variable_value):
    update_bookshelf(username, 'Currently Reading', variable_value)


def get_user_bookshelf(username, variable_type):
    tableName = 'your_bookshelf'
    fileName = 'user_data'
    dbName = 'bookshelf_db'
    dataframe = db_to_dataframe(dbName, tableName, fileName)

    # select rows corresponding to specified variable type
    spec_dataframe = dataframe[dataframe['Variable Type'] == variable_type]
    
    # put results in a list
    results = []
    for index, row in spec_dataframe.iterrows():
        results.append(row['Variable Value'])

    # put results in a dictionary to return
    user_dict = {}
    user_dict[variable_type] = results

    return user_dict


# to be called in main.py
def get_user_interests(username):
    return get_user_bookshelf(username, 'Interests')
    

# to be called in main.py
def get_user_fav_authors(username):
    return get_user_bookshelf(username, 'Favorite Authors')


# to be called in main.py
def _currently_reading(username):
    return get_user_bookshelf(username, 'Currently Reading')

# def main():
#     create_search_history_df()
#     print(get_user_interests('hey'))


if __name__ == "__main__":
    main()
