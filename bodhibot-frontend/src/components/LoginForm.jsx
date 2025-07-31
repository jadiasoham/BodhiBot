import React, { useState } from "react";
import axios from 'axios';
import { useAuth } from "../context/AuthContext";

const baseUrl = `${process.env.REACT_APP_API_BASE_URL}auth/`;

const LoginForm = ({ onSuccess, onLoginSuccess }) => {
    const [formData, setFormData] = useState({ username: "", password: "" });
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false); // to indicate loading state
    const { setAuthTokens } = useAuth();

    const handleSubmit = async e => {
        e.preventDefault();
        setError(""); // Clear any previous errors
        setLoading(true);

        try {
            const response = await axios.post(`${baseUrl}login/`, formData);
            console.log("Logged in: ", response.data);
            
            // store the tokens returned by Django's TokenObtainPair View:
            const { access, refresh } = response.data;
            console.log(access);
            console.log(refresh);

            setAuthTokens(access, refresh)

            onSuccess();
        } catch (err) {
            console.error("Login error: ", err.response || err);

            if (err.response && err.response.data) {
                // simplejwt returns errors in the `data.details` object
                let data = err.response.data;
                if (data.details) {
                    setError("Error during Login: ", data.details);
                } else if (data.username) {
                    setError("Username: ", data.username[0]);
                } else if (data.password) {
                    setError("Password: ", data.password[0]);
                } else {
                    setError("An unexpected error occurred during login. Please try again.");
                }
            } else {
                setError("Network Error or Server Unreachable");
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            {error && <p className="text-red-500 text-sm">{error}</p>}
            <input
                className="w-full mb-2 px-3 py-2 border rounded"
                placeholder="Username"
                value={formData.username}
                onChange={e => setFormData({...formData, username: e.target.value})}
            />
            <input
                className="w-full mb-4 px-3 py-2 border rounded"
                type="password"
                placeholder="Password"
                value={formData.password}
                onChange={e => setFormData({...formData, password: e.target.value})}
            />
            <button className="login-button w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">{ loading ? "Logging in..." : "Login" }</button>
        </form>
    );
};

export default LoginForm;