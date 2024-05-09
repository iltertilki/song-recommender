import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "./AuthContext"; // Adjust the import path according to your structure

const Header = () => {
  const auth = useAuth();
  const handleLogout = () => {
    fetch("/logout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    })
      .then(() => {
        auth.logout(); // Update your auth state/context
        // Optionally redirect to home or login page
      })
      .catch((error) => console.error("Logout failed:", error));
  };

  return (
    <header>
      <Link to="/">Home</Link>
      {auth.currentUser && (
        <>
          <Link to="/songs">Songs</Link>
          <button onClick={handleLogout}>Logout</button>
        </>
      )}
      {!auth.currentUser && (
        <>
          <Link to="/login">Login</Link>
          <Link to="/register">Register</Link>
        </>
      )}
    </header>
  );
};

export default Header;
