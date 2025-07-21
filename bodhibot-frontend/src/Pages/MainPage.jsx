import React, { useState } from 'react';
import ChatList from '../components/ChatList';
import axios from 'axios';

const baseUrl = process.env.REACT_APP_API_BASE_URL;

const MainPage = () => {
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
      setSelectedChat(newChat);
    } catch (err) {
      console.error("Error creating new chat: ", err);
      alert("Failed to create new chat. Please try again.");
    }
  };

  return (
    <div className="flex h-screen">
      <ChatList onChatSelect={setSelectedChat} onChatAdd={addNewChat} />
      <div className="flex-1 p-4">
        {selectedChat ? (
          <div>
            {/* <ChatScreen chat={selectedChat} /> */}
            <p className="text-lg font-medium">Chat messages for: {selectedChat.name} will appear here once ready!</p>
            {/* This is a temporary placeholder, and will be replaced with the actual chat screen once ready. */}
          </div>
        ) : (
          <p className="text-gray-500">Select a chat to begin</p>
        )}
      </div>
    </div>
  );
};

export default MainPage;
