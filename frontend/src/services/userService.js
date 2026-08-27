const API_URL = "http://127.0.0.1:8000";

export async function createUser(userData) {
  const response = await fetch(`${API_URL}/users`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });

  const data = await response.json();

  if (!response.ok) {
    if (
      response.status === 409 ||
      String(data.detail || data.message)
        .toLowerCase()
        .includes("email")
    ) {
      throw new Error(
        "An account with that email already exists"
      );
    }

    throw new Error(
      data.detail ||
        data.message ||
        "Failed to create account"
    );
  }

  return data;
}