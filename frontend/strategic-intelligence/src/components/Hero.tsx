import React from 'react';
import { Shield, Clock, Mail, Users } from 'lucide-react';

const Hero: React.FC = () => {
  return (
    <div className="bg-gradient-to-br from-military-900 via-military-800 to-blue-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <div className="flex items-center justify-center mb-6">
            <Shield className="h-16 w-16 text-military-300 mr-4" />
            <h1 className="text-5xl md:text-7xl font-bold">
              Strategic
              <span className="block gradient-text">Intelligence</span>
              <span className="block text-4xl md:text-6xl">Reports</span>
            </h1>
          </div>
          
          <p className="text-xl md:text-2xl text-military-100 mb-8 max-w-4xl mx-auto leading-relaxed">
            Get daily AI-powered military intelligence briefings from trusted sources. 
            Curated for <strong>DIS scholarship preparation</strong> and strategic analysis.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mt-12 mb-12">
            <div className="flex flex-col items-center p-4">
              <Clock className="h-8 w-8 text-military-300 mb-2" />
              <span className="text-lg font-semibold">06:00 SGT</span>
              <span className="text-military-200 text-sm">Daily Delivery</span>
            </div>
            
            <div className="flex flex-col items-center p-4">
              <Shield className="h-8 w-8 text-military-300 mb-2" />
              <span className="text-lg font-semibold">7 Themes</span>
              <span className="text-military-200 text-sm">Intelligence Focus</span>
            </div>
            
            <div className="flex flex-col items-center p-4">
              <Users className="h-8 w-8 text-military-300 mb-2" />
              <span className="text-lg font-semibold">AI Analysis</span>
              <span className="text-military-200 text-sm">GPT-4 Powered</span>
            </div>
            
            <div className="flex flex-col items-center p-4">
              <Mail className="h-8 w-8 text-military-300 mb-2" />
              <span className="text-lg font-semibold">PDF + HTML</span>
              <span className="text-military-200 text-sm">Full Content</span>
            </div>
          </div>
          
          <div className="bg-military-800/50 backdrop-blur-sm rounded-xl p-6 max-w-3xl mx-auto">
            <h3 className="text-2xl font-bold mb-4">Trusted Sources</h3>
            <div className="flex flex-wrap justify-center items-center gap-6 text-military-200">
              <span className="text-lg font-medium">Channel NewsAsia</span>
              <span className="text-military-400">•</span>
              <span className="text-lg font-medium">The Straits Times</span>
              <span className="text-military-400">•</span>
              <span className="text-lg font-medium">BBC News</span>
              <span className="text-military-400">•</span>
              <span className="text-lg font-medium">Al Jazeera</span>
              <span className="text-military-400">•</span>
              <span className="text-lg font-medium">RSS Feeds</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;