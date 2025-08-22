import React from "react";
import Layout from "../components/Layout";
import { Route, Routes, Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import LandingPage from "./LandingPage"
import ChatsPage from "./ChatsPage";
import PolicyViewPage from "./UsagePolicyPage";

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

					<Route
						path="/policy"
						element= {
							<ProtectedRoute element={<PolicyViewPage />} />
						}
					/>

				</Routes>
			</Layout>
		</>
	);
};

export default Pages;