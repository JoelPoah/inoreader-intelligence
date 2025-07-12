import React, { useState } from 'react';
import { Heart, Server, Zap, Coffee } from 'lucide-react';

const Donation: React.FC = () => {
  const [showDonation, setShowDonation] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleDonate = async () => {
    setIsProcessing(true);
    
    try {
      const response = await fetch('/api/create-checkout-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ amount: 5 }), // $5 donation
      });

      const { url } = await response.json();
      
      if (url) {
        window.location.href = url;
      }
    } catch (error) {
      console.error('Error:', error);
      setIsProcessing(false);
    }
  };

  return (
    <div className="py-20 bg-gray-900">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Support Strategic Intelligence
          </h2>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Help us maintain this free service by supporting our AI processing costs and server infrastructure.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className="bg-gray-800 rounded-xl p-6 text-center">
            <Server className="h-10 w-10 text-military-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-white mb-2">Server Costs</h3>
            <p className="text-gray-400 text-sm">
              Hosting and processing daily reports for our growing community
            </p>
          </div>
          
          <div className="bg-gray-800 rounded-xl p-6 text-center">
            <Zap className="h-10 w-10 text-military-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-white mb-2">AI Processing</h3>
            <p className="text-gray-400 text-sm">
              OpenAI GPT-4 costs for analyzing and summarizing articles
            </p>
          </div>
          
          <div className="bg-gray-800 rounded-xl p-6 text-center">
            <Heart className="h-10 w-10 text-military-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-white mb-2">Free Access</h3>
            <p className="text-gray-400 text-sm">
              Keeping the service completely free for all users
            </p>
          </div>
        </div>

        <div className="bg-gray-800 rounded-2xl p-8 text-center">
          {!showDonation ? (
            <div>
              <Coffee className="h-16 w-16 text-military-400 mx-auto mb-6" />
              <h3 className="text-2xl font-bold text-white mb-4">
                Enjoying the Intelligence Reports?
              </h3>
              <p className="text-gray-300 mb-6 max-w-2xl mx-auto">
                Your support helps us continue providing free, high-quality military intelligence analysis 
                to the DIS community. Every contribution helps cover our AI and infrastructure costs.
              </p>
              
              <div className="space-y-4">
                <button
                  onClick={() => setShowDonation(true)}
                  className="bg-military-600 hover:bg-military-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200 mr-4"
                >
                  ❤️ Support the Service
                </button>
                
                <button
                  onClick={() => setShowDonation(false)}
                  className="bg-gray-700 hover:bg-gray-600 text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200"
                >
                  Continue with Free Reports
                </button>
              </div>
            </div>
          ) : (
            <div>
              <h3 className="text-2xl font-bold text-white mb-4">
                Support Strategic Intelligence
              </h3>
              <p className="text-gray-300 mb-6">
                A $5 contribution helps us process hundreds of articles and maintain the service for everyone.
              </p>
              
              <div className="bg-gray-700 rounded-xl p-6 mb-6 max-w-md mx-auto">
                <div className="text-3xl font-bold text-white mb-2">$5</div>
                <div className="text-gray-300 text-sm">One-time contribution</div>
                <div className="text-gray-400 text-xs mt-2">
                  Covers ~200 AI summaries + server costs
                </div>
              </div>
              
              <div className="space-y-4">
                <button
                  onClick={handleDonate}
                  disabled={isProcessing}
                  className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200 disabled:opacity-50 mr-4"
                >
                  {isProcessing ? 'Processing...' : '💳 Donate $5'}
                </button>
                
                <button
                  onClick={() => setShowDonation(false)}
                  className="bg-gray-700 hover:bg-gray-600 text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200"
                >
                  Maybe Later
                </button>
              </div>
              
              <p className="text-gray-400 text-xs mt-4">
                Secure payment processed by Stripe • No recurring charges
              </p>
            </div>
          )}
        </div>
        
        <div className="mt-8 text-center">
          <p className="text-gray-500 text-sm">
            This service is completely optional. All intelligence reports remain free regardless of contribution.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Donation;