import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Webcam from 'react-webcam';
import { MicrophoneIcon, VideoCameraIcon, UserIcon } from '@heroicons/react/24/outline';

function InterviewRoom() {
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [round, setRound] = useState('resume');
  const [isProcessing, setIsProcessing] = useState(false);
  const webcamRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const wsRef = useRef(null);

  useEffect(() => {
    // Initialize WebSocket connection
    const ws = new WebSocket('ws://localhost:5000');
    wsRef.current = ws;

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'question') {
        setCurrentQuestion(data.content);
      } else if (data.type === 'round_change') {
        setRound(data.round);
      }
    };

    return () => {
      ws.close();
      if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
        mediaRecorderRef.current.stop();
      }
    };
  }, []);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = async (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
          
          // Create a blob from the chunks
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
          
          await sendAudioChunk(audioBlob);
          
          audioChunksRef.current = [];
        }
      };

      
      mediaRecorder.start(10000);
      setIsRecording(true);
    } catch (error) {
      console.error('Error starting recording:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
    }
  };

  const sendAudioChunk = async (audioBlob) => {
    setIsProcessing(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/transcribe-chunk', {
        method: 'POST',
        body: audioBlob,
        headers: {
          'Content-Type': 'audio/webm',
          'Accept': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setTranscript(prevTranscript => prevTranscript + ' ' + data.transcription);
      } else {
        console.error('Failed to transcribe audio chunk');
      }
    } catch (error) {
      console.error('Error sending audio chunk:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const toggleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
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
                    {isProcessing && (
                      <div className="mt-2 text-sm text-gray-500">
                        Processing audio...
                      </div>
                    )}
                  </div>
                </motion.div>

                <motion.button
                  onClick={toggleRecording}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className={`w-full button-primary flex items-center justify-center space-x-2 ${
                    isRecording ? 'bg-red-600 hover:bg-red-700' : ''
                  }`}
                >
                  <MicrophoneIcon className="w-5 h-5" />
                  <span>{isRecording ? 'Stop Recording' : 'Start Recording'}</span>
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