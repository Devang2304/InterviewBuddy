import React, { useState, useEffect, useRef } from 'react';
import Webcam from 'react-webcam';

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
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="grid grid-cols-2 gap-4">
        {/* Left side - Video feeds */}
        <div className="space-y-4">
          <div className="rounded-lg bg-white p-4 shadow-lg">
            <h3 className="mb-2 text-lg font-semibold">You</h3>
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              videoConstraints={videoConstraints}
              className="w-full rounded-lg"
            />
          </div>
          <div className="rounded-lg bg-white p-4 shadow-lg">
            <h3 className="mb-2 text-lg font-semibold">AI Interviewer</h3>
            <div className="h-[480px] w-full rounded-lg bg-gray-800"></div>
          </div>
        </div>

        {/* Right side - Interview interaction */}
        <div className="space-y-4">
          <div className="rounded-lg bg-white p-6 shadow-lg">
            <h2 className="mb-4 text-2xl font-bold">
              {round.charAt(0).toUpperCase() + round.slice(1)} Round
            </h2>
            <div className="mb-6 rounded-lg bg-gray-50 p-4">
              <h3 className="mb-2 text-lg font-semibold">Current Question:</h3>
              <p className="text-lg">{currentQuestion}</p>
            </div>
            <div className="mb-6">
              <h3 className="mb-2 text-lg font-semibold">Your Answer:</h3>
              <div className="h-32 rounded-lg bg-gray-50 p-4">
                {transcript}
              </div>
            </div>
            <button
              onClick={toggleListening}
              className={`w-full rounded-md px-4 py-2 text-white ${
                isListening
                  ? 'bg-red-600 hover:bg-red-700'
                  : 'bg-green-600 hover:bg-green-700'
              }`}
            >
              {isListening ? 'Stop Recording' : 'Start Recording'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default InterviewRoom; 