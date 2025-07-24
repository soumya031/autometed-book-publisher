import { useState } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

export const useWorkflow = () => {
  const [progress, setProgress] = useState(null);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const runWorkflow = async (params) => {
    try {
      setError(null);
      setResults(null);
      setProgress({ currentStep: 1, currentStepName: 'Initializing...', message: 'Starting workflow...' });

      const response = await axios.post('/api/workflow', params, {
        timeout: 300000, // 5 minutes timeout
        onUploadProgress: (progressEvent) => {
          // Handle upload progress if needed
        }
      });

      // Simulate progress updates
      const steps = [
        { step: 1, name: 'Scraping', message: 'Scraping content from source...' },
        { step: 2, name: 'AI Generation', message: 'Generating AI content...' },
        { step: 3, name: 'Review', message: 'Reviewing and refining content...' },
        { step: 4, name: 'Complete', message: 'Workflow completed successfully!' }
      ];

      for (let i = 0; i < steps.length; i++) {
        setProgress(steps[i]);
        await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate step duration
      }

      setResults(response.data);
      setProgress(null);
      toast.success('Workflow completed successfully!');
      
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Workflow failed');
      setProgress(null);
      toast.error('Workflow failed. Please try again.');
    }
  };

  const resetWorkflow = () => {
    setProgress(null);
    setResults(null);
    setError(null);
  };

  return { runWorkflow, progress, results, error, resetWorkflow };
}; 