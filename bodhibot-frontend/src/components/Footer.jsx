import React from 'react';

const Footer = () => {
  return (
    <footer className="w-full bg-gray-800 app-footer text-white text-center py-4 mt-10">
      <p className="text-sm">
        &copy; {new Date().getFullYear()} BodhiBot, Dept. of CSE, IIT Bombay | All rights reserved.
      </p>
    </footer>
  );
};

export default Footer;
