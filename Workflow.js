import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  PlayIcon, 
  DocumentTextIcon, 
  LightBulbIcon, 
  CheckCircleIcon,
  ClockIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import { useWorkflow } from '../hooks/useWorkflow';

const Workflow = () => {
  const [url, setUrl] = useState('');
  const [topic, setTopic] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const { runWorkflow, progress, results, error } = useWorkflow();

  const steps = [
    { id: 1, name: 'Scraping', icon: DocumentTextIcon, status: 'inactive' },
    { id: 2, name: 'AI Generation', icon: LightBulbIcon, status: 'inactive' },
    { id: 3, name: 'Review', icon: CheckCircleIcon, status: 'inactive' },
    { id: 4, name: 'Complete', icon: CheckCircleIcon, status: 'inactive' }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!url && !topic) {
      alert('Please provide either a URL or topic');
      return;
    }

    setIsRunning(true);
    try {
      await runWorkflow({ url, topic });
    } catch (err) {
      console.error('Workflow error:', err);
    } finally {
      setIsRunning(false);
    }
  };

  const getStepStatus = (stepId) => {
    if (!isRunning && !progress) return 'inactive';
    if (progress && progress.currentStep >= stepId) {
      return progress.currentStep === stepId ? 'active' : 'completed';
    }
    return 'inactive';
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">AI Workflow</h1>
        <p className="text-gray-600">Automate your content creation process with AI-powered writing</p>
      </div>

      {/* Input Form */}
      <motion.div 
        className="card mb-8"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h2 className="text-xl font-semibold mb-4">Start New Workflow</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
              Source URL (Optional)
            </label>
            <input
              type="url"
              id="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com/article"
              className="input-field"
              disabled={isRunning}
            />
          </div>
          
          <div>
            <label htmlFor="topic" className="block text-sm font-medium text-gray-700 mb-2">
              Topic (Optional)
            </label>
            <input
              type="text"
              id="topic"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Enter a topic for AI content generation"
              className="input-field"
              disabled={isRunning}
            />
          </div>
          
          <button
            type="submit"
            disabled={isRunning || (!url && !topic)}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            {isRunning ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                <span>Running...</span>
              </>
            ) : (
              <>
                <PlayIcon className="h-5 w-5" />
                <span>Start Workflow</span>
              </>
            )}
          </button>
        </form>
      </motion.div>

      {/* Progress Steps */}
      {isRunning && (
        <motion.div 
          className="card mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <h2 className="text-xl font-semibold mb-6">Workflow Progress</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {steps.map((step, index) => {
              const status = getStepStatus(step.id);
              return (
                <div
                  key={step.id}
                  className={`flex flex-col items-center p-4 rounded-lg border-2 transition-all duration-300 ${
                    status === 'active' ? 'step-active' :
                    status === 'completed' ? 'step-completed' :
                    'step-inactive'
                  }`}
                >
                  <step.icon className={`h-8 w-8 mb-2 ${
                    status === 'active' ? 'animate-pulse' : ''
                  }`} />
                  <span className="text-sm font-medium">{step.name}</span>
                  {status === 'active' && (
                    <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-white h-2 rounded-full animate-pulse" style={{ width: '60%' }}></div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
          
          {progress && (
            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-blue-800">
                <strong>Current Step:</strong> {progress.currentStepName}
              </p>
              {progress.message && (
                <p className="text-sm text-blue-700 mt-1">{progress.message}</p>
              )}
            </div>
          )}
        </motion.div>
      )}

      {/* Results */}
      {results && !isRunning && (
        <motion.div 
          className="card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <h2 className="text-xl font-semibold mb-4">Workflow Results</h2>
          <div className="space-y-4">
            {results.scraped_content && (
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Scraped Content</h3>
                <div className="bg-gray-50 p-4 rounded-lg max-h-40 overflow-y-auto">
                  <p className="text-sm text-gray-700">{results.scraped_content}</p>
                </div>
              </div>
            )}
            
            {results.ai_content && (
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">AI Generated Content</h3>
                <div className="bg-blue-50 p-4 rounded-lg max-h-40 overflow-y-auto">
                  <p className="text-sm text-blue-800">{results.ai_content}</p>
                </div>
              </div>
            )}
            
            {results.review && (
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">AI Review</h3>
                <div className="bg-green-50 p-4 rounded-lg max-h-40 overflow-y-auto">
                  <p className="text-sm text-green-800">{results.review}</p>
                </div>
              </div>
            )}
          </div>
        </motion.div>
      )}

      {/* Error Display */}
      {error && (
        <motion.div 
          className="card border-red-200 bg-red-50"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="flex items-center space-x-2 mb-2">
            <ExclamationTriangleIcon className="h-5 w-5 text-red-500" />
            <h2 className="text-lg font-semibold text-red-800">Error</h2>
          </div>
          <p className="text-red-700">{error}</p>
        </motion.div>
      )}
    </div>
  );
};

export default Workflow; 