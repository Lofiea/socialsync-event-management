def test_signup_login_profile_flow(client):
    # Sign up
    r = client.post("/signup", data={
        "name": "alice",
        "email": "alice@example.com",
        "password": "StrongP@ss1",
        "confirm-password": "StrongP@ss1"
    }, follow_redirects=True)
    assert r.status_code in (200, 302)

    r = client.post("/login", data={
        "email": "alice@example.com",
        "password": "StrongP@ss1"
    }, follow_redirects=True)
    assert r.status_code in (200, 302)

    r = client.get("/profile", follow_redirects=True)
    assert r.status_code == 200

    r = client.get("/create-event", follow_redirects=True)
    assert r.status_code == 200