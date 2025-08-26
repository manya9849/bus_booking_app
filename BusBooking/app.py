from flask import Flask, request, jsonify
from flask import render_template, redirect, url_for, session
app = Flask(__name__) 
app.secret_key = "secret"

# Dummy users
users = {"admin": "123"}

# Dummy bus data
buses = [
    {"id": 1, "from": "Bengaluru", "to": "Mysuru", "time": "06:30 AM", "price": 280},
    {"id": 2, "from": "Hassan", "to": "Sakleshpur", "time": "08:00 AM", "price": 150},
    {"id": 3, "from": "Bengaluru", "to": "Chennai", "time": "09:15 AM", "price": 700},
    {"id": 4, "from": "Mysuru", "to": "Kodagu", "time": "10:00 AM", "price": 350},
    {"id": 5, "from": "Hassan", "to": "Kodagu", "time": "11:00 AM", "price": 220},
    {"id": 6, "from": "Mangaluru", "to": "Udupi", "time": "11:30 AM", "price": 120},
    {"id": 7, "from": "Hubli", "to": "Belagavi", "time": "01:00 PM", "price": 250},
    {"id": 8, "from": "Bengaluru", "to": "Hyderabad", "time": "02:45 PM", "price": 900},
    {"id": 9, "from": "Chikkamagaluru", "to": "Bengaluru", "time": "04:00 PM", "price": 400},
    {"id": 10, "from": "Mysuru", "to": "Ooty", "time": "05:15 PM", "price": 300},
    {"id": 11, "from": "Bengaluru", "to": "Goa", "time": "07:30 PM", "price": 1500},
    {"id": 12, "from": "Hyderabad", "to": "Vijayawada", "time": "09:00 PM", "price": 650},
    {"id": 13, "from": "Bengaluru", "to": "Pune", "time": "10:30 PM", "price": 1200},
    {"id": 14, "from": "Bengaluru", "to": "Delhi", "time": "11:45 PM", "price": 2500},
    {"id": 15, "from": "Kodagu", "to": "Mysuru", "time": "06:00 AM", "price": 320},
    {"id": 16, "from": "Kodagu", "to": "Hassan", "time": "07:30 AM", "price": 220},
    {"id": 17, "from": "Hassan", "to": "Bengaluru", "time": "05:45 PM", "price": 300},
    {"id": 18, "from": "Bengaluru", "to": "Hassan", "time": "06:15 PM", "price": 320},

]

# Store bookings
bookings = []

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["username"]
        pwd = request.form["password"]
        if uname in users and users[uname] == pwd:
            session["user"] = uname
            return redirect(url_for("home"))
        else:
            return "Invalid login"
    return render_template("login.html")

@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("home.html", buses=buses)

@app.route("/select/<int:bus_id>")
def select(bus_id):
    if "user" not in session:
        return redirect(url_for("login"))
    bus = next((b for b in buses if b["id"] == bus_id), None)
    return render_template("select.html", bus=bus)

@app.route("/book/<int:bus_id>", methods=["GET", "POST"])
def book(bus_id, age=None):
    if "user" not in session:
        return redirect(url_for("login"))
    bus = next((b for b in buses if b["id"] == bus_id), None)
    if request.method == "POST":
        booking = {
            "bus": bus,
            "name": request.form["name"],
            "age": request.form["age"],
            "seat": request.form["seat"],
        }
        bookings.append(booking)
        return redirect(url_for("confirm", index=len(bookings) - 1))
    return render_template("booking.html", bus=bus)

@app.route("/confirm/<int:index>")
def confirm(index):
    if "user" not in session:
        return redirect(url_for("login"))
    booking = bookings[index]
    return render_template("confirm.html", booking=booking)

if __name__ == "__main__":  # Fixed __name__ check
    app.run(debug=True)
 