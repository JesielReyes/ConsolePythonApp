import uuid

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def _create_user(is_admin=False):
	email = f"{uuid.uuid4()}@example.com"
	password = "test-password123"
	first_name = "Test Admin" if is_admin else "Test Customer"

	response = client.post(
		"/users",
		json={
			"email": email,
			"password": password,
			"is_admin": is_admin,
			"birthday": "1990-01-01",
			"phone_number": "555-0100",
			"first_name": first_name,
			"last_name": "User",
		},
	)
	assert response.status_code == 201

	return email, password, response.json()["id"], first_name


def test_login_returns_customer_details_for_valid_credentials():
	email, password, user_id, first_name = _create_user(is_admin=False)

	response = client.post(
		"/login",
		json={
			"email": email,
			"password": password,
		},
	)

	assert response.status_code == 200
	assert response.json() == {
		"user_id": user_id,
		"first_name": first_name,
		"is_admin": False,
		"message": "Login successful",
		"redirect_to": "/user-dashboard",
	}


def test_login_rejects_invalid_credentials():
	email, _password, _user_id, _first_name = _create_user(is_admin=False)

	response = client.post(
		"/login",
		json={
			"email": email,
			"password": "wrong-password",
		},
	)

	assert response.status_code == 401
	assert response.json() == {"detail": "Invalid email or password"}


def test_login_redirects_admin_to_admin_dashboard():
	email, password, _user_id, _first_name = _create_user(is_admin=True)

	response = client.post(
		"/login",
		json={"email": email, "password": password},
	)

	assert response.status_code == 200
	assert response.json()["is_admin"] is True
	assert response.json()["redirect_to"] == "/admin-dashboard"
