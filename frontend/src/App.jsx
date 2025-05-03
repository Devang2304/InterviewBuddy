import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import ApiKeySetup from './components/ApiKeySetup';
import ResumeUpload from './components/ResumeUpload';
import InterviewRoom from './components/InterviewRoom';

const Navigation = () => {
  const location = useLocation();
  
  return (
    <nav className="bg-gradient-to-r from-indigo-600 to-purple-600 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="text-white text-xl font-bold hover:text-indigo-100 transition-colors duration-200">
              AI Interviewer
            </Link>
          </div>
          <div className="flex space-x-4">
            <Link
              to="/"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                location.pathname === '/'
                  ? 'bg-white text-indigo-600'
                  : 'text-white hover:bg-white/20'
              }`}
            >
              Setup
            </Link>
            <Link
              to="/resume-upload"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                location.pathname === '/resume-upload'
                  ? 'bg-white text-indigo-600'
                  : 'text-white hover:bg-white/20'
              }`}
            >
              Resume
            </Link>
            <Link
              to="/interview"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                location.pathname === '/interview'
                  ? 'bg-white text-indigo-600'
                  : 'text-white hover:bg-white/20'
              }`}
            >
              Interview
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
        <Navigation />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="animate-fade-in">
            <Routes>
              <Route path="/" element={<ApiKeySetup />} />
              <Route path="/resume-upload" element={<ResumeUpload />} />
              <Route path="/interview" element={<InterviewRoom />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
}

export default App; 