from flask import Flask,redirect,url_for,render_template,request,flash,session
from flask_pymongo import PyMongo


app=Flask(__name__)
app.secret_key="hfieufhwhwrhwhfh"

app.config["MONGO_URI"] = "mongodb://localhost:27017/Blog"
mongo = PyMongo(app)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/blog')
def blog():
	return render_template("blog.html")

@app.route('/article')
def article():
	return render_template("property-grid.html")

@app.route('/login')
def login():
	return render_template("login.html")

@app.route('/reg',methods=["POST"])
def reg():
	reg=mongo.db.register
	roll=reg.find_one({"roll":request.form["roll"]})
	print(roll)
	if roll is None:
		mongo.db.register.insert({"name":request.form["nm"],"roll":request.form["roll"],"password":request.form["pwd"]})
		flash("details sent to database")
		request.form={}
		return redirect(url_for("login"))
	else:
		return "user already exists"

@app.route('/log',methods=["POST"])
def log():
	reg=mongo.db.register
	roll=reg.find_one({"roll":request.form["logname"]})
	password=request.form["logpwd"]
	username=request.form["logname"]
	session["username"]=username
	if roll:
		if password==roll["password"]:
			request.form={}
			return render_template("user.html")
		else:
			request.form={}
			return "invalid password"
	else:
		request.form={}
		return "invalid username"

@app.route('/ckeditor',methods=["POST"])
def ckeditor():
	if "username" in session:
		username=session["username"]
		reg=mongo.db.register
		roll=reg.find_one({"roll":username})
		if "editor" in request.form:
			mongo.db.article.insert({"roll":username,"name":roll["name"],"article":request.form["editor"],"date":request.form["date"],"heading":request.form["head"]})
	return redirect(url_for("logout"))

@app.route('/getblog')
def getblog():
	print("blog working")
	article=mongo.db.article
	data=article.find()
	return render_template("blog.html",content=data)


@app.route('/logout')
def logout():
	session.pop("username",None)
	return redirect(url_for("index"))