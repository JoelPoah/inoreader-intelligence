import React, { useState } from 'react';
import { Mail, Clock, CheckCircle, AlertCircle } from 'lucide-react';

const EmailSignup: React.FC = () => {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('loading');

    try {
      const response = await fetch('/api/subscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      if (response.ok) {
        setStatus('success');
        setMessage('Successfully subscribed! You\'ll receive your first report tomorrow at 06:00 SGT.');
        setEmail('');
      } else {
        const errorData = await response.json();
        setStatus('error');
        setMessage(errorData.message || 'Failed to subscribe. Please try again.');
      }
    } catch (error) {
      setStatus('error');
      setMessage('Network error. Please check your connection and try again.');
    }
  };

  return (
    <div className="py-20 bg-gradient-to-br from-military-50 to-blue-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-2xl shadow-xl p-8 md:p-12">
          <div className="text-center mb-8">
            <div className="flex items-center justify-center mb-4">
              <Mail className="h-12 w-12 text-military-600 mr-3" />
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900">
                Get Daily Intelligence Reports
              </h2>
            </div>
            
            <p className="text-xl text-gray-600 mb-6">
              Join our community of military analysts and DIS scholarship candidates. 
              Receive comprehensive intelligence briefings every morning.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="flex flex-col items-center p-4 bg-gray-50 rounded-lg">
                <Clock className="h-8 w-8 text-military-600 mb-2" />
                <span className="font-semibold text-gray-900">06:00 SGT</span>
                <span className="text-sm text-gray-600">Daily Delivery</span>
              </div>
              
              <div className="flex flex-col items-center p-4 bg-gray-50 rounded-lg">
                <Mail className="h-8 w-8 text-military-600 mb-2" />
                <span className="font-semibold text-gray-900">HTML + PDF</span>
                <span className="text-sm text-gray-600">Dual Format</span>
              </div>
              
              <div className="flex flex-col items-center p-4 bg-gray-50 rounded-lg">
                <CheckCircle className="h-8 w-8 text-military-600 mb-2" />
                <span className="font-semibold text-gray-900">Free Service</span>
                <span className="text-sm text-gray-600">No Cost</span>
              </div>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="max-w-md mx-auto">
            <div className="flex flex-col sm:flex-row gap-4">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email address"
                required
                disabled={status === 'loading'}
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-military-500 focus:border-transparent outline-none disabled:opacity-50"
              />
              
              <button
                type="submit"
                disabled={status === 'loading' || !email}
                className="btn-primary min-w-[120px] disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {status === 'loading' ? 'Subscribing...' : 'Subscribe'}
              </button>
            </div>
            
            {status === 'success' && (
              <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center">
                <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
                <span className="text-green-800">{message}</span>
              </div>
            )}
            
            {status === 'error' && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center">
                <AlertCircle className="h-5 w-5 text-red-600 mr-2" />
                <span className="text-red-800">{message}</span>
              </div>
            )}
          </form>

          <div className="mt-8 text-center">
            <p className="text-sm text-gray-500">
              We respect your privacy. Unsubscribe at any time. 
              <br />
              Reports include links to Inoreader for full article access.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmailSignup;