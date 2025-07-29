import React, { useState } from "react";
import LoginForm from "./LoginForm";
import SignupForm from "./SignupForm";

const AuthModal = ({ onLoginSuccess, onClose }) => {
    const [activeTab, setActiveTab] = useState("login");

    return (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
            <div className="bg-white p-6 rounded-lg w-96 shadow-lg relative">
                <button className="absolute top-2 right-3 text-xl text-gray-500" onClick={onClose}>
                    &times;
                </button>
                <div className="flex mb-4 border-b">
                    <button
                        className={`flex-1 py-2 ${activeTab === "login" ? "border-b-2 border-blue-500 font-semibold" : ""}`}
                        onClick={() => setActiveTab("login")}
                    >
                        Login
                    </button>
                    <button
                        className={`flex-1 py-2 ${activeTab === 'signup' ? 'border-b-2 border-blue-500 font-semibold' : ''}`}
                        onClick={() => setActiveTab('signup')}
                    >
                        Sign Up
                    </button>
                </div>
                {activeTab === 'login' ? <LoginForm onSuccess={ onLoginSuccess } /> : <SignupForm onSuccess={ onClose } />}
            </div>
        </div>
    );
};

export default AuthModal;