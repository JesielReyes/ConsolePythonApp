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
    throw new Error(
      data.detail || "Unable to create user"
    );
  }

  return data;
}