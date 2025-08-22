import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import { useAuth } from '../../../context/AuthContext';
import MessageRender from './MessageRender';

const ChatView = ({ chatName }) => {
	const [messages, setMessages] = useState([]);
	const [nextCursor, setNextCursor] = useState(null);
	const [socket, setSocket] = useState(null);
	const [isLoadingMore, setIsLoadingMore] = useState(false);
	const messageContainerRef = useRef(null);
	const topSentinelRef = useRef(null);
	const [newMessage, setNewMessage] = useState('');
	const { user } = useAuth();

	const baseUrl = process.env.REACT_APP_API_BASE_URL;
	const wsUrl = process.env.REACT_APP_WEBSOCKET_URL;

	const sendMessage = () => {
		if (socket && socket.readyState === WebSocket.OPEN && newMessage.trim()) {
			console.log("Sending! 1")
			socket.send(JSON.stringify({
				message: newMessage
			}));

			console.log(user);

			const userMessage = {
				id: `local-${new Date().now}-${Math.random()}`,
				content: newMessage,
				sender: user.username,
				timestamp: new Date().toLocaleString(),
			};

			setMessages((prev) => [...prev, userMessage]);
			setNewMessage('');
		}
	};

	const handleKeyDown = (e) => {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			sendMessage();
		}
	};

	useEffect(() => {
		fetchMessages(); // Initial fetch
		connectWebSocket();

		const observer = new IntersectionObserver(handleScrollUp, {
			root: messageContainerRef.current,
			threshold: 0.1,
		});

		if (topSentinelRef.current) observer.observe(topSentinelRef.current);

		return () => {
			if (socket) socket.close();
			if (topSentinelRef.current) observer.unobserve(topSentinelRef.current);
		};
	}, [chatName]);

	const fetchMessages = async (cursor = null) => {
		const params = { name: chatName };
		if (cursor) params.cursor = cursor;

		try {
			setIsLoadingMore(true);
			const res = await axios.get(`${baseUrl}chats/messages/`, {
				params,
				headers: {
					Authorization: `Bearer ${localStorage.getItem('access_token')}`,
				},
			});
			console.log(res?.data)
			const newMessages = res?.data?.data?.results.reverse();
			setMessages((prev) => [...newMessages, ...prev]);
			setNextCursor(res?.data?.data?.next?.split('cursor=')[1] || null);
		} catch (err) {
			console.error('Failed to fetch messages:', err);
		} finally {
			setIsLoadingMore(false);
		}
	};

	const connectWebSocket = () => {
		const ws = new WebSocket(`${wsUrl}${chatName?.trim()?.replace(/\s+/g, "") || "someSafeGenericName"}/?token=${localStorage.getItem('access_token')}`);

		ws.onmessage = (event) => {
			const data = JSON.parse(event.data);
			if (data.type === 'chat.message') {
				setMessages((prev) => [...prev, data.message]);
			}
		};

		ws.onerror = (err) => console.error("WebSocket error:", err);

		setSocket(ws);
	};

	const handleScrollUp = (entries) => {
		const top = entries[0];
		if (top.isIntersecting && nextCursor && !isLoadingMore) {
			const container = messageContainerRef.current;
			const scrollPosBefore = container.scrollHeight;

			fetchMessages(nextCursor).then(() => {
				requestAnimationFrame(() => {
					const scrollPosAfter = container.scrollHeight;
					container.scrollTop = scrollPosAfter - scrollPosBefore;
				});
			});
		}
	};

	return (
		<div className="flex flex-col h-full"> {/* This is your main chat container */}
			{/* MESSAGE LIST */}
			<div ref={messageContainerRef} className="flex-1 overflow-y-auto p-4 bg-gray-50">
				<div ref={topSentinelRef}></div>
				{messages.map((msg) => (
					<div key={msg.id} className="my-2 flex flex-col">
						<div className={`max-w-[75%] px-4 py-2 rounded-lg ${msg.sender !== 'BodhiBot' ? 'bg-blue-500 text-white self-end ml-auto' : 'bg-gray-200 text-black self-start'}`}>
							{/* Render Markdown here */}
							<MessageRender chatMessage= {msg.content} />
						</div>
						<div className={`text-xs text-gray-500 mt-1 ${msg.sender !== 'BodhiBot' ? 'text-right' : 'text-left'}`}>
							{new Date(msg.timestamp).toLocaleString()}
						</div>
					</div>
				))}
				{isLoadingMore && <p className="text-center text-sm text-gray-400 mt-2">Loading more...</p>}
			</div>

			{/* MESSAGE INPUT BOX */}
			{/* REMOVED: fixed bottom-0 right-0 */}
			<div className="p-4 bg-white border-t flex gap-2 w-full"> {/* Changed w-[70%] to w-full here */}
				<textarea
					rows="1"
					value={newMessage}
					onChange={(e) => setNewMessage(e.target.value)}
					onKeyDown={handleKeyDown}
					placeholder="Type your message..."
					className="flex-1 border rounded px-3 py-2 resize-none focus:outline-none focus:ring"
				/>
				<button
					onClick={sendMessage}
					className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
				>
					Send
				</button>
			</div>
		</div>
	);
};

export default ChatView;