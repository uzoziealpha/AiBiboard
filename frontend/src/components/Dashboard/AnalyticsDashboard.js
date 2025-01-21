// frontend/src/components/Dashboard/AnalyticsDashboard.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AnalyticsDashboard = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(
          'http://localhost:8000/api/dashboard/analytics',
          {
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          }
        );
        setAnalytics(response.data);
      } catch (err) {
        setError(err.response?.data?.detail || 'Error fetching analytics');
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-gray-500">Loading analytics...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 p-4 rounded-md">
        <div className="text-red-700">{error}</div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="bg-white shadow sm:rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Analytics Dashboard
          </h3>
          {analytics ? (
            <div className="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {/* Display analytics data here */}
              <pre className="bg-gray-50 p-4 rounded-md overflow-auto">
                {JSON.stringify(analytics, null, 2)}
              </pre>
            </div>
          ) : (
            <div className="mt-5 text-gray-500">
              No analytics data available. Please upload some data first.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;