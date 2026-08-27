import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { createUser } from "../services/userService";
import "./Signup.css";

function Signup() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    birthday: "",
    phone_number: "",
    is_admin: false,
  });

  const [errors, setErrors] = useState({});
  const [apiError, setApiError] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(event) {
    const { name, value, type, checked } = event.target;

    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  }

  function validateForm() {
    const newErrors = {};

    if (!formData.first_name.trim()) {
      newErrors.first_name = "First name is required";
    }

    if (!formData.last_name.trim()) {
      newErrors.last_name = "Last name is required";
    }

    if (!formData.email.trim()) {
      newErrors.email = "Email is required";
    } else if (
      !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)
    ) {
      newErrors.email = "Enter a valid email";
    }

    if (!formData.password) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 8) {
      newErrors.password =
        "Password must be at least 8 characters";
    }

    if (!formData.birthday) {
      newErrors.birthday = "Birthday is required";
    } else {
      const birthday = new Date(formData.birthday);
      const today = new Date();

      if (birthday > today) {
        newErrors.birthday =
          "Birthday cannot be in the future";
      }
    }

    if (!formData.phone_number.trim()) {
      newErrors.phone_number =
        "Phone number is required";
    } else if (
      !/^\d{10}$/.test(formData.phone_number)
    ) {
      newErrors.phone_number =
        "Phone number must contain 10 digits";
    }

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setApiError("");

    if (!validateForm()) {
      return;
    }

    try {
      setLoading(true);

      await createUser(formData);

      navigate("/login");
    } catch (error) {
      setApiError(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="signup-page">
      <div className="signup-card">
        <h1>Create Account</h1>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>First Name</label>

            <input
              type="text"
              name="first_name"
              value={formData.first_name}
              onChange={handleChange}
            />

            {errors.first_name && (
              <p className="error">
                {errors.first_name}
              </p>
            )}
          </div>

          <div className="form-group">
            <label>Last Name</label>

            <input
              type="text"
              name="last_name"
              value={formData.last_name}
              onChange={handleChange}
            />

            {errors.last_name && (
              <p className="error">
                {errors.last_name}
              </p>
            )}
          </div>

          <div className="form-group">
            <label>Email</label>

            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
            />

            {errors.email && (
              <p className="error">
                {errors.email}
              </p>
            )}
          </div>

          <div className="form-group">
            <label>Password</label>

            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
            />

            {errors.password && (
              <p className="error">
                {errors.password}
              </p>
            )}
          </div>

          <div className="form-group">
            <label>Birthday</label>

            <input
              type="date"
              name="birthday"
              value={formData.birthday}
              onChange={handleChange}
            />

            {errors.birthday && (
              <p className="error">
                {errors.birthday}
              </p>
            )}
          </div>

          <div className="form-group">
            <label>Phone Number</label>

            <input
              type="tel"
              name="phone_number"
              value={formData.phone_number}
              onChange={handleChange}
              placeholder="9545551234"
            />

            {errors.phone_number && (
              <p className="error">
                {errors.phone_number}
              </p>
            )}
          </div>

          <label className="admin-toggle">
            <input
              type="checkbox"
              name="is_admin"
              checked={formData.is_admin}
              onChange={handleChange}
            />

            Create as Admin
          </label>

          {apiError && (
            <p className="error api-error">
              {apiError}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
          >
            {loading ? "Creating Account..." : "Sign Up"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Signup;