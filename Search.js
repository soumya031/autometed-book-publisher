import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { MagnifyingGlassIcon, DocumentTextIcon, CalendarIcon } from '@heroicons/react/24/outline';
import { useSearch } from '../hooks/useSearch';

const Search = () => {
  const [query, setQuery] = useState('');
  const [searchType, setSearchType] = useState('semantic');
  const { search, results, loading, error } = useSearch();

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    await search(query, searchType);
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Content Search</h1>
        <p className="text-gray-600">Search through your AI-generated content and scraped data</p>
      </div>

      {/* Search Form */}
      <motion.div 
        className="card mb-8"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <form onSubmit={handleSearch} className="space-y-4">
          <div className="flex space-x-4">
            <div className="flex-1">
              <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-2">
                Search Query
              </label>
              <div className="relative">
                <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="text"
                  id="search"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Enter your search query..."
                  className="input-field pl-10"
                  disabled={loading}
                />
              </div>
            </div>
            
            <div className="w-48">
              <label htmlFor="searchType" className="block text-sm font-medium text-gray-700 mb-2">
                Search Type
              </label>
              <select
                id="searchType"
                value={searchType}
                onChange={(e) => setSearchType(e.target.value)}
                className="input-field"
                disabled={loading}
              >
                <option value="semantic">Semantic Search</option>
                <option value="keyword">Keyword Search</option>
                <option value="hybrid">Hybrid Search</option>
              </select>
            </div>
          </div>
          
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                <span>Searching...</span>
              </>
            ) : (
              <>
                <MagnifyingGlassIcon className="h-5 w-5" />
                <span>Search</span>
              </>
            )}
          </button>
        </form>
      </motion.div>

      {/* Search Results */}
      {results && results.length > 0 && (
        <motion.div 
          className="space-y-4"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-gray-900">
              Search Results ({results.length})
            </h2>
            <span className="text-sm text-gray-500">
              {searchType.charAt(0).toUpperCase() + searchType.slice(1)} Search
            </span>
          </div>
          
          {results.map((result, index) => (
            <motion.div
              key={result.id || index}
              className="card hover:shadow-lg transition-shadow duration-200"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <DocumentTextIcon className="h-5 w-5 text-blue-500" />
                  <h3 className="text-lg font-medium text-gray-900">
                    {result.title || `Result ${index + 1}`}
                  </h3>
                </div>
                {result.timestamp && (
                  <div className="flex items-center space-x-1 text-sm text-gray-500">
                    <CalendarIcon className="h-4 w-4" />
                    <span>{new Date(result.timestamp).toLocaleDateString()}</span>
                  </div>
                )}
              </div>
              
              <div className="space-y-3">
                {result.content && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 mb-1">Content</h4>
                    <p className="text-sm text-gray-600 line-clamp-3">
                      {result.content}
                    </p>
                  </div>
                )}
                
                {result.metadata && (
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
                    {Object.entries(result.metadata).map(([key, value]) => (
                      <div key={key} className="bg-gray-50 px-2 py-1 rounded">
                        <span className="font-medium text-gray-600">{key}:</span>
                        <span className="text-gray-500 ml-1">{value}</span>
                      </div>
                    ))}
                  </div>
                )}
                
                {result.score && (
                  <div className="flex items-center space-x-2">
                    <span className="text-sm text-gray-500">Relevance Score:</span>
                    <div className="flex items-center space-x-1">
                      <div className="w-16 bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full" 
                          style={{ width: `${result.score * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-sm text-gray-600">
                        {(result.score * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </motion.div>
      )}

      {/* No Results */}
      {results && results.length === 0 && !loading && (
        <motion.div 
          className="card text-center py-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <MagnifyingGlassIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No results found</h3>
          <p className="text-gray-500">
            Try adjusting your search query or search type to find more content.
          </p>
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
          <h2 className="text-lg font-semibold text-red-800 mb-2">Search Error</h2>
          <p className="text-red-700">{error}</p>
        </motion.div>
      )}
    </div>
  );
};

export default Search; 