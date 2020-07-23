from flask import Flask, render_template,url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)


class Task(db.Model):
	id= db.Column(db.Integer, primary_key =True)
	content = db.Column(db.String(200), nullable =False)
	date_c = db.Column(db.DateTime, default =datetime.utcnow)

	def __repr__(self):
		return '<Task %r>' % self.id



@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method=='POST':
		task_content = request.form['content']

		new_task = Task(content=task_content)

		try:
			db.session.add(new_task)
			db.session.commit()
			return redirect("/")
		except:
			return "There was an isssue adding your task !!!"
	else:
		tasks = Task.query.order_by(Task.date_c).all()
		return render_template("index.html", task =tasks)

 	

@app.route('/delete/<id>')
def delete(id):
	task = Task.query.get_or_404(id)

	try:
		db.session.delete(task)
		db.session.commit()
		return redirect('/')
	except:
		return "There was an isssue deleting your task !!!"


@app.route('/update/<id>', methods=['POST', 'GET'])
def update(id):
	task = Task.query.get_or_404(id)
	if request.method =='POST':
		task.content = request.form['content']
		try:
			db.session.commit()
			return redirect('/')
		except:
			return "There was an isssue updating your task !!!"
	else:
		return render_template('update.html', task=task)







if __name__ == "__main__":
	app.run(debug=True)

