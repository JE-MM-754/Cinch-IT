'use client';

import React, { useState, useEffect } from 'react';
import {
  Target,
  TrendingUp,
  Users,
  BarChart3,
  Search,
  Plus,
  Filter,
  Download,
  PlayCircle,
  AlertTriangle,
  CheckCircle,
  Clock,
  Eye,
  ArrowUpRight,
  Zap
} from 'lucide-react';

interface DashboardMetrics {
  totalProspectsAnalyzed: number;
  leadsReactivated: number;
  competitorsTracked: number;
  successRate: number;
  avgResponseTime: string;
}

interface ProspectIntel {
  id: string;
  companyName: string;
  contactName: string;
  intelligenceSummary: string;
  youtubePresence: boolean;
  performanceScore: number;
  status: 'new' | 'analyzed' | 'contacted';
  lastUpdated: string;
}

interface CompetitorAlert {
  id: string;
  competitor: string;
  alertType: string;
  message: string;
  urgency: 'low' | 'medium' | 'high' | 'critical';
  date: string;
}

const Dashboard = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics>({
    totalProspectsAnalyzed: 0,
    leadsReactivated: 0,
    competitorsTracked: 0,
    successRate: 0,
    avgResponseTime: '0s'
  });

  const [prospects, setProspects] = useState<ProspectIntel[]>([]);
  const [alerts, setAlerts] = useState<CompetitorAlert[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [newProspectName, setNewProspectName] = useState('');
  const [showAnalysisModal, setShowAnalysisModal] = useState(false);

  // Mock data loading
  useEffect(() => {
    const loadDashboardData = async () => {
      setIsLoading(true);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setMetrics({
        totalProspectsAnalyzed: 247,
        leadsReactivated: 84,
        competitorsTracked: 15,
        successRate: 87.5,
        avgResponseTime: '1.2s'
      });

      setProspects([
        {
          id: '1',
          companyName: 'TechCorp Solutions',
          contactName: 'Sarah Johnson',
          intelligenceSummary: 'Active YouTube presence with 15K subscribers focusing on product demos and thought leadership. Strong digital marketing maturity.',
          youtubePresence: true,
          performanceScore: 78,
          status: 'new',
          lastUpdated: '2 hours ago'
        },
        {
          id: '2',
          companyName: 'InnovateLabs',
          contactName: 'Mike Chen',
          intelligenceSummary: 'No significant YouTube presence detected. Moderate competitive landscape with growth opportunities.',
          youtubePresence: false,
          performanceScore: 45,
          status: 'analyzed',
          lastUpdated: '1 day ago'
        },
        {
          id: '3',
          companyName: 'DataDriven Inc',
          contactName: 'Alex Rodriguez',
          intelligenceSummary: 'High content production with educational focus. Target audience: developers and technical decision makers.',
          youtubePresence: true,
          performanceScore: 92,
          status: 'contacted',
          lastUpdated: '3 hours ago'
        }
      ]);

      setAlerts([
        {
          id: '1',
          competitor: 'CompetitorX',
          alertType: 'funding_announcement',
          message: 'Secured $25M Series B funding',
          urgency: 'high',
          date: '2 hours ago'
        },
        {
          id: '2',
          competitor: 'RivalCorp',
          alertType: 'product_release',
          message: 'Launched new AI features',
          urgency: 'medium',
          date: '1 day ago'
        },
        {
          id: '3',
          competitor: 'MarketLeader',
          alertType: 'executive_hire',
          message: 'New VP of Sales appointed',
          urgency: 'medium',
          date: '3 days ago'
        }
      ]);

      setIsLoading(false);
    };

    loadDashboardData();
  }, []);

  const analyzeNewProspect = async () => {
    if (!newProspectName.trim()) return;

    setShowAnalysisModal(true);
    
    // Simulate prospect analysis
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const newProspect: ProspectIntel = {
      id: Date.now().toString(),
      companyName: newProspectName,
      contactName: 'Auto-detected Contact',
      intelligenceSummary: 'Analysis complete. YouTube presence detected with moderate engagement metrics.',
      youtubePresence: Math.random() > 0.5,
      performanceScore: Math.floor(Math.random() * 40) + 50,
      status: 'new',
      lastUpdated: 'Just now'
    };

    setProspects(prev => [newProspect, ...prev]);
    setMetrics(prev => ({ ...prev, totalProspectsAnalyzed: prev.totalProspectsAnalyzed + 1 }));
    setNewProspectName('');
    setShowAnalysisModal(false);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'new': return 'bg-blue-500/10 text-blue-400 border-blue-500/20';
      case 'analyzed': return 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20';
      case 'contacted': return 'bg-green-500/10 text-green-400 border-green-500/20';
      default: return 'bg-gray-500/10 text-gray-400 border-gray-500/20';
    }
  };

  const getUrgencyColor = (urgency: string) => {
    switch (urgency) {
      case 'critical': return 'bg-red-500 text-white';
      case 'high': return 'bg-orange-500 text-white';
      case 'medium': return 'bg-yellow-500 text-black';
      case 'low': return 'bg-gray-500 text-white';
      default: return 'bg-gray-500 text-white';
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-white text-lg">Loading Sales Intelligence Dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Header */}
      <header className="bg-black/20 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center">
                <Target className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">CinchIT AI Sales Engine</h1>
                <p className="text-gray-400">Sales Intelligence Dashboard</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
                <Download className="w-4 h-4" />
                <span>Export Data</span>
              </button>
              <div className="w-8 h-8 bg-gray-600 rounded-full"></div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
          <div className="bg-black/20 backdrop-blur-md border border-white/10 rounded-xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Prospects Analyzed</p>
                <p className="text-2xl font-bold text-white">{metrics.totalProspectsAnalyzed}</p>
              </div>
              <Target className="w-8 h-8 text-blue-400" />
            </div>
          </div>

          <div className="bg-black/20 backdrop-blur-md border border-white/10 rounded-xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Leads Reactivated</p>
                <p className="text-2xl font-bold text-white">{metrics.leadsReactivated}</p>
              </div>
              <TrendingUp className="w-8 h-8 text-green-400" />
            </div>
          </div>

          <div className="bg-black/20 backdrop-blur-md border border-white/10 rounded-xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Competitors Tracked</p>
                <p className="text-2xl font-bold text-white">{metrics.competitorsTracked}</p>
              </div>
              <BarChart3 className="w-8 h-8 text-purple-400" />
            </div>
          </div>

          <div className="bg-black/20 backdrop-blur-md border border-white/10 rounded-xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Success Rate</p>
                <p className="text-2xl font-bold text-white">{metrics.successRate}%</p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-400" />
            </div>
          </div>

          <div className="bg-black/20 backdrop-blur-md border border-white/10 rounded-xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Avg Response Time</p>
                <p className="text-2xl font-bold text-white">{metrics.avgResponseTime}</p>
              </div>
              <Clock className="w-8 h-8 text-blue-400" />
            </div>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Prospect Analysis */}
          <div className="lg:col-span-2">
            <div className="bg-black/20 backdrop-blur-md border border-white/10 rounded-xl overflow-hidden">
              <div className="px-6 py-4 border-b border-white/10 flex justify-between items-center">
                <h2 className="text-xl font-semibold text-white">Prospect Intelligence</h2>
                <div className="flex items-center space-x-3">
                  <div className="relative">
                    <input
                      type="text"
                      placeholder="Add new prospect..."
                      value={newProspectName}
                      onChange={(e) => setNewProspectName(e.target.value)}
                      className="bg-gray-800/50 border border-gray-600 rounded-lg px-4 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
                      onKeyPress={(e) => e.key === 'Enter' && analyzeNewProspect()}
                    />
                    <Search className="absolute right-3 top-2.5 w-4 h-4 text-gray-400" />
                  </div>
                  <button 
                    onClick={analyzeNewProspect}
                    disabled={!newProspectName.trim()}
                    className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-4 py-2 rounded-lg transition-colors flex items-center space-x-2"
                  >
                    <Plus className="w-4 h-4" />
                    <span>Analyze</span>
                  </button>
                </div>
              </div>

              <div className="p-6">
                <div className="space-y-4">
                  {prospects.map((prospect) => (
                    <div key={prospect.id} className="bg-gray-800/30 border border-gray-700 rounded-lg p-4 hover:bg-gray-800/50 transition-colors">
                      <div className="flex justify-between items-start mb-3">
                        <div>
                          <h3 className="text-lg font-semibold text-white">{prospect.companyName}</h3>
                          <p className="text-gray-400">{prospect.contactName}</p>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className={`px-2 py-1 rounded-full border text-xs ${getStatusColor(prospect.status)}`}>
                            {prospect.status}
                          </span>
                          <div className="flex items-center space-x-1">
                            {prospect.youtubePresence ? (
                              <PlayCircle className="w-4 h-4 text-red-400" />
                            ) : (
                              <div className="w-4 h-4"></div>
                            )}
                            <span className="text-sm text-gray-400">{prospect.performanceScore}/100</span>
                          </div>
                        </div>
                      </div>
                      
                      <p className="text-gray-300 text-sm mb-3 line-clamp-2">{prospect.intelligenceSummary}</p>
                      
                      <div className="flex justify-between items-center">
                        <span className="text-xs text-gray-500">Updated {prospect.lastUpdated}</span>
                        <div className="flex space-x-2">
                          <button className="text-blue-400 hover:text-blue-300 transition-colors">
                            <Eye className="w-4 h-4" />
                          </button>
                          <button className="text-green-400 hover:text-green-300 transition-colors">
                            <ArrowUpRight className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Competitor Alerts */}
          <div className="space-y-6">
            <div className="bg-black/20 backdrop-blur-md border border-white/10 rounded-xl">
              <div className="px-6 py-4 border-b border-white/10">
                <h2 className="text-xl font-semibold text-white">Competitor Alerts</h2>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {alerts.map((alert) => (
                    <div key={alert.id} className="border-l-4 border-blue-500 bg-gray-800/30 p-4 rounded-r-lg">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-semibold text-white">{alert.competitor}</h4>
                        <span className={`px-2 py-1 rounded text-xs ${getUrgencyColor(alert.urgency)}`}>
                          {alert.urgency}
                        </span>
                      </div>
                      <p className="text-gray-300 text-sm mb-2">{alert.message}</p>
                      <p className="text-gray-500 text-xs">{alert.date}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-black/20 backdrop-blur-md border border-white/10 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <button className="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-3 rounded-lg transition-colors flex items-center justify-center space-x-2">
                  <Zap className="w-4 h-4" />
                  <span>Run Intelligence Update</span>
                </button>
                
                <button className="w-full bg-gray-700 hover:bg-gray-600 text-white px-4 py-3 rounded-lg transition-colors flex items-center justify-center space-x-2">
                  <Users className="w-4 h-4" />
                  <span>Analyze Dead Leads</span>
                </button>
                
                <button className="w-full bg-gray-700 hover:bg-gray-600 text-white px-4 py-3 rounded-lg transition-colors flex items-center justify-center space-x-2">
                  <BarChart3 className="w-4 h-4" />
                  <span>Export Reports</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Analysis Modal */}
      {showAnalysisModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-gray-800 border border-gray-700 rounded-xl p-8 max-w-md w-full mx-4">
            <div className="text-center">
              <div className="animate-spin w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
              <h3 className="text-xl font-semibold text-white mb-2">Analyzing Prospect</h3>
              <p className="text-gray-400">Gathering YouTube intelligence, competitive data, and market signals...</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;