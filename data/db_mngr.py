import sqlite3
import os


class DBMngr:
    def __init__(self):
        self.db_name = 'records.db'
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()

    def create_db(self):
        # date format: yyyymmdd, duration unit: minute
        self.cur.execute(
            '''Create Table Records (
                    date int,
                    activity text,
                    duration int,
                    Primary Key (date, activity)
                )'''
        )
        
    def drop_db(self):
        os.remove(self.db_name)

    def insert(self, record):
        '''record is a tuple to be inserted '''
        insert_sql = 'Insert Into Records Values (?,?,?)'
        self.cur.execute(insert_sql, record)
        self.conn.commit()

    def insertmany(self, records):
        '''records is a list of tuple to be inserted'''
        insert_sql = 'Insert Into Records Values (?,?,?)'
        self.cur.executemany(insert_sql, records)
        self.conn.commit()


if __name__ == '__main__':
    m = DBMngr()
