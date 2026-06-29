from src import app as app_module


def test_unregister_success_removes_participant(client):
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Unregistered michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown%20Club/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_when_email_not_signed_up(client):
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "notregistered@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "notregistered@mergington.edu is not signed up for Chess Club"


def test_unregister_is_case_insensitive_for_email_match(client):
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "MICHAEL@MERGINGTON.EDU"},
    )

    assert response.status_code == 200
    participants_lower = [
        participant.lower()
        for participant in app_module.activities["Chess Club"]["participants"]
    ]
    assert "michael@mergington.edu" not in participants_lower
