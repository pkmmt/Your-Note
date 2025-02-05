import React, { useState, useEffect } from 'react';
import { useRef } from 'react';
import { Tabs, TabList, Tab, TabPanel } from '@/components/ui/tabs';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { MessageSquare, Edit, Search, Save, Share, Settings } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';




const ChatTab = ({ messages, setMessages }) => {
    const [input, setInput] = useState('');
    const messagesEndRef = useRef(null);
  
    const scrollToBottom = () => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };
  
    useEffect(() => {
      scrollToBottom();
    }, [messages]);
  
    const handleSend = () => {
      if (!input.trim()) return;
      
      const newMessage = { role: 'user', content: input };
      setMessages([...messages, newMessage]);
      setInput('');
      
      // Simulate AI response
      setTimeout(() => {
        const aiResponse = { role: 'assistant', content: 'AI response simulation' };
        setMessages(prev => [...prev, aiResponse]);
      }, 1000);
    };
  
    return (
      <div className="p-4">
        <h2 className="text-2xl font-bold mb-4">AI Chat Assistant</h2>
        <div className="h-96 overflow-y-auto border rounded p-4 mb-4">
          {messages.map((msg, idx) => (
            <div key={idx} className={`mb-4 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
              <div className={`inline-block p-2 rounded ${msg.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}>
                {msg.content}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        <div className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask anything..."
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          />
          <Button onClick={handleSend}>Send</Button>
        </div>
      </div>
    );
  };
  export default ChatTab