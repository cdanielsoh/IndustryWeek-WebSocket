import React, { useState, useEffect } from 'react';
import './App.css';

function ConnectionStatus({ isConnected }) {
  return (
    <div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
      {isConnected ? 'Connected' : 'Disconnected'}
    </div>
  );
}

function App() {
  const [messages, setMessages] = useState([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8765');

    socket.onopen = () => {
      console.log('WebSocket connection established');
      setIsConnected(true);
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages((prevMessages) => [...prevMessages, data.message]);
    };

    socket.onclose = () => {
      console.log('WebSocket connection closed');
      setIsConnected(false);
    };

    return () => {
      socket.close();
    };
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>WebSocket Messages</h1>
        <ConnectionStatus isConnected={isConnected} />
        <div className="message-container">
          {messages.map((message, index) => (
            <p key={index} className="message">{message}</p>
          ))}
        </div>
      </header>
    </div>
  );
}

export default App;