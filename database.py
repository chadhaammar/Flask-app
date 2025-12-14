from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime , timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/vehicle_db.sqlite3' # Config to use sqlalchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Entry(db.Model):
    curr_entry_time = datetime.now().isoformat(' ', 'seconds')

    id = db.Column(db.Integer, primary_key=True)
    date_of_entry = db.Column("date_of_entry" , db.String(30) ,nullable = False , default= curr_entry_time)
    malade = db.Column("malade" , db.String(30) , nullable=False)
    status = db.Column("status" , db.String(20) , nullable=False)


    def __init__(self , malade , entry_dtime ,statu):
        self.malade = malade
        self.date_of_entry = entry_dtime
        self.status=statu 

    def __repr__(self):
        return f"{self.date_of_entry}|{self.malade}|{self.status}"

class DB_Manager():
    def __init__(self):
        self.db_connected = False
        self.db_data = []
        self.db_data_entries = []
        self.get_db_data()
        self.count = 0
        count = 0

    def create_db():
        db.create_all()

    def get_db_data(self):
        self.db_data = [] # Clear current db_data to get fresh fetch
        self.db_db = []
        self.allreg = []
        self.db_data_entries = [] # for LOG

        # Entries
        all_db_entries = Entry.query.all()
        self.count = 0
        for data in all_db_entries:
            data = str(data).split("|")
            self.count = self.count + 1 
            data_breakdown = {
                "id" : self.count,
                "date": data[0],
                "malade" : data[1],
                "status": data[2]
            }
            self.db_data_entries.insert(0,data_breakdown)

    def delete_pat(self , x):
        pat_to_delete = Entry.query.filter_by(malade = x).first()
        print(pat_to_delete)
        print(Entry)
        db.session.delete(pat_to_delete)
        db.session.commit()


if __name__ == '__main__':
    pass

    # ------------------------------ create db debug ----------------------------- #
    db.create_all() # Create DB when it doesnt exist

