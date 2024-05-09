import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

function LogoutButton() {
  const navigate = useNavigate();
  const auth = useAuth();

  const handleLogout = () => {
    fetch("/logout", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (response.ok) {
          auth.logout(); // Update auth state to reflect logout
          navigate("/"); // Redirect to the homepage or login page
        }
      })
      .catch((error) => console.error("Logout failed:", error));
  };

  return <button onClick={handleLogout}>Logout</button>;
}

export default LogoutButton;
