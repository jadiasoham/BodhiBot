import React, { createContext, useState, useEffect, useContext, useCallback } from 'react';
import axios from 'axios'; 
import { jwtDecode } from 'jwt-decode';

const AuthContext = createContext(null);

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;


export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    // Function to set user and token upon successful login
    const setAuthTokens = useCallback((accessToken, refreshToken) => {
        localStorage.setItem("access_token", accessToken);
        localStorage.setItem("refresh_token", refreshToken);
        const decodedUser = accessToken ? jwtDecode(accessToken) : null;
        setUser(decodedUser);
        setIsAuthenticated(!!accessToken);
    }, []);

    // Function to clear user and token upon a logout.
    const logout = useCallback(() => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        setUser(null);
        setIsAuthenticated(false);
    }, []);

    // Function to refresh access token
    const refreshAccessToken = useCallback(async () => {
        const refreshToken = localStorage.getItem("refresh_token");
        if (!refreshToken) {
            logout();
            return null;
        }

        try {
            const response = await axios.post(`${API_BASE_URL}users/token/refresh`, {refresh: refreshToken});
            const newAccessToken = response.data.access;
            localStorage.setItem("access_token", newAccessToken);

            return newAccessToken;
        } catch (error) {
            console.error("Failed to refresh: ", error);
            logout(); // Force a logout since the refresh failed
            return null;
        }
    }, [logout]);

    // Axios interceptor to automatically refresh tokens and store them
    useEffect(() => {
        const requestInterceptor = axios.interceptors.request.use(
            async config => {
                const accessToken = localStorage.getItem("access_token");
                const refreshToken = localStorage.getItem("refresh_token");
                const currentTime = Date.now() / 1000; // In seconds

                if (accessToken && user && user.exp < currentTime) {
                    console.log("Access token expired, attempting to refresh...");
                    const newAccessToken = await refreshAccessToken();

                    if (newAccessToken) {
                        config.headers.Authorization = `Bearer ${newAccessToken}`;

                        const decodedUser = jwtDecode(newAccessToken);
                        setUser(decodedUser);
                    } else {
                        return Promise.reject(new Error("Token refresh failed. User has been logged out."));
                    }
                } else if (accessToken) {
                    config.headers.Authorization = `Bearer ${accessToken}`;
                }
                return config;
            },
            error => {
                return Promise.reject(error);
            }
        );

        const responseInterceptor = axios.interceptors.response.use(
            response => response,
            async error => {
                const originalRequest = error.config;
                if (error.response.status === 401 && originalRequest.url === `${API_BASE_URL}/users/token/refresh/`) {
                    logout();
                    return Promise.reject(error);
                }
                if (error.response.status === 401 && !originalRequest._retry) {
                    originalRequest._retry = true;
                    const newAccessToken = refreshAccessToken();
                    if (newAccessToken) {
                        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
                        return axios(originalRequest);
                    }
                }
                return Promise.reject(error);
            }
        );
        // Clean up the interceptors
        return() => {
            axios.interceptors.request.eject(requestInterceptor);
            axios.interceptors.response.eject(responseInterceptor);
        };
    }, [user, refreshAccessToken, logout]); // Dependencies for useEffect

    //Initial check for tokens on app load:
    useEffect(() => {
        const accessToken = localStorage.getItem("access_token");
        if (accessToken) {
            try {
                const decodedUser = jwtDecode(accessToken);
                const currentTime = Date.now() / 1000;

                if (decodedUser && decodedUser.exp > currentTime) {
                    setUser(decodedUser);
                    setIsAuthenticated(true);
                } else {
                    refreshAccessToken().then(newAccessToken => {
                        if (newAccessToken) {
                            const newDecodedUser = jwtDecode(newAccessToken);
                            setUser(newDecodedUser);
                            setIsAuthenticated(true);
                        } else {
                            logout(); // Force a logout if refresh fails
                        }
                    });
                }
            } catch (error) {
                console.error("Error while decoding the access token or invalid token: ", error);
                logout(); // Current token is malformed. logout.
            }
        }
        setIsLoading(false);
    }, [logout, refreshAccessToken]);

    const contextValue = {
        user,
        isAuthenticated,
        setAuthTokens,
        logout,
        isLoading,
    };

    if (isLoading) {
        return <div>Loading Authentication...</div>;
    }

    return (
        <AuthContext.Provider value= {contextValue}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error("AuthContext must be used within an AuthProvider");
    }
    return context;
};
