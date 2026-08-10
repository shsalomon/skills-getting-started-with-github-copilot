from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    activities[activity_name]["participants"].append(email)

    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"


def test_signup_then_unregister_round_trip():
    activity_name = "Programming Class"
    email = "roundtrip@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )

    assert unregister_response.status_code == 200
    assert email not in activities[activity_name]["participants"]
