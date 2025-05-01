import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ApiKeySetup from './components/ApiKeySetup';
import ResumeUpload from './components/ResumeUpload';
import InterviewRoom from './components/InterviewRoom';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Routes>
          <Route path="/" element={<ApiKeySetup />} />
          <Route path="/resume-upload" element={<ResumeUpload />} />
          <Route path="/interview" element={<InterviewRoom />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App; 