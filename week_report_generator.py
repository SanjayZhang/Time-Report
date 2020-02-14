from datetime import date, timedelta
from db_mngr import DBMngr
from record_parser import RecordParser


class WeekReportGenerator:
    def __init__(self, week_begin):
        self.week_begin = week_begin
        self.db = DBMngr()

    def everyday_workload(self):
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
