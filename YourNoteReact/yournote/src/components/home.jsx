import React, { useState, useEffect } from 'react';
import { useRef } from 'react';
import { Tabs, TabList, Tab, TabPanel } from '@/components/ui/tabs';
import ChatTab from './chat';
import ExamTab from './exam';
import NotesTab from './notes';
import WhiteboardTab from './whiteboard';




const LearningPlatform = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [messages, setMessages] = useState([]);
  const [notes, setNotes] = useState([]);
  const [currentNote, setCurrentNote] = useState(null);
  const [showAnalysis, setShowAnalysis] = useState(false);
  const canvasRef = useRef(null);

  const formatLastEdited = (timestamp) => {
    const dt = new Date(timestamp);
    return `Last edited ${dt.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Interactive Learning Platform</h1>
      
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabList>
          <Tab value={0}>Whiteboard</Tab>
          <Tab value={1}>AI Chat</Tab>
          <Tab value={2}>Notes</Tab>
          <Tab value={3}>Exams</Tab>
        </TabList>

        <TabPanel value={0}>
          <WhiteboardTab canvasRef={canvasRef} />
        </TabPanel>

        <TabPanel value={1}>
          <ChatTab messages={messages} setMessages={setMessages} />
        </TabPanel>

        <TabPanel value={2}>
          <NotesTab
            notes={notes}
            setNotes={setNotes}
            currentNote={currentNote}
            setCurrentNote={setCurrentNote}
            showAnalysis={showAnalysis}
            setShowAnalysis={setShowAnalysis}
            formatLastEdited={formatLastEdited}
          />
        </TabPanel>

        <TabPanel value={3}>
          <ExamTab />
        </TabPanel>
      </Tabs>
    </div>
  );
};
export default LearningPlatform