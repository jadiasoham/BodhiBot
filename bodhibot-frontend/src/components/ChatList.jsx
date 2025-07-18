import React, { useEffect, useState } from 'react';
import axios from '../utils/axios';

const ChatList = ({ onChatSelect }) => {
  const [chats, setChats] = useState([]);

  useEffect(() => {
    axios.get('/api/chats/')
      .then(res => setChats(res.data))
      .catch(err => console.error("Failed to load chats", err));
  }, []);

  return (
    <div className="w-full sm:w-1/3 p-4 border-r">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">Your Chats</h2>
        {/* You can plug in your "New Chat" button/modal here too */}
      </div>
      <ul>
        {chats.map(chat => (
          <li
            key={chat.id}
            className="cursor-pointer p-2 hover:bg-gray-100 rounded"
            onClick={() => onChatSelect(chat)}
          >
            <div className="font-semibold">{chat.name}</div>
            <div className="text-xs text-gray-500">
              Last updated: {new Date(chat.last_message).toLocaleString()}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ChatList;
