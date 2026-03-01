// Prospecting Dashboard Component - BUILD THIS FIRST
// Shows AI-generated prospects, lead pipeline, and performance metrics

'use client';

import { useState, useEffect } from 'react';
import { dashboard, prospects } from '../api/client';
import type { ProspectingDashboard, Prospect } from '../types/prospect';

export default function ProspectingDashboard() {
  const [stats, setStats] = useState<ProspectingDashboard | null>(null);
  const [recentProspects, setRecentProspects] = useState<Prospect[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [dashboardData, prospectsData] = await Promise.all([
        dashboard.getSummary(),
        prospects.list({ per_page: 10, sort_by: 'created_at', order: 'desc' })
      ]);
      setStats(dashboardData);
      setRecentProspects(prospectsData.prospects);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load dashboard');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-8">Loading prospecting dashboard...</div>;
  }

  if (error) {
    return <div className="p-8 text-red-600">Error: {error}</div>;
  }

  if (!stats) {
    return <div className="p-8">No data available</div>;
  }

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">
          Cinch IT AI Prospecting Engine
        </h1>
        <div className="flex space-x-4">
          <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
            Run AI Discovery
          </button>
          <button className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700">
            Create Campaign
          </button>
        </div>
      </div>

      {/* Key Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">
        {/* Total Prospects */}
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <svg className="h-8 w-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Total Prospects</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.summary.total_prospects}</p>
            </div>
          </div>
        </div>

        {/* Qualified Leads */}
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <svg className="h-8 w-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Qualified Leads</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.summary.qualified_leads}</p>
            </div>
          </div>
        </div>

        {/* Active Campaigns */}
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <svg className="h-8 w-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Active Campaigns</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.summary.active_campaigns}</p>
            </div>
          </div>
        </div>

        {/* Meetings This Month */}
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <svg className="h-8 w-8 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Meetings This Month</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.summary.meetings_this_month}</p>
            </div>
          </div>
        </div>

        {/* Pipeline Value */}
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <svg className="h-8 w-8 text-green-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Pipeline Value</p>
              <p className="text-2xl font-semibold text-gray-900">${stats.summary.pipeline_value.toLocaleString()}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Lead Funnel Visualization */}
      <div className="bg-white p-6 rounded-lg shadow mb-8">
        <h2 className="text-xl font-semibold mb-4">Lead Funnel</h2>
        <div className="flex justify-between items-center">
          {Object.entries(stats.lead_funnel).map(([stage, count], index) => (
            <div key={stage} className="text-center flex-1">
              <div className="relative">
                <div className="w-16 h-16 mx-auto bg-blue-100 rounded-full flex items-center justify-center">
                  <span className="text-xl font-bold text-blue-600">{count}</span>
                </div>
                <p className="mt-2 text-sm font-medium capitalize">{stage.replace('_', ' ')}</p>
              </div>
              {index < Object.keys(stats.lead_funnel).length - 1 && (
                <div className="hidden md:block absolute top-8 left-1/2 w-full h-0.5 bg-gray-300"></div>
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Prospects */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Recent AI Discoveries</h2>
          <div className="space-y-4">
            {recentProspects.length > 0 ? (
              recentProspects.map((prospect) => (
                <div key={prospect.company.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <h3 className="font-semibold">{prospect.company.name}</h3>
                    <p className="text-sm text-gray-600">{prospect.company.industry} • {prospect.company.employee_count} employees</p>
                    <p className="text-sm text-gray-500">{prospect.primary_contact.first_name} {prospect.primary_contact.last_name}</p>
                  </div>
                  <div className="text-right">
                    <div className={`px-2 py-1 rounded text-sm font-medium ${
                      prospect.lead_score.qualification_status === 'hot' 
                        ? 'bg-red-100 text-red-800'
                        : prospect.lead_score.qualification_status === 'warm'
                        ? 'bg-orange-100 text-orange-800' 
                        : 'bg-blue-100 text-blue-800'
                    }`}>
                      {prospect.lead_score.qualification_status.toUpperCase()}
                    </div>
                    <p className="text-sm text-gray-500 mt-1">Score: {prospect.lead_score.overall_score}</p>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-gray-500 text-center py-8">No prospects discovered yet. Run AI discovery to find potential clients.</p>
            )}
          </div>
          <div className="mt-6">
            <button className="w-full bg-gray-100 text-gray-700 py-2 rounded-lg hover:bg-gray-200">
              View All Prospects
            </button>
          </div>
        </div>

        {/* Performance Metrics */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">AI Performance</h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-sm font-medium text-gray-600">Discovery Rate</span>
              <span className="text-sm font-semibold">{stats.performance.prospect_discovery_rate}/week</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-blue-600 h-2 rounded-full" 
                style={{ width: `${Math.min(stats.performance.prospect_discovery_rate / 50 * 100, 100)}%` }}
              ></div>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-sm font-medium text-gray-600">Qualification Accuracy</span>
              <span className="text-sm font-semibold">{stats.performance.qualification_accuracy}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-green-600 h-2 rounded-full" 
                style={{ width: `${stats.performance.qualification_accuracy}%` }}
              ></div>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-sm font-medium text-gray-600">Response Rate</span>
              <span className="text-sm font-semibold">{stats.performance.outreach_response_rate}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-purple-600 h-2 rounded-full" 
                style={{ width: `${stats.performance.outreach_response_rate}%` }}
              ></div>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-sm font-medium text-gray-600">Meeting Rate</span>
              <span className="text-sm font-semibold">{stats.performance.meeting_booking_rate}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-orange-600 h-2 rounded-full" 
                style={{ width: `${stats.performance.meeting_booking_rate}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}