import React, { useState, useEffect } from "react";
import { FaAdd } from "react-icons/fa"

const ChatList = ({ onChatSelect, onChatAdd }) => {
  const [chats, setChats] = useState([]);
  

  return (
    <div className="w-full p-4 border-r">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">Your Chats</h2>
        <button className='btn btn-primary' onClick={onChatAdd}>New</button>
      </div>

      {Array.isArray(chats) && chats.length > 0 ? (
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
      ) : (
        <h3>Start a new Chat</h3>
      )}
    </div>
  );
};

export default ChatList;