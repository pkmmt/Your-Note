import React, { useState, useEffect } from 'react';
import { useRef } from 'react';
import { Tabs, TabList, Tab, TabPanel } from '@/components/ui/tabs';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { MessageSquare, Edit, Search, Save, Share, Settings } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

const ExamTab = () => {
    const [examTitle, setExamTitle] = useState('');
    const [subject, setSubject] = useState('');
    const [duration, setDuration] = useState(60);
    const [questions, setQuestions] = useState([]);
  
    return (
      <div className="p-4">
        <h2 className="text-2xl font-bold mb-4">Interactive Exam Platform</h2>
        <Card>
          <CardHeader>
            <CardTitle>Create New Exam</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <Input
                placeholder="Exam Title"
                value={examTitle}
                onChange={(e) => setExamTitle(e.target.value)}
              />
              <Input
                placeholder="Subject"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
              />
              <Input
                type="number"
                placeholder="Duration (minutes)"
                value={duration}
                onChange={(e) => setDuration(parseInt(e.target.value))}
                min={1}
              />
              <Button className="w-full">Create Exam</Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  };
  export default ExamTab