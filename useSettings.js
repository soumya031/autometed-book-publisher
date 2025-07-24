import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

export const useSettings = () => {
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState(null);

  const loadSettings = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await axios.get('/api/settings');
      setSettings(response.data.settings || {});
      
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to load settings');
    } finally {
      setLoading(false);
    }
  }, []);

  const updateSettings = async (newSettings) => {
    try {
      setLoading(true);
      setError(null);

      const response = await axios.put('/api/settings', newSettings);
      setSettings(response.data.settings);
      toast.success('Settings updated successfully');
      
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to update settings');
      toast.error('Failed to update settings');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const testConnection = async () => {
    try {
      setConnectionStatus({ connected: false, message: 'Testing connection...' });
      
      const response = await axios.post('/api/settings/test-connection');
      setConnectionStatus({
        connected: response.data.connected,
        message: response.data.message
      });
      
      if (response.data.connected) {
        toast.success('Connection test successful');
      } else {
        toast.error('Connection test failed');
      }
      
    } catch (err) {
      setConnectionStatus({
        connected: false,
        message: err.response?.data?.error || err.message || 'Connection test failed'
      });
      toast.error('Connection test failed');
    }
  };

  useEffect(() => {
    loadSettings();
  }, [loadSettings]);

  return { 
    settings, 
    loading, 
    error, 
    connectionStatus,
    loadSettings, 
    updateSettings, 
    testConnection 
  };
}; 