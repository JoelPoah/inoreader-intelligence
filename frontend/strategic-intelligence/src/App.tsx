import React from 'react';
import Hero from './components/Hero';
import Features from './components/Features';
import Themes from './components/Themes';
import EmailSignup from './components/EmailSignup';
import Donation from './components/Donation';
import './App.css';

function App() {
  return (
    <div className="App">
      <Hero />
      <Features />
      <Themes />
      <EmailSignup />
      <Donation />
      
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h3 className="text-2xl font-bold mb-4">Strategic Intelligence Reports</h3>
            <p className="text-gray-400 mb-6 max-w-2xl mx-auto">
              AI-powered military intelligence briefings for DIS scholarship preparation. 
              Daily reports at 06:00 Singapore Time from trusted sources.
            </p>
            
            <div className="flex flex-wrap justify-center items-center gap-4 text-gray-400 text-sm">
              <span>Sources:</span>
              <span>Channel NewsAsia</span>
              <span>•</span>
              <span>The Straits Times</span>
              <span>•</span>
              <span>BBC News</span>
              <span>•</span>
              <span>Al Jazeera</span>
              <span>•</span>
              <span>RSS Feeds</span>
            </div>
            
            <div className="mt-8 pt-8 border-t border-gray-700 text-gray-500 text-sm">
              <p>&copy; 2024 Strategic Intelligence Reports. Built for the DIS community.</p>
              <p className="mt-2">Powered by OpenAI GPT-4 and Inoreader API</p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;