
def tableExists(tablename, connection):
    cursor = connection.cursor()
    instruccion = f'SELECT COUNT(*) as cou FROM sqlite_master WHERE type=\'table\' AND name=\'{tablename}\''
    for row in cursor.execute(instruccion):
        return row[0] > 0