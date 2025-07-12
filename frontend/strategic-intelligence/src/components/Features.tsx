import React from 'react';
import { Target, Brain, Filter, Globe, FileText, Clock, Users, Shield } from 'lucide-react';

const Features: React.FC = () => {
  const features = [
    {
      icon: Target,
      title: "Focus Folder Optimization",
      description: "Efficiently processes only your curated Focus folder feeds - 40x faster than processing all feeds.",
      highlight: "~100 articles vs ~4,100"
    },
    {
      icon: Brain,
      title: "AI-Powered Analysis",
      description: "Uses OpenAI GPT-4 for strategic intelligence summaries, categorization, and trend analysis.",
      highlight: "GPT-4 Strategic Analysis"
    },
    {
      icon: Filter,
      title: "Military-Focused Filtering", 
      description: "Automatically excludes irrelevant content (sports, entertainment) and focuses on intelligence themes.",
      highlight: "Zero Noise, Pure Intelligence"
    },
    {
      icon: Globe,
      title: "Singapore Time Operations",
      description: "Scheduled for 06:00 Singapore Time daily with Asia/Singapore timezone configuration.",
      highlight: "06:00 SGT Daily"
    },
    {
      icon: FileText,
      title: "Full Content Access",
      description: "Includes complete 'coffee cup' article content with HTML cleaning and Inoreader integration.",
      highlight: "Full Article Text"
    },
    {
      icon: Clock,
      title: "Real-time Processing",
      description: "Fetches today's articles, processes with AI analysis, and delivers comprehensive reports.",
      highlight: "Same-day Intelligence"
    },
    {
      icon: Users,
      title: "Multi-recipient Delivery",
      description: "Supports multiple email recipients with both HTML viewing and PDF attachments.",
      highlight: "Team Distribution"
    },
    {
      icon: Shield,
      title: "DIS Scholarship Focused",
      description: "Specifically designed for Digital and Intelligence Service scholarship preparation and interviews.",
      highlight: "Interview-Ready Insights"
    }
  ];

  return (
    <div className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            How Strategic Intelligence Works
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Our system transforms raw RSS feeds into actionable military intelligence through 
            AI-powered analysis and strategic categorization.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <div className="flex items-center mb-4">
                <div className="bg-military-100 p-3 rounded-lg">
                  <feature.icon className="h-6 w-6 text-military-600" />
                </div>
              </div>
              
              <h3 className="text-lg font-bold text-gray-900 mb-2">
                {feature.title}
              </h3>
              
              <p className="text-gray-600 mb-3 text-sm leading-relaxed">
                {feature.description}
              </p>
              
              <div className="bg-military-50 px-3 py-1 rounded-full inline-block">
                <span className="text-xs font-semibold text-military-700">
                  {feature.highlight}
                </span>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-16 bg-white rounded-2xl p-8 shadow-lg">
          <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">
            Efficient Processing Flow
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-military-600 text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                1
              </div>
              <h4 className="text-lg font-semibold mb-2">Focus Folder Fetch</h4>
              <p className="text-gray-600 text-sm">
                API call to get your folder list → Direct fetch from Focus folder contents (~100 articles)
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-military-600 text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                2
              </div>
              <h4 className="text-lg font-semibold mb-2">AI Analysis</h4>
              <p className="text-gray-600 text-sm">
                Clean HTML content → GPT-4 categorization → Strategic intelligence summaries
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-military-600 text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                3
              </div>
              <h4 className="text-lg font-semibold mb-2">Report Delivery</h4>
              <p className="text-gray-600 text-sm">
                Generate HTML + PDF reports → Email delivery with Inoreader links
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Features;