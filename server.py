from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

attendance = []

# 🧠 SIMPLE STUDENT DATABASE (ID → NAME)
students = {
    "24-13968": "REYES, NICOLE J.",
    "24-13983": "QUIZON, JACOB ALLYSON D.",
    "24-13988": "SALES, HOWARD L.",
    "24-15076": "SIMILLA, TRIXIE NICOLE A."
}

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "SERVER RUNNING"

# ---------------- MARK ATTENDANCE (NO DUPLICATE + NAME SUPPORT) ----------------
@app.route("/mark", methods=["POST"])
def mark():
    data = request.json
    student_id = data["student_id"]

    now = datetime.now()
    date_today = now.strftime("%Y-%m-%d")

    # get student name (fallback if not found)
    student_name = students.get(student_id, "Unknown Student")

    # ❌ prevent duplicate per day
    for record in attendance:
        if record["student_id"] == student_id and record["date"] == date_today:
            return jsonify({"status": "already recorded"})

    # ✅ save attendance
    attendance.append({
        "student_id": student_id,
        "student_name": student_name,
        "date": date_today,
        "time": now.strftime("%H:%M:%S")
    })

    return jsonify({"status": "saved"})

# ---------------- RESET ----------------
@app.route("/reset")
def reset():
    attendance.clear()
    return jsonify({"status": "reset done"})

# ---------------- DATA ----------------
@app.route("/data")
def data():
    return jsonify(attendance)

# ---------------- DASHBOARD ----------------
@app.route("/records")
def records():
    return """
    <html>
    <head>
        <title>QR Attendance System</title>
        <style>
            body {
                font-family: Arial;
                background: #0f172a;
                color: black;
                text-align: center;
            }

            h1 {
                color: #22c55e;
                margin-top: 20px;
            }

            .box {
                width: 85%;
                margin: auto;
                background: white;
                color: black;
                padding: 20px;
                border-radius: 20px;
            }

            table {
                width: 100%;
                border-collapse: collapse;
            }

            th {
                background: #22c55e;
                color: white;
                padding: 10px;
            }

            td {
                padding: 8px;
                border-bottom: 1px solid #ddd;
                text-align: center;
            }

            tr:hover {
                background: #f1f5f9;
            }
        </style>
    </head>
    <body>

        <h1>📷 QR Attendance System</h1>

        <div class="box">
            <table id="table">
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Date</th>
                    <th>Time</th>
                </tr>
            </table>
        </div>

        <script>
            async function loadData() {
                let res = await fetch('/data');
                let data = await res.json();

                let table = document.getElementById("table");

                table.innerHTML = `
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Date</th>
                        <th>Time</th>
                    </tr>
                `;

                data.reverse().forEach(r => {
                    table.innerHTML += `
                        <tr>
                            <td>${r.student_id}</td>
                            <td>${r.student_name}</td>
                            <td>${r.date}</td>
                            <td>${r.time}</td>
                        </tr>
                    `;
                });
            }

            setInterval(loadData, 1000);
            loadData();
        </script>

    </body>
    </html>
    """

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port = int(os.environ.get("PORT", 5000)))
