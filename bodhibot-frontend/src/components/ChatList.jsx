import React, { useEffect, useState } from 'react';
import axios from 'axios';

const baseUrl = process.env.REACT_APP_API_BASE_URL;

const ChatList = ({ onChatSelect, onChatAdd }) => {
  const [chats, setChats] = useState([]);

  useEffect(() => {
    axios.get(`${baseUrl}chats/my-chats/`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })
      .then(res => setChats(res.data))
      .catch(err => console.error("Failed to load chats", err));
  }, []);

  return (
    <div className="w-full sm:w-1/3 p-4 border-r">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">Your Chats</h2>
        <button onClick={() => {
          const name = prompt("Set a name: ");
          name ? onChatAdd(name) : onChatAdd("UnnamedChat");
          name ? setChats((prev) => [...prev, name]) : setChats((prev) => [...prev, "UnnamedChat"]);
        }}><i className="fa fa-plus" aria-hidden="true"></i>New</button>
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
