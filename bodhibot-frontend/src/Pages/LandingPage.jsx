import React, { useState } from 'react';
import AuthModal from '../components/AuthModal';
import Footer from '../components/Footer';

const LandingPage = () => {
  const [showModal, setShowModal] = useState(false);

  return (
    <>
      {/* NavBar */}
      <nav className="top-navbar flex items-center justify-between p-4 bg-white shadow-md">
        <div className="app-title text-xl font-semibold flex items-center">
          <img
            src="img/CSELogo.png"
            alt="Logo"
            className="h-8 mr-2"
          />
          BodhiBot: Your Educational AI Assistant
        </div>
        <div className="auth-buttons">
          <button
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
            onClick={() => setShowModal(true)}
          >
            Login / Sign Up
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="cover-image-container w-full">
        <img
          src="img/BodhiBotBanner.png"
          alt="Hero"
          className="cover-image w-full h-auto object-cover"
        />
      </div>

      {/* Content Section */}
      <div className="content-container px-6 py-12 text-center bg-gray-50">
        <h2 className="text-3xl md:text-4xl font-bold mb-4">
          BodhiBot: Your 24/7 study buddy, powered by AI.
        </h2>
        <p className="text-lg text-gray-700">
          Ready to solve doubts, explain concepts, and keep you learning anytime, anywhere...
        </p>
      </div>

      {/* Footer */}
      <Footer />

      {/* Auth Modal */}
      {showModal && <AuthModal onClose={() => setShowModal(false)} />}
    </>
  );
};

export default LandingPage;
