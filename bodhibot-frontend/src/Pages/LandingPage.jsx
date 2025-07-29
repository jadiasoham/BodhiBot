import React, { useState } from 'react';
import AuthModal from '../components/AuthModal';
import Footer from '../components/Footer';
import { useNavigate } from 'react-router-dom';

const LandingPage = () => {
  const [showModal, setShowModal] = useState(false);
  const navigate = useNavigate();

  const onLogin = () => {
    setShowModal(false);
    navigate('/main');
  };

  return (
    <>
      <div className='min-h-screen flex flex-col'>
        {/* NavBar */}
        <nav className="top-navbar flex items-center justify-between p-4 bg-white shadow-md">
          <div className="app-title text-xl font-semibold flex items-center">
            <img
              src="BodhibotLogo.png"
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
        {/* Main Content */}
        <div className="flex-grow">
          {/* Hero Section */}
          {/* <div className="cover-image-container w-full">
            <img
              src="BodhibotBanner.png"
              alt="Hero"
              className="cover-image w-full h-auto object-cover"
            />
          </div> */}

          {/* Content Section */}
          <div className="flex flex-col md:flex-row items-center bg-gray-50 px-6 py-12">
            {/* Left Column: Image */}
            <div className="w-full md:w-1/2 flex justify-center mb-6 md:mb-0">
              <img
                src="BodhibotLogo.png"
                alt="BodhiBot Illustration"
                className="w-[500px] h-[500px] object-contain"
              />
            </div>

            {/* Right Column: Text */}
            <div className="w-full md:w-1/2 text-center md:text-left">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                BodhiBot: Your 24/7 study buddy, powered by AI.
              </h2>
              <p className="text-lg text-gray-700">
                Ready to solve doubts, explain concepts, and keep you learning anytime, anywhere...
              </p>
            </div>
          </div>
        </div>


        {/* Footer */}
        <Footer />

        {/* Auth Modal */}
        {showModal && <AuthModal onLoginSuccess={onLogin} onClose={() => setShowModal(false)} />}
      </div>
    </>
  );
};

export default LandingPage;
