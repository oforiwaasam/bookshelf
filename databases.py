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
    col_names = ['Username', 'Interests', 'Favorite Authors',
                 'Currently Reading', 'Search History']
    dataframe = pd.DataFrame(columns=col_names)
    return dataframe


def db_to_dataframe(dbName, tableName, fileName):
    load_database(dbName, fileName)
    dataframe = pd.read_sql_table(tableName,
                                  con=create_engine_function(dbName))
    return dataframe


def put_values_personal_info_df(dataframe, id, username, email):
    dataframe.loc[len(dataframe.index)] = (id, username, email)
    return dataframe


def put_values_your_bookshelf_df(dataframe, username, interests, favorite_authors, currently_reading, search_history):
    dataframe.loc[len(dataframe.index)] = (username, interests, favorite_authors, currently_reading, search_history)
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
    else:
        personal_info_df = db_to_dataframe(dbName, personal_info_tableName, fileName)
        your_bookshelf_df = db_to_dataframe(dbName, your_bookshelf_tableName, fileName)

    # not sure why I had this here
    # dataframe.loc[len(dataframe.index)] = (id, username, 0, 0, 0)

    personal_info_df_final = put_values_personal_info_df(personal_info_df, id, username, email)
    your_bookshelf_df_final = put_values_your_bookshelf_df(your_bookshelf_df, username, None, None, None, None)

    # saving data to database and SQL file
    save_data_to_file(personal_info_df_final, dbName, personal_info_tableName, fileName)
    save_data_to_file(your_bookshelf_df_final, dbName, your_bookshelf_tableName, fileName)


# def update_score(username, correct):
#     tableName = 'user_data'
#     fileName = 'quiz_file'
#     dbName = 'quiz_db'
#     dataframe = db_to_dataframe(dbName, tableName, fileName)

#     # updating the fields in the dataframe
#     if correct:
#         dataframe.loc[dataframe['Username'] == username, ['Score']] += 1
#     dataframe.loc[dataframe['Username'] == username, ['Quizzes Done']] += 1
#     dataframe.loc[dataframe['Username'] == username,
#                   ['Questions Attempted']] += 1

#     # saving the new dataframe into the database
#     save_data_to_file(dataframe, dbName, tableName, fileName)


# def get_score(username):
#     tableName = 'user_data'
#     fileName = 'quiz_file'
#     dbName = 'quiz_db'
#     dataframe = db_to_dataframe(dbName, tableName, fileName)

#     # updating the fields in the dataframe
#     score = dataframe[dataframe['Username'] == username]['Score']
#     quizzes_done = dataframe[dataframe['Username'] == username]['Quizzes Done']
#     questions_attempted = dataframe[dataframe['Username'] == username]['Questions Attempted']
#     return int(score)


if __name__ == "__main__":
    main()
