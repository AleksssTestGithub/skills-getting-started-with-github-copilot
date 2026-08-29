from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)

#A comment
def test_unregister_participant_removes_email_and_keeps_activity_list_consistent():
    # start with a known participant list
    response = client.get("/activities")
    assert response.status_code == 200

    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    before = response.json()[activity_name]
    assert email in before["participants"]

    delete_response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Unregistered {email} from {activity_name}"

    after = client.get("/activities").json()[activity_name]
    assert email not in after["participants"]
    assert len(after["participants"]) == len(before["participants"]) - 1


def test_unregister_nonexistent_participant_returns_404():
    response = client.delete("/activities/Chess Club/participants/ghost@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
