from datetime import datetime

class Migration:
    id = 0
    name = ''
    created_on = datetime.now()

    def __init__(self) -> None:
        self.name = type(self).__name__

    def up(self) -> None: pass
    def down(self) -> None: pass

class InitialMigration20220716(Migration):

    def __init__(self) -> None:
        super().__init__()
    
    def up(self):
        return [
            'CREATE TABLE IF NOT EXISTS sorteos (id integer primary key, fecha datetime not null, numero1 int not null, numero2 int not null, numero3 int not null, numero4 int not null, numero5 int not null, estrella1 int not null, estrella2 int not null, bote int not null default 0, recaudacion int not null default 0, premios int not null default 0, millon string)',
            'CREATE TABLE IF NOT EXISTS configs (id integer primary key autoincrement, tag string not null, value string)',
            'CREATE TABLE IF NOT EXISTS migrations (id integer primary key autoincrement, name string not null, create_on datetime not null default CURRENT_TIMESTAMP )'
        ]
    def down(self):
        return [
            'DROP TABLE migrations',
            'DROP TABLE configs',
            'DROP TABLE sorteos'
        ]

migrations = [
    InitialMigration20220716(),
]