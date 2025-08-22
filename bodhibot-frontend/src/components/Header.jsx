import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import AuthModal from "./AuthModal";
import { useNavigate } from "react-router-dom";
import axiosService from "./axiosInterceptor";

const baseUrl = process.env.REACT_APP_API_BASE_URL;

const Header = () => {
  const { isAuthenticated, logout } = useAuth();
  const [user, setUser] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const getUser = async() => {
      try {
        const response = await axiosService.get(`${baseUrl}auth/me/`);
        if (response?.data) setUser(response.data.data);
        console.log(response.data);
      } catch (err) {
        console.error(`No user found ${err}`);
      }
    }

    getUser();
  }, []);

  return (
    <>
      <nav className="top-navbar flex items-center justify-between p-4 bg-white shadow-md">
        {/* Logo */}
        <div className="app-title text-xl font-semibold flex items-center">
          <img src="BodhibotLogo.png" alt="Logo" className="h-8 mr-2" />
          BodhiBot: Your Educational AI Assistant
        </div>

        {isAuthenticated ? (
          <div className="flex items-center space-x-6">
            {/* Conditional NavLinks */}
            <div className="nav-links flex space-x-4">
              {(user?.is_superuser || user?.is_org_admin) && (
                <button
                  onClick={() => navigate("/policy")}
                  className="nav-link"
                >
                  Policy
                </button>
              )}
              {user?.is_superuser && (
                <button
                  onClick={() => navigate("/logs/view")}
                  className="nav-link"
                >
                  View Logs
                </button>
              )}
              <button
                onClick={() => navigate("/logs/review")}
                className="nav-link"
              >
                Review Logs
              </button>
            </div>

            {/* Dropdown */}
            <div className="relative">
              <button
                onClick={() => setDropdownOpen(!dropdownOpen)}
                className="bg-gray-200 px-3 py-2 rounded hover:bg-gray-300"
              >
                Welcome! {user?.username}
              </button>

              {dropdownOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-white shadow-lg rounded border">
                  <button
                    onClick={() => {
                      setDropdownOpen(false);
                      navigate("/settings");
                    }}
                    className="block w-full text-left px-4 py-2 hover:bg-gray-100"
                  >
                    Settings
                  </button>
                  <button
                    onClick={() => {
                      setDropdownOpen(false);
                      logout();
                    }}
                    className="block w-full text-left px-4 py-2 hover:bg-gray-100"
                  >
                    Logout
                  </button>
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="auth-buttons">
            <button
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
              onClick={() => setShowModal(true)}
            >
              Login / Sign Up
            </button>
          </div>
        )}
      </nav>

      {showModal && <AuthModal onClose={() => setShowModal(false)} />}
    </>
  );

};

export default Header;
