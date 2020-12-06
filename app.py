# Flask
from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

# SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

import datetime

class customer(db.Model):
    acc_no = db.Column(db.String(12), primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    amt = db.Column(db.Integer, nullable=False, default = 0)

    def __repr__(self):
        return f"{self.acc_no},{self.name},{self.amt}"

class transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acc_no = db.Column(db.String(12), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    amt = db.Column(db.Integer, nullable=False)
    date_time = db.Column(db.String(20), default = datetime.datetime.now().strftime("%d-%b-%Y %X"))

    def __repr__(self):
        return f"{self.acc_no},{self.name},{self.amt},{self.date_time}"

def getdata():
    db_obj = customer.query.all()
    cust_db_list = []
    for i in range(len(db_obj)):
        db_str = str(db_obj[i])
        cust_db_list.append(db_str.split(','))
        cust_db_list[i][2] = int(cust_db_list[i][2])
    
    db_obj = transaction.query.all()
    trans_db_list = []
    for i in range(len(db_obj)):
        db_str = str(db_obj[i])
        trans_db_list.append(db_str.split(','))
        trans_db_list[i][2] = int(trans_db_list[i][2])
    
    return cust_db_list,trans_db_list

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/banking',methods=['POST','GET'])
def banking():
    if request.method=='POST':
        # if request.form["button"]=="Confirm":
        acc = request.form['acc_no']
        name = request.form['name']
        amt = request.form['amt']
        main_acc = 'KDB100100012'
        cust,trans=getdata()
        trans_id = len(trans)+1
        try:
            db.session.query(customer).filter(customer.acc_no == main_acc).update({customer.amt:customer.amt - amt})
            db.session.commit()
            db.session.query(customer).filter(customer.acc_no == acc).update({customer.amt: customer.amt + amt})
            db.session.commit()
            new = transaction(id=trans_id,acc_no=acc,name=name,amt=amt)
            db.session.add(new)
            db.session.commit()
            db.session.commit()
            return redirect('/banking')
        except:
            return "Error in Transaction!"
    else:
        cust_db,trans_db = getdata()
        return render_template('main.html',cust_db=cust_db,trans_db=trans_db)

if __name__ == "__main__":
    app.run(debug=True)