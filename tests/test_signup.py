from src import app as app_module


def test_signup_success_adds_normalized_email(client):
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "  NewStudent@Mergington.EDU  "},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Signed up newstudent@mergington.edu for Chess Club"
    assert "newstudent@mergington.edu" in app_module.activities["Chess Club"]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post(
        "/activities/Unknown%20Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_409_for_duplicate_signup_case_insensitive(client):
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "MICHAEL@MERGINGTON.EDU"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "MICHAEL@MERGINGTON.EDU is already signed up for Chess Club"


def test_signup_returns_400_when_activity_is_full(client):
    gym_class = app_module.activities["Gym Class"]
    gym_class["max_participants"] = len(gym_class["participants"])

    response = client.post(
        "/activities/Gym%20Class/signup",
        params={"email": "newgymstudent@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Gym Class is full"
