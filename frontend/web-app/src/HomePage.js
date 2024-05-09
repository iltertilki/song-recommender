// HomePage.js

import React from "react";
import { Link } from "react-router-dom";
import LoginPage from "./LoginPage";

function HomePage() {
  return (
    <div>
      <h1>Welcome to Song Recommender</h1>
      <LoginPage />
      <p>
        Don't have an account? <Link to="/register">Sign up here</Link>
      </p>
    </div>
  );
}

export default HomePage;
