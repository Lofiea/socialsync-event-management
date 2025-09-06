import sqlite3
import importlib

def test_events_pagination(client):
    app_module = importlib.import_module("app")

    con = sqlite3.connect(app_module.DB_PATH)
    cur = con.cursor()
    for i in range(15):
        cur.execute(
            "INSERT INTO events (title, description, start_date, start_time) VALUES (?,?,?,?)",
            (f"TestEvent{i}", "desc", "2025-01-01", "09:00")
        )
    con.commit(); con.close()

    #page 1
    r1 = client.get("/events?page=1&sort=id")
    assert b"TestEvent0" in r1.data and b"TestEvent9" in r1.data
    assert b"TestEvent10" not in r1.data and b"TestEvent14" not in r1.data

    r2 = client.get("/events?page=2&sort=id")
    assert b"TestEvent10" in r2.data or b"TestEvent14" in r2.data