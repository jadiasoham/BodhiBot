import React, { useState } from 'react';
import ChatList from '../components/ChatList';
import ChatView from '../components/ChatView';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

const baseUrl = process.env.REACT_APP_API_BASE_URL;

const MainPage = () => {
  const { logout } = useAuth();
  const [chatList, setChatList] = useState([]);
  const [selectedChat, setSelectedChat] = useState(null);

  const addNewChat = async (chatName) => {
    try {
      const response = await axios.post(`${baseUrl}chats/my-chats/`, {
        name: chatName
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });

      const newChat = response.data;
      setChatList((prev) => [...prev, newChat]);
      setSelectedChat(newChat);
    } catch (err) {
      console.error("Error creating new chat: ", err);
      alert("Failed to create new chat. Please try again.");
    }
  };

  return (
    <>
    {/* NavBar */}
      <nav className="top-navbar flex items-center justify-between p-4 bg-white shadow-md">
        <div className="app-title text-xl font-semibold flex items-center">
          <img
            src="BodhibotLogo.png"
            alt="Logo"
            className="h-8 mr-2"
          />
          BodhiBot: Your Educational AI Assistant
        </div>
        <div className="auth-buttons">
          <button
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
            onClick={logout}
          >
            Logout
          </button>
        </div>
      </nav>

    <div className="flex h-screen">
      <ChatList onChatSelect={setSelectedChat} onChatAdd={addNewChat} />
      <div className="flex-1 p-4">
        {selectedChat ? (
          <div>
            <ChatView chatName={selectedChat.name} />
          </div>
        ) : (
          <p className="text-gray-500">Select a chat to begin</p>
        )}
      </div>
    </div>
    </>
  );
};

export default MainPage;
