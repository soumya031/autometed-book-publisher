import { useState, useEffect } from 'react';
import axios from 'axios';

export const useSystemStatus = () => {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const checkStatus = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/status');
      setStatus(response.data);
      setError(null);
    } catch (err) {
      setError(err.message);
      setStatus(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkStatus();
    
    // Poll status every 30 seconds
    const interval = setInterval(checkStatus, 30000);
    
    return () => clearInterval(interval);
  }, []);

  return { status, loading, error, checkStatus };
}; 