import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  ClockIcon, 
  DocumentTextIcon, 
  PlayIcon, 
  CheckCircleIcon,
  ExclamationTriangleIcon,
  CalendarIcon,
  EyeIcon
} from '@heroicons/react/24/outline';
import { useHistory } from '../hooks/useHistory';

const History = () => {
  const [filter, setFilter] = useState('all');
  const [selectedItem, setSelectedItem] = useState(null);
  const { history, loading, error, loadHistory } = useHistory();

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  const filteredHistory = history.filter(item => {
    if (filter === 'all') return true;
    if (filter === 'completed') return item.status === 'completed';
    if (filter === 'failed') return item.status === 'failed';
    if (filter === 'running') return item.status === 'running';
    return true;
  });

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
      case 'failed':
        return <ExclamationTriangleIcon className="h-5 w-5 text-red-500" />;
      case 'running':
        return <PlayIcon className="h-5 w-5 text-blue-500 animate-pulse" />;
      default:
        return <ClockIcon className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      case 'running':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Workflow History</h1>
        <p className="text-gray-600">View and manage your previous workflow executions</p>
      </div>

      {/* Filters */}
      <motion.div 
        className="card mb-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">Filter History</h2>
          <div className="flex space-x-2">
            {['all', 'completed', 'failed', 'running'].map((filterOption) => (
              <button
                key={filterOption}
                onClick={() => setFilter(filterOption)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  filter === filterOption
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {filterOption.charAt(0).toUpperCase() + filterOption.slice(1)}
              </button>
            ))}
          </div>
        </div>
      </motion.div>

      {/* History List */}
      {loading ? (
        <motion.div 
          className="card text-center py-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading history...</p>
        </motion.div>
      ) : filteredHistory.length > 0 ? (
        <motion.div 
          className="space-y-4"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          {filteredHistory.map((item, index) => (
            <motion.div
              key={item.id}
              className="card hover:shadow-lg transition-shadow duration-200 cursor-pointer"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              onClick={() => setSelectedItem(selectedItem?.id === item.id ? null : item)}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {getStatusIcon(item.status)}
                  <div>
                    <h3 className="text-lg font-medium text-gray-900">
                      {item.title || `Workflow ${item.id}`}
                    </h3>
                    <p className="text-sm text-gray-500">
                      {item.description || 'AI-powered content generation workflow'}
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-4">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(item.status)}`}>
                    {item.status}
                  </span>
                  <div className="flex items-center space-x-1 text-sm text-gray-500">
                    <CalendarIcon className="h-4 w-4" />
                    <span>{new Date(item.timestamp).toLocaleDateString()}</span>
                  </div>
                  <EyeIcon className="h-5 w-5 text-gray-400" />
                </div>
              </div>

              {/* Expanded Details */}
              {selectedItem?.id === item.id && (
                <motion.div 
                  className="mt-4 pt-4 border-t border-gray-200"
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <h4 className="text-sm font-medium text-gray-700 mb-2">Input Parameters</h4>
                      <div className="space-y-1 text-sm text-gray-600">
                        {item.input?.url && (
                          <div><strong>URL:</strong> {item.input.url}</div>
                        )}
                        {item.input?.topic && (
                          <div><strong>Topic:</strong> {item.input.topic}</div>
                        )}
                      </div>
                    </div>
                    
                    <div>
                      <h4 className="text-sm font-medium text-gray-700 mb-2">Execution Details</h4>
                      <div className="space-y-1 text-sm text-gray-600">
                        <div><strong>Duration:</strong> {item.duration || 'N/A'}</div>
                        <div><strong>Steps:</strong> {item.steps?.length || 0}</div>
                        {item.error && (
                          <div className="text-red-600"><strong>Error:</strong> {item.error}</div>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Results Preview */}
                  {item.results && (
                    <div className="mt-4">
                      <h4 className="text-sm font-medium text-gray-700 mb-2">Results Preview</h4>
                      <div className="space-y-2">
                        {item.results.scraped_content && (
                          <div className="bg-gray-50 p-3 rounded-lg">
                            <div className="text-xs font-medium text-gray-600 mb-1">Scraped Content</div>
                            <p className="text-sm text-gray-700 line-clamp-2">
                              {item.results.scraped_content}
                            </p>
                          </div>
                        )}
                        {item.results.ai_content && (
                          <div className="bg-blue-50 p-3 rounded-lg">
                            <div className="text-xs font-medium text-blue-600 mb-1">AI Content</div>
                            <p className="text-sm text-blue-700 line-clamp-2">
                              {item.results.ai_content}
                            </p>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </motion.div>
              )}
            </motion.div>
          ))}
        </motion.div>
      ) : (
        <motion.div 
          className="card text-center py-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <ClockIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No history found</h3>
          <p className="text-gray-500">
            {filter === 'all' 
              ? 'No workflow executions found. Start a new workflow to see history here.'
              : `No ${filter} workflows found.`
            }
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
          <h2 className="text-lg font-semibold text-red-800 mb-2">Error Loading History</h2>
          <p className="text-red-700">{error}</p>
        </motion.div>
      )}
    </div>
  );
};

export default History; 