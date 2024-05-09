import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const auth = useAuth();
  const navigate = useNavigate();

  const handleLogin = (event) => {
    event.preventDefault();
    fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.authenticated) {
          auth.login(data.user);
          navigate("/songs");
        } else {
          alert("Login failed");
        }
      })
      .catch((error) => {
        console.error("Login error:", error);
      });
  };

  return (
    <div>
      <form onSubmit={handleLogin}>
        <label>
          Username:
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </label>
        <label>
          Password:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default LoginPage;
