import React from "react";
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import ReactMarkdown from 'react-markdown';


const MessageRender = ({chatMessage}) => {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypeRaw]}
    >
      {chatMessage}
    </ReactMarkdown>
  );
};

export default MessageRender;