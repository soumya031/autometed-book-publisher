import { useState } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

export const useSearch = () => {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const search = async (query, searchType = 'semantic') => {
    try {
      setLoading(true);
      setError(null);
      setResults(null);

      const response = await axios.post('/api/search', {
        query,
        search_type: searchType
      });

      setResults(response.data.results || []);
      toast.success(`Found ${response.data.results?.length || 0} results`);
      
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Search failed');
      setResults(null);
      toast.error('Search failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const clearResults = () => {
    setResults(null);
    setError(null);
  };

  return { search, results, loading, error, clearResults };
}; 