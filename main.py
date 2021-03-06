import os
import base64
import sqlite3

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()

    if request.method == 'POST':
        # A message'), ('256.256.256.256', 'You have been hacked!)
        # "INSERT INTO messages VALUES ('127.0.0.1', 'A message'), ('256.256.256.256', 'You have been hacked!))"
        # above results in two SQL row inserts
        transaction = "INSERT INTO messages VALUES ('{}', '{}')".format(
            request.remote_addr,
            request.form['content'],
        ).strip("'")#strips single quotes from input to avoid breaking out of SQL syntax
        c.execute(transaction)
        conn.commit()


    body = """
<html>
<body>
<h1>Messages</h1>
<h2>Enter a Message</h2>
<form method="POST">
    <label for="content">Message</label>
    <input type="text" name="content"><br>

    <input type="submit" value="Submit">
</form>

<h2>Messages</h2>
"""
    
    for m in c.execute("SELECT * FROM messages"):
        body += """
<div class="message">
{}: {}
</div>
""".format(m[0], m[1])

    c.close()

    return body 


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6779))
    app.run(host='0.0.0.0', port=port)

