from flask import Flask, render_template, request, redirect
#from gevent.pywsgi import WSGIServer
import model as db
import sys
import time, calendar

def get_date(date):
    date = date.split("/")
    time = str(date[0])
    day_str = calendar.day_name[calendar.weekday(int(date[3]), int(date[2]), int(date[1]))]  # .day_abbr[]
    day_num = str(int(date[1]))
    month = calendar.month_name[int(date[2])]
    year = str(date[3])
    if int(day_num) == 1:
        day_num = "1st "
    elif int(day_num) == 2:
        day_num = "2nd "
    elif int(day_num) == 3:
        day_num = "3rd "
    else:
        return str(time + " " + day_str + ", the " + day_num + "th " + month + " " + year)

    return str(time + " " + day_str + ", the " + day_num + month + " " + year)

app = Flask(__name__)

@app.route("/")
def index():
    post = db.get_last_post()
    post[3] = get_date(post[3])
    return render_template("index.html", last_post=post)

@app.route("/edit")
def add():
    table = db.get_all_posts()
    return render_template("edit.html", action="write", table=table)

@app.route("/edit", methods=["POST"])
def edit():
    if request.method == "POST":
        title = request.form["title"]
        under_title = request.form["under_title"]
        author = request.form["author"]
        release = time.strftime("%H:%M/%-d/%m/%Y")  # HH:MM/dd/mm/yyyy format
        content = request.form["content"]
        if db.add_post(title, under_title, author, release, content):
            print("Failed to add post to database!", file=sys.stderr)
            return render_template("add.html", post=1)
        else:  # successfull
            print("Successfully added post to database!", file=sys.stderr)
            return render_template("add.html", post=0)

@app.route("/edit/d")
def d():
    pass

@app.route("/posts")
def posts():
    posts = db.get_all_posts()
    for post in posts:
        post[3] = get_date(post[3])
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
