from flask import Flask, render_template, request, redirect
#from gevent.pywsgi import WSGIServer
import model as db
import sys
import time

app = Flask(__name__)

@app.route("/")
def index():
    post = db.get_last_post()
    return render_template("index.html", last_post=post)

@app.route("/add")
def add():
    return render_template("add.html", action="write")

@app.route("/add", methods=["POST"])
def new_post():
    if request.method == "POST":
        title = request.form["title"]
        under_title = request.form["under_title"]
        author = request.form["author"]
        release = time.strftime("%H:%M/%m/%d/%Y")  # HH:MM/dd/mm/yyyy format
        content = request.form["content"]
        if db.add_post(title, under_title, author, release, content):
            print("Failed to add post to database!", file=sys.stderr)
            return render_template("add.html", post=1)
        else:  # successfull
            print("Successfully added post to database!", file=sys.stderr)
            return render_template("add.html", post=0)

@app.route("/posts")
def posts():
    posts = db.get_all_posts()
    return render_template("posts.html", posts=posts)


# @app.route("/register", methods=["POST"])
# def get_registration_data():
#     if request.method == "POST":  # only if website sends sth
#         email = request.form["email"]  # get userinput via HTML-form
#         username = request.form["username"]
#         if register_user(username, email):  # if sth is wrong with the db
#             print("Failed to register!", file=sys.stderr)
#             return render_template('register.html',
#                 action="register",
#                 status="Failed to register! Please try again!",
#                 status_color="#ff0033")
#         else:  # db check successfull
#             print("Successfully registered!", file=sys.stderr)
#             return render_template('register.html',
#                 action="finish",
#                 status="You have been successfully registered!",
#                 status_color="#08da94",
#                 username=username)

if __name__ == "__main__":
    db.check()
    # development/debugging (flask default):
    app.run(host="0.0.0.0", port=8000, debug=True)

    # basic server, ready for real-life usage [http://localhost:8000/]
    #server = WSGIServer(('0.0.0.0', 8000), app)
    #server.serve_forever()
