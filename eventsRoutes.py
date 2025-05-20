@events_bp.route("/createevent", methods=["GET", "POST"])
def create_event():
    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        date = request.form["date"]
        time = request.form["time"]
        type_ = request.form["type"]
        price = request.form["price"]

        with sqlite3.connect("events.db") as conn:
            conn.execute("""
                INSERT INTO events (name, location, date, time, type, price)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, location, date, time, type_, price))
            conn.commit()

        return redirect("/events")

    return render_template("createevent.html")