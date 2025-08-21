import React, { useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const LandingPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();


  useEffect(() => {
    if (isAuthenticated) {
      navigate('/chats');
    }
  }, [isAuthenticated, navigate]);

  return (
    <>
      <div className='min-h-screen flex flex-col'>
        {/* Main Content */}
        <div className="flex-grow">
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
      </div>
    </>
  );
};

export default LandingPage;
