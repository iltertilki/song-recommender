import React from "react";
import { Link } from "react-router-dom";
import LoginPage from "./LoginPage";
import "./HomePage.css"; // Assuming your CSS file is named HomePage.css

function HomePage() {
  return (
    <div className="home-container">
      <h1 className="home-title">Welcome to Song Recommender</h1>
      <div className="login-container">
        <LoginPage />
      </div>
      <p className="signup-link">
        Don't have an account?{" "}
        <Link to="/register" className="register-link">
          Sign up here
        </Link>
      </p>
    </div>
  );
}

export default HomePage;
