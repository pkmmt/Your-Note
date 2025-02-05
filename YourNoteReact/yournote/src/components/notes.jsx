import React, { useState, useEffect } from 'react';
import { useRef } from 'react';
import { Tabs, TabList, Tab, TabPanel } from '@/components/ui/tabs';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { MessageSquare, Edit, Search, Save, Share, Settings } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';


const NotesTab = ({ notes, setNotes, currentNote, setCurrentNote, showAnalysis, setShowAnalysis, formatLastEdited }) => {
    const handleNewNote = () => {
      const newNote = {
        title: "Untitled Document",
        content: "",
        created: Date.now(),
        last_edited: Date.now(),
        id: notes.length
      };
      setNotes([...notes, newNote]);
      setCurrentNote(newNote.id);
    };
  
    const handleNoteChange = (field, value) => {
      const updatedNotes = notes.map(note =>
        note.id === currentNote
          ? { ...note, [field]: value, last_edited: Date.now() }
          : note
      );
      setNotes(updatedNotes);
    };
  
    return (
      <div className="grid grid-cols-4 gap-4 p-4">
        <div className="col-span-1 border-r pr-4">
          <Button onClick={handleNewNote} className="w-full mb-4">+ New Document</Button>
          <div className="space-y-2">
            {notes.map(note => (
              <Card
                key={note.id}
                className={`cursor-pointer ${currentNote === note.id ? 'bg-gray-100' : ''}`}
                onClick={() => setCurrentNote(note.id)}
              >
                <CardContent className="p-4">
                  <h3 className="font-medium">{note.title}</h3>
                  <p className="text-sm text-gray-500">{formatLastEdited(note.last_edited)}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
  
        <div className="col-span-2">
          {currentNote !== null && notes.find(n => n.id === currentNote) && (
            <div className="space-y-4">
              <div className="flex gap-2">
                <Button><Edit size={16} /></Button>
                <Button><Search size={16} /></Button>
                <Button><Save size={16} /></Button>
                <Button><Share size={16} /></Button>
                <Button><Settings size={16} /></Button>
              </div>
              <Input
                value={notes.find(n => n.id === currentNote).title}
                onChange={(e) => handleNoteChange('title', e.target.value)}
                placeholder="Title"
              />
              <Textarea
                value={notes.find(n => n.id === currentNote).content}
                onChange={(e) => handleNoteChange('content', e.target.value)}
                placeholder="Start writing..."
                className="h-96"
              />
            </div>
          )}
        </div>
  
        <div className="col-span-1">
          <Card>
            <CardHeader>
              <CardTitle>Analysis Tools</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <Button className="w-full" onClick={() => setShowAnalysis(!showAnalysis)}>
                  {showAnalysis ? 'Hide Analysis' : 'Show Analysis'}
                </Button>
                {showAnalysis && (
                  <>
                    <Button className="w-full">Generate Summary</Button>
                    <Input placeholder="Summarize specific topic" />
                    <Button className="w-full">Generate Topic Summary</Button>
                    <Button className="w-full">Analyze Notes</Button>
                  </>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  };
  export default NotesTab