import sqlite3
import sys

db_path = "db/posts.db"

# check if there are any problems with the database
def check():
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("CREATE TABLE if not exists posts \
        (id INTEGER PRIMARY KEY, title TEXT, under_title TEXT, author TEXT, release TEXT, content TEXT)")
        return 0
    except FileNotFoundError as e:
        print(f"Post database not found! \n ERROR:\n{e}",
            file=sys.stderr)
        return 1  # return 1 if sth goes wrong

def add_post(title, under_title, author, release, content):
    if check():
        return 1  # error code 1
    else:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("INSERT INTO posts('title', 'under_title', 'author', 'release', 'content') \
        VALUES(?, ?, ?, ?, ?)", (title, under_title, author, release, content))
        conn.commit()
        conn.close()

def get_last_post():
    if check():
        return 1
    else:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 1")
        post = list(cur.fetchone())
        conn.commit()
        conn.close()
        post.pop(0)  # alternative: del post[0]
        return post

def get_all_posts():
    if check():
        return 1
    else:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM posts ORDER BY id DESC")
        all_posts = cur.fetchall()
        conn.commit()
        cur.close()
        posts = []
        for post in all_posts:
            post = list(post)
            post.pop(0)
            posts.append(post)
        return posts
