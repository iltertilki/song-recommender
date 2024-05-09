import React, { useRef } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import RegisterForm from "./RegisterForm";
import SongList from "./SongList";
import { AuthProvider, useAuth } from "./AuthContext";
import HomePage from "./HomePage";

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/register" element={<RegisterForm />} />
            <Route
              path="/songs"
              element={
                <ProtectedRoute>
                  <SongList />
                </ProtectedRoute>
              }
            />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

function ProtectedRoute({ children }) {
  const auth = useAuth();
  return auth.currentUser ? children : <Navigate to="/" />;
}

export default App;
