import happybase
import pandas as pd

connection = happybase.Connection(host='localhost', port=9090)
tables = ['users', 'channels', 'videos', 'likes', 'views']

def create_tabel(name):
    try:
        connection.create_table(
            name,
            {
                'cfv': dict(max_versions=10)
            }
        )
    except Exception as error:
        if 'AlreadyExists' not in str(error):
            raise

print(connection.tables())

for table_name in tables:
    create_tabel(table_name)
    if table_name != 'videos':
        df = pd.read_parquet('../extract/' + table_name + '.parquet')
    else:
        df = pd.read_parquet('../transform/videos_with_views_and_likes.parquet')

    table = connection.table(table_name)
    columns = df.columns

    for i, row in df.iterrows():
        row_values = dict()
        for column in columns:
            row_values[f'cfv:{column}'.encode('utf-8')] = str(row[column]).encode('utf-8')

        table.put(
            str(row['id']).encode('utf-8'), row_values
        )

table = connection.table('videos')
for key, data in table.scan():
    print(key, '-->', data)






