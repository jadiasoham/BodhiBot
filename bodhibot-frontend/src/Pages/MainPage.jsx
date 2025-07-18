import React, { useState } from 'react';
import ChatList from '../components/ChatList';

const MainPage = () => {
  const [selectedChat, setSelectedChat] = useState(null);

  return (
    <div className="flex h-screen">
      <ChatList onChatSelect={setSelectedChat} />
      <div className="flex-1 p-4">
        {selectedChat ? (
          <div>
            {/* <ChatScreen chat={selectedChat} /> */}
            <p className="text-lg font-medium">Chat with: {selectedChat.name}</p>
            {/* Temporary placeholder */}
          </div>
        ) : (
          <p className="text-gray-500">Select a chat to begin</p>
        )}
      </div>
    </div>
  );
};

export default MainPage;
