from datetime import date, timedelta
from db_mngr import DBMngr
from record_parser import RecordParser


class ReportGenerator:
    def __init__(self):
        self.db = DBMngr()
        self.begin_date = None
        self.end_date = None

    def __init__(self, begin_date, end_date):
        self.db = DBMngr()
        self.begin_date = begin_date 
        self.end_date = end_date

    def set_begin_date(self, date):
        self.begin_date = date
        
    def set_end_date(self, date):
        self.end_date = date

    def everyday_workload(self, begin=self.begin_date, days=None):
        if days = None:
            days = (self.end_date - self.begin_date).days
        

        workloads = []
        
        for i in range(7):
            workloads.append(
                self.db.cur.execute(
                    'select sum(duration) from Records where date = ?',
                    (self.week_begin + timedelta(days=i),)
                ).fetchone()[0]
            )
        return workloads

    def time_spent_on_every_activity(self):
        all_activities = list(self.db.cur.execute (
                'Select Distinct Activity From Records'
            ).fetchall()
        )

        days = [str(self.week_begin + timedelta(days=i)) for i in range(7)]

        query = '''Select Activity, Sum(Duration) as total_duration
                From Records 
                Where 
                Date In ({})
                Group By Activity
                Order By total_duration DESC
                '''.format(','.join(['?']*len(days)))

        return self.db.cur.execute(query, tuple(days)).fetchall()

            
if __name__ == '__main__':
    w = WeekReportGenerator(date.fromisoformat('2019-09-02'))
    result = w.time_spent_on_every_activity()
    print(result)
