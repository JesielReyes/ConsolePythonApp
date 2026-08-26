import { useState } from "react";
import { createUser } from "../services/userService";

function Signup() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    first_name: "",
    last_name: "",
    birthday: "",
    phone_number: "",
    is_admin: false,
  });

  const [message, setMessage] = useState("");

  function handleChange(event) {
    const { name, value, type, checked } = event.target;

    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  }

  async function handleSubmit(event) {
    event.preventDefault();

    try {
      const user = await createUser(formData);

      setMessage(`User created successfully. ID: ${user.id}`);
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <div>
      <h1>Create Account</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="first_name"
          placeholder="First name"
          value={formData.first_name}
          onChange={handleChange}
        />

        <input
          type="text"
          name="last_name"
          placeholder="Last name"
          value={formData.last_name}
          onChange={handleChange}
        />

        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
        />

        <input
          type="date"
          name="birthday"
          value={formData.birthday}
          onChange={handleChange}
        />

        <input
          type="tel"
          name="phone_number"
          placeholder="Phone number"
          value={formData.phone_number}
          onChange={handleChange}
        />

        <label>
          <input
            type="checkbox"
            name="is_admin"
            checked={formData.is_admin}
            onChange={handleChange}
          />

          Create as Admin
        </label>

        <button type="submit">
          Sign Up
        </button>
      </form>

      {message && <p>{message}</p>}
    </div>
  );
}

export default Signup;