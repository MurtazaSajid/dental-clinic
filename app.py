import os, time
from flask import Flask, request, redirect, render_template, flash, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

SERVICES = [
    ("General Checkup", "Full exam, X-rays and professional cleaning.", "🦷"),
    ("Teeth Whitening", "Safe in-clinic whitening for a brighter smile.", "✨"),
    ("Braces & Aligners", "Modern orthodontics for teens and adults.", "😁"),
    ("Root Canal", "Pain-free treatment to save your natural tooth.", "🩺"),
    ("Dental Implants", "Permanent, natural-looking tooth replacement.", "🔩"),
    ("Kids Dentistry", "Gentle, friendly care for little smiles.", "🧸"),
]

def get_conn():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "rootpass"),
        database=os.getenv("DB_NAME", "dentaldb"),
    )

def init_db():
    for _ in range(40):  # wait for MySQL to be ready
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS appointments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                patient_name VARCHAR(100) NOT NULL,
                phone VARCHAR(30) NOT NULL,
                email VARCHAR(120),
                service VARCHAR(80) NOT NULL,
                appt_date DATE NOT NULL,
                appt_time VARCHAR(10) NOT NULL,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
            conn.commit(); conn.close()
            return
        except Exception:
            time.sleep(2)

@app.route("/")
def index():
    return render_template("index.html", services=SERVICES)

@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "POST":
        f = request.form
        conn = get_conn(); cur = conn.cursor()
        cur.execute(
            "INSERT INTO appointments (patient_name, phone, email, service, appt_date, appt_time, message) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (f["name"], f["phone"], f.get("email"), f["service"], f["date"], f["time"], f.get("message")))
        conn.commit(); conn.close()
        flash("Appointment booked! We will contact you shortly to confirm.")
        return redirect(url_for("book"))
    return render_template("book.html", services=SERVICES)

@app.route("/appointments")
def appointments():
    conn = get_conn(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM appointments ORDER BY appt_date, appt_time")
    rows = cur.fetchall(); conn.close()
    return render_template("appointments.html", rows=rows)

@app.route("/appointments/<int:appt_id>/delete", methods=["POST"])
def delete(appt_id):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("DELETE FROM appointments WHERE id=%s", (appt_id,))
    conn.commit(); conn.close()
    return redirect(url_for("appointments"))

@app.route("/health")
def health():
    return "ok"

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
