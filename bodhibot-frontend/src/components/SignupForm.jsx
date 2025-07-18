import React, { useState } from "react";
import axios from "axios";

const baseUrl = `${process.env.REACT_APP_API_BASE_URL}/users`;

const SignupForm = ({onSuccess}) => {
    const [formData, setFormData] = useState({username: "", email: "", password: ""});
    const [error, setError] = useState("");

    const handleSubmit = async e => {
        e.preventDefault();
        try {
            const response = await axios.post(`${baseUrl}/signup/`, formData);
            console.log(response.data);

            onSuccess();
        } catch (err) {
            setError("Signup Failed: " + (err.response?.data?.detail || "Unknown error"));
        }
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            {error && <p className="text-red-500 text-sm">{error}</p>}
            <input
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
                placeholder="Username"
                value={formData.username}
                onChange={e => setFormData({...formData, username: e.target.value})}
            />
            <input
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
                placeholder="Email"
                type="email"
                value={formData.email}
                onChange={e => setFormData({...formData, email: e.target.value})}
            />
            <input
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
                type="password"
                placeholder="Password"
                value={formData.password}
                onChange={e => setFormData({...formData, password: e.target.value})}
            />
            <input
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
                type="password"
                placeholder="Confirm Password"
                value={formData.confirmPassword}
                onChange={e => setFormData({...formData, confirmPassword: e.target.value})}
            />
            <button className="w-full signup-button bg-green-600 text-white py-2 rounded hover: bg-green-700">Sign Up</button>
        </form>
    );
};

export default SignupForm;