import React, { useState, useEffect, useRef } from 'react';
import { Input, Button, List, Card, message } from 'antd';
import { SendOutlined, LoadingOutlined } from '@ant-design/icons';
import './ChatInterface.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const ws = new WebSocket('ws://localhost:8000/ws/chat');
      
      ws.onopen = () => {
        ws.send(input);
      };

      ws.onmessage = (event) => {
        const response: Message = {
          role: 'assistant',
          content: event.data,
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, response]);
        setIsLoading(false);
        ws.close();
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        message.error('Failed to connect to the server');
        setIsLoading(false);
      };
    } catch (error) {
      console.error('Error:', error);
      message.error('Failed to send message');
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages-container">
        <List
          dataSource={messages}
          renderItem={(msg) => (
            <List.Item className={`message ${msg.role}`}>
              <Card 
                bordered={false} 
                className={`message-card ${msg.role}`}
              >
                {msg.content}
              </Card>
            </List.Item>
          )}
        />
        <div ref={messagesEndRef} />
      </div>
      <div className="input-container">
        <Input.TextArea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          autoSize={{ minRows: 1, maxRows: 4 }}
          onPressEnter={(e) => {
            if (!e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
        />
        <Button
          type="primary"
          icon={isLoading ? <LoadingOutlined /> : <SendOutlined />}
          onClick={handleSend}
          disabled={isLoading}
        >
          Send
        </Button>
      </div>
    </div>
  );
};

export default ChatInterface; 