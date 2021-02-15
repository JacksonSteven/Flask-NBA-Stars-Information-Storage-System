from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'Secret Key'
#设置数据库连接，给出数据库的url
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stars.sqlite3'
#设置数据库追踪信息,压制警告
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class stars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    height = db.Column(db.String(50))
    age = db.Column(db.String(10))
    level = db.Column(db.String(200))

    def __init__(self,name,height,age,level):
        self.name = name
        self.height = height
        self.age = age
        self.level = level

@app.route('/')  #app连接的路由，括号里是路径，/代表根目录
def home():
    all_info = stars.query.all()
    return render_template('home.html', stars = all_info) #渲染html模板

@app.route('/insert', methods=["POST"])  #app连接的路由，括号里是路径，/insert代表根目录
#怎么实现前端和后端交互？在前端插入数据，后端需要实现接收，并存入数据库、
def insert():
    if request.method == 'POST':
        name = request.form['name']
        height = request.form['height']
        age = request.form['age']
        level = request.form['level']

        insert_data = stars(name, height, age, level)
        db.session.add(insert_data)
        db.session.commit()
        return  redirect(url_for('home'))
    else:
        return  redirect(url_for('home' ))#若不是post请求，直接返回home

@app.route('/delete/<id>', methods=['GET','POST'])
def delete(id):
    delete_data = stars.query.get(id)
    db.session.delete(delete_data)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/update', methods=['GET','POST'])
def update():
    if request.method == "POST":
        update_id = request.form.get('id')
        update_data = stars.query.get(update_id)
        update_data.name = request.form['name']
        update_data.height = request.form['height']
        update_data.age = request.form['age']
        update_data.level = request.form['level']
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
