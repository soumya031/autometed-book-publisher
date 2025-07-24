import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

export const useHistory = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadHistory = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await axios.get('/api/history');
      setHistory(response.data.history || []);
      
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to load history');
      toast.error('Failed to load history');
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteHistoryItem = async (id) => {
    try {
      await axios.delete(`/api/history/${id}`);
      setHistory(prev => prev.filter(item => item.id !== id));
      toast.success('History item deleted');
    } catch (err) {
      toast.error('Failed to delete history item');
    }
  };

  const clearHistory = async () => {
    try {
      await axios.delete('/api/history');
      setHistory([]);
      toast.success('History cleared');
    } catch (err) {
      toast.error('Failed to clear history');
    }
  };

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  return { history, loading, error, loadHistory, deleteHistoryItem, clearHistory };
}; 