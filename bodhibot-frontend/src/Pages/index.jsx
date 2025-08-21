import React from "react";
import LandingPage from "./LandingPage"
import ChatsPage from "./ChatsPage";

function ProtectedRoute({ element }) {
	const { isAuthenticated } = useAuth();
	return isAuthenticated ? element : <Navigate to="/" />;
};

function Pages() {
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
					path="/chats"
					element= {
						<ProtectedRoute element={<ChatsPage />} />
					}
				/>
			</Routes>
		</>
	);
};

export default Pages;