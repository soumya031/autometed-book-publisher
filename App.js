import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Workflow from './pages/Workflow';
import Search from './pages/Search';
import History from './pages/History';
import Settings from './pages/Settings';
import { useSystemStatus } from './hooks/useSystemStatus';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { status, loading } = useSystemStatus();

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <Header 
          sidebarOpen={sidebarOpen} 
          setSidebarOpen={setSidebarOpen}
          systemStatus={status}
        />

        {/* Sidebar */}
        <Sidebar 
          open={sidebarOpen} 
          setOpen={setSidebarOpen}
          systemStatus={status}
        />

        {/* Main Content */}
        <main className="lg:pl-64">
          <div className="px-4 sm:px-6 lg:px-8 py-8">
            <AnimatePresence mode="wait">
              <Routes>
                <Route 
                  path="/" 
                  element={
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ duration: 0.3 }}
                    >
                      <Workflow />
                    </motion.div>
                  } 
                />
                <Route 
                  path="/search" 
                  element={
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ duration: 0.3 }}
                    >
                      <Search />
                    </motion.div>
                  } 
                />
                <Route 
                  path="/history" 
                  element={
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ duration: 0.3 }}
                    >
                      <History />
                    </motion.div>
                  } 
                />
                <Route 
                  path="/settings" 
                  element={
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ duration: 0.3 }}
                    >
                      <Settings />
                    </motion.div>
                  } 
                />
              </Routes>
            </AnimatePresence>
          </div>
        </main>

        {/* Loading Overlay */}
        {loading && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 flex items-center space-x-3">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
              <span className="text-gray-700">Loading system status...</span>
            </div>
          </div>
        )}
      </div>
    </Router>
  );
}

export default App; 