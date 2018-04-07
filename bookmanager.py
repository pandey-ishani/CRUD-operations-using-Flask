import os

from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
SQLALCHEMY_TRACK_MODIFICATIONS = True
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)

@app.route("/update",methods=["POST"])
def update():
	newtitle = request.form.get("newtitle")
	oldtitle = request.form.get("oldtitle")
	book = Book.query.filter_by(title=oldtitle).first()
	book.title = newtitle
	db.session.commit()
	return redirect("/")

@app.route("/delete",methods=["POST"])
def delete():
	title = request.form.get("title")
	book = Book.query.filter_by(title=title).first()
	db.session.delete(book)
	db.session.commit()
	return redirect("/")


@app.route("/", methods=["GET", "POST"])
def home():
    books = None
    if request.form:
        try:
            book = Book(title=request.form.get("title"))
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            print(e)
    books = Book.query.all()
    return render_template("home.html", books=books)
  
if __name__ == "__main__":
    app.run(debug=True)