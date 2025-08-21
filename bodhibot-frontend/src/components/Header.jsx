import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import AuthModal from "./AuthModal";

const Header = () => {
	const { isAuthenticated, logout } = useAuth();
	const [showModal, setShowModal] = useState(false);

	return (
		<>
			<nav className="top-navbar flex items-center justify-between p-4 bg-white shadow-md">
				<div className="app-title text-xl font-semibold flex items-center">
					<img
						src="BodhibotLogo.png"
						alt="Logo"
						className="h-8 mr-2"
					/>
					BodhiBot: Your Educational AI Assistant
				</div>
				{
					isAuthenticated ?
					(
						<div className="auth-buttons">
							<button
								className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
								onClick={logout}
							>
								Logout
							</button>
						</div>
					) : (
						<div className="auth-buttons">
							<button
								className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
								onClick={() => setShowModal(true)}
							>
								Login / Sign Up
							</button>
						</div>
					)
				}
			</nav>
			{showModal && <AuthModal onClose={() => setShowModal(false)} />}
		</>
	);

};

export default Header;
