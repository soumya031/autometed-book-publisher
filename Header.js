import React from 'react';
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';
import { BookOpenIcon, CheckCircleIcon, ExclamationTriangleIcon } from '@heroicons/react/24/solid';

const Header = ({ sidebarOpen, setSidebarOpen, systemStatus }) => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200 lg:pl-64">
      <div className="flex items-center justify-between px-4 sm:px-6 lg:px-8 h-16">
        {/* Mobile menu button */}
        <button
          type="button"
          className="lg:hidden -m-2.5 p-2.5 text-gray-700"
          onClick={() => setSidebarOpen(true)}
        >
          <span className="sr-only">Open sidebar</span>
          <Bars3Icon className="h-6 w-6" aria-hidden="true" />
        </button>

        {/* Logo and title */}
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2">
            <BookOpenIcon className="h-8 w-8 text-blue-600" />
            <div>
              <h1 className="text-xl font-bold text-gray-900">AI Book Publication</h1>
              <p className="text-sm text-gray-500">Workflow Automation</p>
            </div>
          </div>
        </div>

        {/* System status */}
        <div className="flex items-center space-x-4">
          {systemStatus && (
            <div className="hidden sm:flex items-center space-x-2">
              <span className="text-sm text-gray-500">System Status:</span>
              <div className="flex items-center space-x-1">
                {systemStatus.database ? (
                  <CheckCircleIcon className="h-4 w-4 text-green-500" />
                ) : (
                  <ExclamationTriangleIcon className="h-4 w-4 text-red-500" />
                )}
                <span className={`text-sm ${systemStatus.database ? 'text-green-600' : 'text-red-600'}`}>
                  Database
                </span>
              </div>
              <div className="flex items-center space-x-1">
                {systemStatus.ai ? (
                  <CheckCircleIcon className="h-4 w-4 text-green-500" />
                ) : (
                  <ExclamationTriangleIcon className="h-4 w-4 text-yellow-500" />
                )}
                <span className={`text-sm ${systemStatus.ai ? 'text-green-600' : 'text-yellow-600'}`}>
                  AI
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header; 