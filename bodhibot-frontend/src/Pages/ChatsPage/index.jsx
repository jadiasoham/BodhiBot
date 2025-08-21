import React, { useState } from 'react';
import ChatList from './components/ChatList';
import ChatView from './components/ChatView';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';

const baseUrl = process.env.REACT_APP_API_BASE_URL;

const ChatsPage = () => {
	const { logout } = useAuth();
	const [chatList, setChatList] = useState([]);
	const [selectedChat, setSelectedChat] = useState(null);

	const addNewChat = async () => {
		try {
			const response = await axios.post(`${baseUrl}chats/my-chats/`, {
				name: "ThisNewChat"
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
			{/* Chat Layout */}
			<div className="flex h-[calc(100vh-64px)] overflow-hidden"> {/* Adjusted for navbar height */}
				{/* Chat List - 30% */}
				<div className="w-[30%] max-w-sm border-r border-gray-300 overflow-y-auto bg-gray-50">
					<ChatList
						chats={chatList}
						onChatSelect={setSelectedChat}
						onChatAdd={addNewChat}
					/>
				</div>

				{/* Chat View - 70% */}
				<div className="w-[70%] flex-1 p-4 overflow-y-auto">
					{selectedChat ? (
						<ChatView chatName={selectedChat.room_name || selectedChat.name} />
					) : (
						<div className="text-center text-gray-500 mt-10 text-lg">
							Select a chat to begin
						</div>
					)}
				</div>
			</div>
		</>
	);
};

export default ChatsPage;
