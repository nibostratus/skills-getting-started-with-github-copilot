def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities


def test_get_activities_includes_required_activity_fields(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    chess_club = activities["Chess Club"]

    assert set(chess_club.keys()) == {
        "description",
        "schedule",
        "max_participants",
        "participants",
    }
    assert isinstance(chess_club["participants"], list)
