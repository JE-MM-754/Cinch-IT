export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            AI Sales Engine
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Transform your sales process with intelligent lead reactivation and automated prospecting
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white p-8 rounded-lg shadow-lg">
            <div className="w-12 h-12 bg-blue-500 rounded-lg mb-4 flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">Dead Lead Reactivation</h3>
            <p className="text-gray-600">
              Automatically re-engage cold prospects with personalized AI-generated outreach
            </p>
          </div>

          <div className="bg-white p-8 rounded-lg shadow-lg">
            <div className="w-12 h-12 bg-green-500 rounded-lg mb-4 flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">Smart Analytics</h3>
            <p className="text-gray-600">
              Track engagement, conversion rates, and ROI with detailed campaign analytics
            </p>
          </div>

          <div className="bg-white p-8 rounded-lg shadow-lg">
            <div className="w-12 h-12 bg-purple-500 rounded-lg mb-4 flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">Automated Workflows</h3>
            <p className="text-gray-600">
              Set up complex multi-touch campaigns that run on autopilot
            </p>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center bg-white p-12 rounded-lg shadow-lg">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Ready to 10x Your Sales Pipeline?
          </h2>
          <p className="text-gray-600 mb-8 max-w-xl mx-auto">
            Schedule a demo to see how our AI sales engine can transform your outbound efforts
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors">
              Schedule Demo
            </button>
            <button className="border border-gray-300 text-gray-700 px-8 py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors">
              View Case Studies
            </button>
          </div>
        </div>

        {/* Demo Stats */}
        <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div>
            <div className="text-3xl font-bold text-blue-600 mb-2">250%</div>
            <div className="text-gray-600">Response Rate Increase</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-green-600 mb-2">80%</div>
            <div className="text-gray-600">Time Saved</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-purple-600 mb-2">15x</div>
            <div className="text-gray-600">ROI Improvement</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-orange-600 mb-2">500+</div>
            <div className="text-gray-600">Happy Customers</div>
          </div>
        </div>
      </div>
    </div>
  );
}