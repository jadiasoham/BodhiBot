import React from "react";
import LandingPage from "./LandingPage"
import ChatsPage from "./ChatsPage";
import Layout from "../components/Layout";

function ProtectedRoute({ element }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? element : <Navigate to="/" />;
};

function Pages() {
  const [showAuthModal, setShowAuthModal] = useState(false);  
  
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