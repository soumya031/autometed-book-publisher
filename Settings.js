import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Cog6ToothIcon, 
  KeyIcon, 
  ServerIcon, 
  CpuChipIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import { useSettings } from '../hooks/useSettings';

const Settings = () => {
  const [activeTab, setActiveTab] = useState('general');
  const { 
    settings, 
    loading, 
    error, 
    updateSettings, 
    testConnection,
    connectionStatus 
  } = useSettings();

  const [formData, setFormData] = useState({
    apiKey: '',
    maxTokens: 1000,
    temperature: 0.7,
    model: 'gemini-pro',
    databasePath: './chroma_db',
    enableLogging: true,
    autoSave: true
  });

  useEffect(() => {
    if (settings) {
      setFormData(settings);
    }
  }, [settings]);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSave = async () => {
    try {
      await updateSettings(formData);
    } catch (err) {
      console.error('Failed to save settings:', err);
    }
  };

  const tabs = [
    { id: 'general', name: 'General', icon: Cog6ToothIcon },
    { id: 'ai', name: 'AI Settings', icon: CpuChipIcon },
    { id: 'database', name: 'Database', icon: ServerIcon },
    { id: 'security', name: 'Security', icon: KeyIcon }
  ];

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Settings</h1>
        <p className="text-gray-600">Configure your AI Book Publication system</p>
      </div>

      {/* Tab Navigation */}
      <motion.div 
        className="card mb-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <tab.icon className="h-5 w-5" />
                <span>{tab.name}</span>
              </button>
            ))}
          </nav>
        </div>
      </motion.div>

      {/* Tab Content */}
      <motion.div 
        className="card"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading settings...</p>
          </div>
        ) : (
          <div className="space-y-6">
            {/* General Settings */}
            {activeTab === 'general' && (
              <div className="space-y-4">
                <h2 className="text-xl font-semibold text-gray-900">General Settings</h2>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Enable Logging
                    </label>
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        name="enableLogging"
                        checked={formData.enableLogging}
                        onChange={handleInputChange}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="ml-2 text-sm text-gray-700">Enable system logging</span>
                    </label>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Auto Save
                    </label>
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        name="autoSave"
                        checked={formData.autoSave}
                        onChange={handleInputChange}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="ml-2 text-sm text-gray-700">Auto-save workflow results</span>
                    </label>
                  </div>
                </div>
              </div>
            )}

            {/* AI Settings */}
            {activeTab === 'ai' && (
              <div className="space-y-4">
                <h2 className="text-xl font-semibold text-gray-900">AI Configuration</h2>
                
                <div>
                  <label htmlFor="apiKey" className="block text-sm font-medium text-gray-700 mb-2">
                    API Key
                  </label>
                  <input
                    type="password"
                    id="apiKey"
                    name="apiKey"
                    value={formData.apiKey}
                    onChange={handleInputChange}
                    placeholder="Enter your Google AI API key"
                    className="input-field"
                  />
                  <p className="mt-1 text-sm text-gray-500">
                    Your API key is stored securely and never shared
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label htmlFor="model" className="block text-sm font-medium text-gray-700 mb-2">
                      AI Model
                    </label>
                    <select
                      id="model"
                      name="model"
                      value={formData.model}
                      onChange={handleInputChange}
                      className="input-field"
                    >
                      <option value="gemini-pro">Gemini Pro</option>
                      <option value="gemini-pro-vision">Gemini Pro Vision</option>
                    </select>
                  </div>
                  
                  <div>
                    <label htmlFor="maxTokens" className="block text-sm font-medium text-gray-700 mb-2">
                      Max Tokens
                    </label>
                    <input
                      type="number"
                      id="maxTokens"
                      name="maxTokens"
                      value={formData.maxTokens}
                      onChange={handleInputChange}
                      min="100"
                      max="8000"
                      className="input-field"
                    />
                  </div>
                  
                  <div>
                    <label htmlFor="temperature" className="block text-sm font-medium text-gray-700 mb-2">
                      Temperature
                    </label>
                    <input
                      type="range"
                      id="temperature"
                      name="temperature"
                      value={formData.temperature}
                      onChange={handleInputChange}
                      min="0"
                      max="1"
                      step="0.1"
                      className="w-full"
                    />
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                      <span>Conservative (0)</span>
                      <span>Creative (1)</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Database Settings */}
            {activeTab === 'database' && (
              <div className="space-y-4">
                <h2 className="text-xl font-semibold text-gray-900">Database Configuration</h2>
                
                <div>
                  <label htmlFor="databasePath" className="block text-sm font-medium text-gray-700 mb-2">
                    Database Path
                  </label>
                  <input
                    type="text"
                    id="databasePath"
                    name="databasePath"
                    value={formData.databasePath}
                    onChange={handleInputChange}
                    placeholder="./chroma_db"
                    className="input-field"
                  />
                </div>

                <div className="flex items-center space-x-4">
                  <button
                    onClick={testConnection}
                    className="btn-secondary flex items-center space-x-2"
                  >
                    <ServerIcon className="h-5 w-5" />
                    <span>Test Connection</span>
                  </button>
                  
                  {connectionStatus && (
                    <div className="flex items-center space-x-2">
                      {connectionStatus.connected ? (
                        <CheckCircleIcon className="h-5 w-5 text-green-500" />
                      ) : (
                        <ExclamationTriangleIcon className="h-5 w-5 text-red-500" />
                      )}
                      <span className={`text-sm ${
                        connectionStatus.connected ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {connectionStatus.message}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Security Settings */}
            {activeTab === 'security' && (
              <div className="space-y-4">
                <h2 className="text-xl font-semibold text-gray-900">Security Settings</h2>
                
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <div className="flex">
                    <ExclamationTriangleIcon className="h-5 w-5 text-yellow-400" />
                    <div className="ml-3">
                      <h3 className="text-sm font-medium text-yellow-800">
                        Security Notice
                      </h3>
                      <div className="mt-2 text-sm text-yellow-700">
                        <p>
                          Your API key and sensitive data are stored locally and encrypted.
                          Never share your API key or expose it in client-side code.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="space-y-2">
                  <h3 className="text-lg font-medium text-gray-900">Data Protection</h3>
                  <ul className="space-y-1 text-sm text-gray-600">
                    <li>• API keys are encrypted and stored securely</li>
                    <li>• All data is stored locally on your machine</li>
                    <li>• No data is transmitted to external servers</li>
                    <li>• Database files are protected with access controls</li>
                  </ul>
                </div>
              </div>
            )}

            {/* Save Button */}
            <div className="flex justify-end pt-6 border-t border-gray-200">
              <button
                onClick={handleSave}
                className="btn-primary"
              >
                Save Settings
              </button>
            </div>
          </div>
        )}
      </motion.div>

      {/* Error Display */}
      {error && (
        <motion.div 
          className="card border-red-200 bg-red-50 mt-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h2 className="text-lg font-semibold text-red-800 mb-2">Settings Error</h2>
          <p className="text-red-700">{error}</p>
        </motion.div>
      )}
    </div>
  );
};

export default Settings; 