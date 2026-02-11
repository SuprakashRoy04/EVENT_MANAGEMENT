from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "secretkey"

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS membership(
        membership_no INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        start_date TEXT,
        duration TEXT,
        expiry_date TEXT,
        status TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        membership_no INTEGER,
        event_name TEXT,
        amount INTEGER,
        date TEXT
    )
    """)

    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username,password,role) VALUES ('admin','admin123','admin')")
        cursor.execute("INSERT INTO users (username,password,role) VALUES ('user','user123','user')")

    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["username"] = user[1]
            session["role"] = user[3]
            return redirect("/dashboard")
        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")
    return render_template("dashboard.html", role=session["role"])



@app.route("/add_membership", methods=["GET", "POST"])
def add_membership():

    if "username" not in session:
        return redirect("/")

    if session["role"] != "admin":
        return redirect("/dashboard")

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        duration = request.form["duration"]

        start_date = datetime.today()

        if duration == "6":
            expiry_date = start_date + timedelta(days=180)
        elif duration == "12":
            expiry_date = start_date + timedelta(days=365)
        else:
            expiry_date = start_date + timedelta(days=730)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO membership (name, phone, start_date, duration, expiry_date, status)
        VALUES (?,?,?,?,?,?)
        """, (
            name,
            phone,
            start_date.strftime("%Y-%m-%d"),
            duration,
            expiry_date.strftime("%Y-%m-%d"),
            "active"
        ))

        conn.commit()
        conn.close()

        # Return fresh page with message and CLEAR form
        return render_template("add_membership.html", success=True)

    return render_template("add_membership.html")





@app.route("/report")
def report():
    if "username" not in session:
        return redirect("/")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM membership")
    data = cursor.fetchall()
    conn.close()

    return render_template("report.html", data=data)

@app.route("/transaction_report")
def transaction_report():
    if "username" not in session:
        return redirect("/")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    data = cursor.fetchall()
    conn.close()

    return render_template("transaction_report.html", data=data)


@app.route("/transactions", methods=["GET", "POST"])
def transactions():

    if "username" not in session:
        return redirect("/")

    if request.method == "POST":
        membership_no = request.form["membership_no"]
        event_name = request.form["event_name"]
        amount = request.form["amount"]
        date = datetime.today().strftime("%Y-%m-%d")

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO transactions (membership_no, event_name, amount, date)
        VALUES (?,?,?,?)
        """, (membership_no, event_name, amount, date))

        conn.commit()
        conn.close()

        return redirect("/transaction_report")

    return render_template("transactions.html")


@app.route("/update_membership", methods=["GET", "POST"])
def update_membership():

    if "username" not in session:
        return redirect("/")

    if session["role"] != "admin":
        return redirect("/dashboard")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        membership_no = request.form["membership_no"]

        cursor.execute("SELECT * FROM membership WHERE membership_no=?", (membership_no,))
        member = cursor.fetchone()

        if not member:
            conn.close()
            return "Membership Not Found"

        action = request.form.get("action")

        if action == "extend":
            old_expiry = datetime.strptime(member[5], "%Y-%m-%d")
            new_expiry = old_expiry + timedelta(days=180)

            cursor.execute("""
            UPDATE membership
            SET expiry_date=?
            WHERE membership_no=?
            """, (new_expiry.strftime("%Y-%m-%d"), membership_no))

        elif action == "cancel":
            cursor.execute("""
            UPDATE membership
            SET status='cancelled'
            WHERE membership_no=?
            """, (membership_no,))

        conn.commit()
        conn.close()

        return render_template("update_membership.html", success="Membership Updated Successfully")

    conn.close()
    return render_template("update_membership.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
