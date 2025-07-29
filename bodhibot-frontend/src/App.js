import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from './context/AuthContext';
import AuthModal from './components/AuthModal';
import LandingPage from "./Pages/LandingPage";
import MainPage from './Pages/MainPage';
import './App.css';


function ProtectedRoute({ element }) {
	const { isAuthenticated } = useAuth();
	return isAuthenticated ? element : <Navigate to="/" />;
};

function AppRoutes() {
	const [showAuthModal, setShowAuthModal] = useState(false);

	return (
		<>
			<Routes>
				<Route
					path= "/"
					element = {
						<>
							<LandingPage setShowAuthModal={ setShowAuthModal } />
							{ showAuthModal && <AuthModal onClose={() => setShowAuthModal(false)} />} 
						</>
					}
				/>
				
				<Route
					path="/main"
					element= {
						<ProtectedRoute element={<MainPage />} />
					}
				/>
			</Routes>
		</>
	);
};

function App() {
	return (
		<AuthProvider>
			<Router>
				<AppRoutes />
			</Router>
		</AuthProvider>
	);
};

export default App;