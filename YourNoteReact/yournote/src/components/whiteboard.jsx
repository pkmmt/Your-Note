import React, { useState, useEffect } from 'react';
import { useRef } from 'react';
import { Tabs, TabList, Tab, TabPanel } from '@/components/ui/tabs';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { MessageSquare, Edit, Search, Save, Share, Settings } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

const WhiteboardTab = ({ canvasRef }) => {
    useEffect(() => {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
      let isDrawing = false;
      let lastX = 0;
      let lastY = 0;
  
      const draw = (e) => {
        if (!isDrawing) return;
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke();
        [lastX, lastY] = [e.offsetX, e.offsetY];
      };
  
      canvas.addEventListener('mousedown', (e) => {
        isDrawing = true;
        [lastX, lastY] = [e.offsetX, e.offsetY];
      });
      canvas.addEventListener('mousemove', draw);
      canvas.addEventListener('mouseup', () => isDrawing = false);
      canvas.addEventListener('mouseout', () => isDrawing = false);
  
      return () => {
        canvas.removeEventListener('mousedown', () => {});
        canvas.removeEventListener('mousemove', draw);
        canvas.removeEventListener('mouseup', () => {});
        canvas.removeEventListener('mouseout', () => {});
      };
    }, []);
  
    return (
      <div className="p-4">
        <h2 className="text-2xl font-bold mb-4">Interactive Whiteboard</h2>
        <canvas
          ref={canvasRef}
          width={800}
          height={400}
          className="border border-gray-300 rounded"
        />
        <Button className="mt-4">Analyze Whiteboard</Button>
      </div>
    );
  };
  export default WhiteboardTab