// frontend/src/components/Layout/LandingPage.js
import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-6">
          <div className="flex items-center">
            <h1 className="text-2xl font-bold text-gray-900">AI Business Dashboard</h1>
          </div>
          <div className="flex items-center space-x-4">
            <Link
              to="/signin"
              className="text-base font-medium text-gray-500 hover:text-gray-900"
            >
              Sign In
            </Link>
            <Link
              to="/signup"
              className="inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
            >
              Sign Up
            </Link>
          </div>
        </div>
        
        <div className="mt-16 text-center">
          <h2 className="text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight lg:text-6xl">
            Transform Your Business Data
          </h2>
          <p className="mt-5 max-w-xl mx-auto text-xl text-gray-500">
            Upload your business data and get AI-powered insights instantly
          </p>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;