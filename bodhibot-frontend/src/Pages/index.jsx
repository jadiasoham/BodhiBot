import React from "react";
import LandingPage from "./LandingPage"
import ChatsPage from "./ChatsPage";
import Layout from "../components/Layout";
import { Route, Routes, Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function ProtectedRoute({ element }) {
	const { isAuthenticated } = useAuth();
	return isAuthenticated ? element : <Navigate to="/" />;
};

function Pages() {  
	return (
		<>
			<Layout>
				<Routes>
					<Route
						path= "/"
						element = {
							<LandingPage /> 
						}
					/>
					
					<Route
						path="/chats"
						element= {
							<ProtectedRoute element={<ChatsPage />} />
						}
					/>
				</Routes>
			</Layout>
		</>
	);
};

export default Pages;