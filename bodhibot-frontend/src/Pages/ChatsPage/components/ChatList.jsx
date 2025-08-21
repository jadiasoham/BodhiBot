import React, { useState, useEffect } from "react";
import axiosService from "../../../components/axiosInterceptor";
import { FaPlusCircle } from "react-icons/fa"

const baseUrl = process.env.REACT_APP_API_BASE_URL;

const ChatList = ({ onChatSelect, onChatAdd }) => {
  const [chats, setChats] = useState([]);
  const [selectedChat, setSelectedChat] = useState(null);

  const getChats = async() => {
    try {
      const response = await axiosService.get(`${baseUrl}chats/my-chats/`);
      if (response?.data) setChats(response.data.data);
    } catch (err) {
      console.error(`Unable to retrieve chats: ${err}`);
    }
  }

  useEffect(() => {
    getChats();
  }, [])

  const handleChatSelect = (chat) => {
    if (onChatSelect) onChatSelect(chat);
    setSelectedChat(chat.id)
  }  

  return (
    <div className="w-full p-4 border-r">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">Your Chats</h2>
        <button className='btn btn-primary' onClick={onChatAdd}>
          <FaPlusCircle size={32} />
        </button>
      </div>

      {Array.isArray(chats) && chats.length > 0 ? (
        <ul>
          {chats.map(chat => (
            <li
              key={chat.id}
              className={`cursor-pointer p-2 hover:bg-gray-100 rounded ${selectedChat === chat.id ? "bg-blue-100" : ""}`}
              onClick={() => handleChatSelect(chat)}
            >
              <div className="font-semibold">{chat.name}</div>
              <div className="text-xs text-gray-500">
                Last updated: {new Date(chat.last_message).toLocaleString()}
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <h3>Start a new Chat</h3>
      )}
    </div>
  );
};

export default ChatList;