import React, { useState } from "react";
import { AuthProvider, useAuth } from "./context/AuthContext";
import AuthModal from './components/AuthModal';
import LandingPage from './Pages/LandingPage';
import MainPage from './Pages/MainPage';
import './App.css';

function AppContent() {
  const { isAuthenticated, logout } = useAuth();
  const [showAuthModal, setShowAuthModal] = useState(false);

  return (
    <div className="app-container">
      {isAuthenticated ? (
        <MainPage logout={logout} />
      ) : (
        <>
          <LandingPage setShowModal={setShowAuthModal} />
          {showAuthModal && <AuthModal onClose={() => setShowAuthModal(false)} />}
        </>
      )}
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
