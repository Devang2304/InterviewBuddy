import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { HomeIcon, DocumentTextIcon, ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline';
import ApiKeySetup from './components/ApiKeySetup';
import ResumeUpload from './components/ResumeUpload';
import InterviewRoom from './components/InterviewRoom';

const Navigation = () => {
  const location = useLocation();
  
  const navItems = [
    { path: '/', name: 'Setup', icon: HomeIcon },
    { path: '/resume-upload', name: 'Resume', icon: DocumentTextIcon },
    { path: '/interview', name: 'Interview', icon: ChatBubbleLeftRightIcon },
  ];

  return (
    <nav className="bg-white/80 backdrop-blur-md border-b border-gray-100 shadow-soft sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <motion.div 
            className="flex items-center"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Link to="/" className="flex items-center space-x-2 group">
              <span className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
                AI Interviewer
              </span>
            </Link>
          </motion.div>
          <div className="flex space-x-2">
            {navItems.map((item) => {
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`
                    flex items-center space-x-2 px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200
                    ${isActive 
                      ? 'bg-primary-50 text-primary-600 shadow-soft' 
                      : 'text-gray-600 hover:bg-gray-50 hover:text-primary-600'
                    }
                  `}
                >
                  <item.icon className="w-5 h-5" />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
};

const pageVariants = {
  initial: {
    opacity: 0,
    y: 20
  },
  animate: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.5,
      ease: "easeOut"
    }
  },
  exit: {
    opacity: 0,
    y: -20,
    transition: {
      duration: 0.3,
      ease: "easeIn"
    }
  }
};

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50">
        <Navigation />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <AnimatePresence mode="wait">
            <Routes>
              <Route path="/" element={
                <motion.div
                  key="setup"
                  variants={pageVariants}
                  initial="initial"
                  animate="animate"
                  exit="exit"
                >
                  <ApiKeySetup />
                </motion.div>
              } />
              <Route path="/resume-upload" element={
                <motion.div
                  key="resume"
                  variants={pageVariants}
                  initial="initial"
                  animate="animate"
                  exit="exit"
                >
                  <ResumeUpload />
                </motion.div>
              } />
              <Route path="/interview" element={
                <motion.div
                  key="interview"
                  variants={pageVariants}
                  initial="initial"
                  animate="animate"
                  exit="exit"
                >
                  <InterviewRoom />
                </motion.div>
              } />
            </Routes>
          </AnimatePresence>
        </main>
      </div>
    </Router>
  );
}

export default App; 