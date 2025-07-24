import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { XMarkIcon } from '@heroicons/react/24/outline';
import { 
  PlayIcon, 
  MagnifyingGlassIcon, 
  ClockIcon, 
  Cog6ToothIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/solid';

const navigation = [
  { name: 'Workflow', href: '/', icon: PlayIcon },
  { name: 'Search', href: '/search', icon: MagnifyingGlassIcon },
  { name: 'History', href: '/history', icon: ClockIcon },
  { name: 'Settings', href: '/settings', icon: Cog6ToothIcon },
];

const Sidebar = ({ open, setOpen, systemStatus }) => {
  const location = useLocation();

  return (
    <>
      {/* Mobile sidebar */}
      <div className={`fixed inset-0 flex z-40 lg:hidden ${open ? '' : 'hidden'}`}>
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setOpen(false)} />
        <div className="relative flex-1 flex flex-col max-w-xs w-full bg-white">
          <div className="absolute top-0 right-0 -mr-12 pt-2">
            <button
              type="button"
              className="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
              onClick={() => setOpen(false)}
            >
              <span className="sr-only">Close sidebar</span>
              <XMarkIcon className="h-6 w-6 text-white" aria-hidden="true" />
            </button>
          </div>
          <div className="flex-1 h-0 pt-5 pb-4 overflow-y-auto">
            <div className="flex-shrink-0 flex items-center px-4">
              <h2 className="text-lg font-semibold text-gray-900">AI Book Publication</h2>
            </div>
            <nav className="mt-5 px-2 space-y-1">
              {navigation.map((item) => {
                const isActive = location.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`group flex items-center px-2 py-2 text-base font-medium rounded-md transition-colors ${
                      isActive
                        ? 'bg-blue-100 text-blue-900'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                    onClick={() => setOpen(false)}
                  >
                    <item.icon
                      className={`mr-4 flex-shrink-0 h-6 w-6 ${
                        isActive ? 'text-blue-500' : 'text-gray-400 group-hover:text-gray-500'
                      }`}
                      aria-hidden="true"
                    />
                    {item.name}
                  </Link>
                );
              })}
            </nav>
          </div>
          
          {/* System Status */}
          {systemStatus && (
            <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
              <div className="w-full">
                <h3 className="text-sm font-medium text-gray-500 mb-2">System Status</h3>
                <div className="space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Database</span>
                    <div className="flex items-center">
                      {systemStatus.database ? (
                        <CheckCircleIcon className="h-4 w-4 text-green-500" />
                      ) : (
                        <ExclamationTriangleIcon className="h-4 w-4 text-red-500" />
                      )}
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">AI Service</span>
                    <div className="flex items-center">
                      {systemStatus.ai ? (
                        <CheckCircleIcon className="h-4 w-4 text-green-500" />
                      ) : (
                        <ExclamationTriangleIcon className="h-4 w-4 text-yellow-500" />
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Desktop sidebar */}
      <div className="hidden lg:flex lg:w-64 lg:flex-col lg:fixed lg:inset-y-0">
        <div className="flex-1 flex flex-col min-h-0 bg-white border-r border-gray-200">
          <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
            <div className="flex items-center flex-shrink-0 px-4">
              <h2 className="text-lg font-semibold text-gray-900">AI Book Publication</h2>
            </div>
            <nav className="mt-5 flex-1 px-2 space-y-1">
              {navigation.map((item) => {
                const isActive = location.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors ${
                      isActive
                        ? 'bg-blue-100 text-blue-900'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                  >
                    <item.icon
                      className={`mr-3 flex-shrink-0 h-6 w-6 ${
                        isActive ? 'text-blue-500' : 'text-gray-400 group-hover:text-gray-500'
                      }`}
                      aria-hidden="true"
                    />
                    {item.name}
                  </Link>
                );
              })}
            </nav>
          </div>
          
          {/* System Status */}
          {systemStatus && (
            <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
              <div className="w-full">
                <h3 className="text-sm font-medium text-gray-500 mb-2">System Status</h3>
                <div className="space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Database</span>
                    <div className="flex items-center">
                      {systemStatus.database ? (
                        <CheckCircleIcon className="h-4 w-4 text-green-500" />
                      ) : (
                        <ExclamationTriangleIcon className="h-4 w-4 text-red-500" />
                      )}
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">AI Service</span>
                    <div className="flex items-center">
                      {systemStatus.ai ? (
                        <CheckCircleIcon className="h-4 w-4 text-green-500" />
                      ) : (
                        <ExclamationTriangleIcon className="h-4 w-4 text-yellow-500" />
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default Sidebar; 