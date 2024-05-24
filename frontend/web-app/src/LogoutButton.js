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
          auth.logout();
          navigate("/");
        }
      })
      .catch((error) => console.error("Logout failed:", error));
  };

  return <button onClick={handleLogout}>Logout</button>;
}

export default LogoutButton;
