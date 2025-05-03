import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Webcam from 'react-webcam';
import { MicrophoneIcon, VideoCameraIcon, UserIcon } from '@heroicons/react/24/outline';

function InterviewRoom() {
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [round, setRound] = useState('resume');
  const webcamRef = useRef(null);
  const recognitionRef = useRef(null);

  useEffect(() => {
    // Initialize WebSocket connection
    const ws = new WebSocket('ws://localhost:5000');

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'question') {
        setCurrentQuestion(data.content);
      } else if (data.type === 'round_change') {
        setRound(data.round);
      }
    };

    // Initialize speech recognition
    if ('webkitSpeechRecognition' in window) {
      const recognition = new window.webkitSpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;

      recognition.onresult = (event) => {
        const current = event.resultIndex;
        const transcript = event.results[current][0].transcript;
        setTranscript(transcript);
      };

      recognition.onend = () => {
        if (isListening) {
          recognition.start();
        }
      };

      recognitionRef.current = recognition;
    }

    return () => {
      ws.close();
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, []);

  const toggleListening = () => {
    if (isListening) {
      recognitionRef.current?.stop();
    } else {
      recognitionRef.current?.start();
    }
    setIsListening(!isListening);
  };

  const videoConstraints = {
    width: 640,
    height: 480,
    facingMode: 'user',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50 p-6"
    >
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card overflow-hidden mb-6"
        >
          <div className="bg-gradient-to-r from-primary-600 to-secondary-600 p-8">
            <h2 className="text-3xl font-bold text-white text-center">
              {round.charAt(0).toUpperCase() + round.slice(1)} Round
            </h2>
            <p className="mt-2 text-center text-primary-100">
              AI-Powered Interview Session
            </p>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left side - Video feeds */}
          <div className="space-y-6">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
              className="card overflow-hidden"
            >
              <div className="p-4 bg-gray-50 border-b">
                <h3 className="text-lg font-semibold text-gray-800 flex items-center">
                  <VideoCameraIcon className="w-5 h-5 mr-2 text-primary-600" />
                  Your Camera
                </h3>
              </div>
              <div className="p-4">
                <Webcam
                  audio={false}
                  ref={webcamRef}
                  screenshotFormat="image/jpeg"
                  videoConstraints={videoConstraints}
                  className="w-full rounded-xl shadow-soft"
                />
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
              className="card overflow-hidden"
            >
              <div className="p-4 bg-gray-50 border-b">
                <h3 className="text-lg font-semibold text-gray-800 flex items-center">
                  <UserIcon className="w-5 h-5 mr-2 text-secondary-600" />
                  AI Interviewer
                </h3>
              </div>
              <div className="p-4">
                <div className="h-[480px] w-full rounded-xl bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center">
                  <motion.div
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.5 }}
                    className="text-center"
                  >
                    <motion.div
                      className="w-24 h-24 bg-primary-600 rounded-full mx-auto mb-4"
                      animate={{
                        scale: [1, 1.1, 1],
                        opacity: [0.7, 1, 0.7],
                      }}
                      transition={{
                        duration: 2,
                        repeat: Infinity,
                        ease: "easeInOut"
                      }}
                    />
                    <p className="text-gray-400">AI Interviewer is ready</p>
                  </motion.div>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Right side - Interview interaction */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
            className="space-y-6"
          >
            <div className="card overflow-hidden">
              <div className="p-6">
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.6 }}
                  className="mb-6"
                >
                  <h3 className="text-lg font-semibold text-gray-800 mb-2">Current Question</h3>
                  <div className="bg-primary-50 rounded-xl p-4 border border-primary-100">
                    <p className="text-lg text-gray-800">{currentQuestion || 'Waiting for the first question...'}</p>
                  </div>
                </motion.div>

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.7 }}
                  className="mb-6"
                >
                  <h3 className="text-lg font-semibold text-gray-800 mb-2">Your Answer</h3>
                  <div className="bg-gray-50 rounded-xl p-4 border border-gray-200 min-h-[200px]">
                    <p className="text-gray-700">{transcript || 'Your answer will appear here...'}</p>
                  </div>
                </motion.div>

                <motion.button
                  onClick={toggleListening}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className={`w-full button-primary flex items-center justify-center space-x-2 ${
                    isListening ? 'bg-red-600 hover:bg-red-700' : ''
                  }`}
                >
                  <MicrophoneIcon className="w-5 h-5" />
                  <span>{isListening ? 'Stop Recording' : 'Start Recording'}</span>
                </motion.button>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
}

export default InterviewRoom; 