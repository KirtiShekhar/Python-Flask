from flask import Flask,request,redirect
from flask import render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///toDoTask.db'
sqliteDatabase = SQLAlchemy(app)


class ToDoTask(sqliteDatabase.Model):
    taskId = sqliteDatabase.Column(sqliteDatabase.Integer, primary_key=True, nullable=False)
    taskName = sqliteDatabase.Column(sqliteDatabase.Text, nullable=False)
    taskStartDateTime = sqliteDatabase.Column(sqliteDatabase.Text, nullable=False, default=str(datetime.utcnow))
    taskEndDateTime = sqliteDatabase.Column(sqliteDatabase.Text, nullable=False, default=str(datetime.utcnow))

    def __repr__(self):
        return "taskId : " + str(
            self.taskId) + "\n" + "taskName : " + self.taskName + "\n" + "taskStartDateTime : " + \
               self.taskStartDateTime + "\n" + "taskEndDateTime : " + self.taskEndDateTime

@app.route('/task', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        postTaskName = request.form['taskName']
        postTaskStartDateTime = request.form['taskStartDateTime']
        postTaskEndDateTime = request.form['taskEndDateTime']
        sqliteDatabase.session.add(ToDoTask(taskName=postTaskName,taskStartDateTime=postTaskStartDateTime,taskEndDateTime=postTaskEndDateTime))
        sqliteDatabase.session.commit()
        return redirect('/task')
    else:
        ToDoTasksList = ToDoTask.query.all()
        return render_template('blogPostHome.html',ToDoTasksList=ToDoTasksList)


@app.route('/about')
def about():
    return render_template('blogPostAbout.html')\

@app.route('/delete/<int:taskId>/')
def delete(taskId):
    postTaskDelete = ToDoTask.query.get_or_404(taskId)
    sqliteDatabase.session.delete(postTaskDelete)
    sqliteDatabase.session.commit()
    return redirect('/task')


if __name__ == "__main__":
    app.run(debug=True)
