import React from 'react';
import { Globe, Shield, Zap, Lock, Sword, Scale, Eye, Filter } from 'lucide-react';

const Themes: React.FC = () => {
  const themes = [
    {
      icon: Globe,
      emoji: "🌍",
      title: "Geopolitical Tensions",
      description: "Statecraft, balance of power, regional flashpoints",
      topics: [
        "Great Power Competition – US-China relations, Russia-West dynamics",
        "Indo-Pacific Security – Taiwan Strait, South China Sea, AUKUS, QUAD", 
        "ASEAN & Regional Politics – Military coups, foreign interference",
        "Middle East Conflicts – Iran nuclear talks, Israel-Palestine",
        "Africa Rising – Military coups, China's Belt and Road"
      ]
    },
    {
      icon: Shield,
      emoji: "🔒",
      title: "Cybersecurity Warfare",
      description: "Threat actors, espionage, hybrid warfare",
      topics: [
        "Nation-State APTs – Operations by China, Russia, North Korea, Iran",
        "Critical Infrastructure Attacks – Energy, banking, transport, satellites",
        "Cyber Norms & Treaties – Global cyber law, cyber diplomacy",
        "Disinformation & Deepfakes – Influence ops, election interference",
        "Zero-Day Exploits – Major vulnerabilities (Log4j, SolarWinds)"
      ]
    },
    {
      icon: Zap,
      emoji: "⚡",
      title: "Emerging Tech",
      description: "Military tech, dual-use innovation, techno-nationalism",
      topics: [
        "AI & Autonomous Weapons – Swarming drones, LAWS, battlefield AI",
        "Quantum Computing – Decryption threats, military R&D races",
        "Space Militarization – ASAT weapons, satellite constellations",
        "Semiconductor Supply Chain – Chip wars, export controls",
        "Biotechnology & Synthetic Biology – CRISPR, biosecurity risks"
      ]
    },
    {
      icon: Lock,
      emoji: "🛡️",
      title: "National Security",
      description: "Homeland protection, resilience, extremist threats",
      topics: [
        "Terrorism & Extremism – Islamic State, right-wing extremism",
        "Pandemics & Biosecurity – Disease outbreaks, public health prep",
        "Social Cohesion Risks – Ethnic tensions, online radicalization",
        "Energy & Food Security – Resource scarcity, supply chain risks"
      ]
    },
    {
      icon: Sword,
      emoji: "⚔️",
      title: "Military Modernization",
      description: "Strategic posture, operational concepts",
      topics: [
        "Hybrid Warfare – Grey zone conflict, psychological ops",
        "Civil-Military Relations – Military roles in governance, coups",
        "Military Alliances & Exercises – NATO, RIMPAC, Shangri-La",
        "Defense Procurement – Hypersonics, next-gen fighters"
      ]
    },
    {
      icon: Scale,
      emoji: "⚖️",
      title: "Rules-Based Order",
      description: "Global norms, sovereignty, legal frameworks",
      topics: [
        "UN Actions & Deadlocks – Sanctions, peacekeeping, veto politics",
        "Maritime Law & UNCLOS – Freedom of navigation ops",
        "Sovereignty vs. Humanitarian Intervention – Ukraine, Myanmar"
      ]
    },
    {
      icon: Eye,
      emoji: "🔮",
      title: "Strategic Foresight",
      description: "Long-term strategic risks and opportunities",
      topics: [
        "Climate Security – Arctic passage, resource conflicts",
        "Demographic Shifts – Aging, urbanization, youth bulges",
        "Urban Warfare – Conflict in megacities, infrastructure targeting",
        "Rise of Non-State Actors – PMCs, cybercrime syndicates"
      ]
    }
  ];

  return (
    <div className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            7 Intelligence Themes for DIS Preparation
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Our AI automatically categorizes articles into these strategic themes, 
            specifically designed for Digital and Intelligence Service scholarship interviews.
          </p>
          
          <div className="mt-8 flex items-center justify-center gap-4 p-4 bg-gray-50 rounded-lg max-w-2xl mx-auto">
            <Filter className="h-6 w-6 text-military-600" />
            <span className="text-sm font-medium text-gray-700">
              Articles not relevant to military/intelligence analysis are automatically excluded
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {themes.map((theme, index) => (
            <div key={index} className="bg-gray-50 rounded-2xl p-8 hover:bg-gray-100 transition-colors duration-200">
              <div className="flex items-start mb-6">
                <div className="bg-white rounded-xl p-3 mr-4 shadow-sm">
                  <span className="text-2xl">{theme.emoji}</span>
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">
                    {theme.title}
                  </h3>
                  <p className="text-military-600 font-medium">
                    {theme.description}
                  </p>
                </div>
              </div>

              <div className="space-y-3">
                {theme.topics.map((topic, topicIndex) => (
                  <div key={topicIndex} className="flex items-start">
                    <div className="w-2 h-2 bg-military-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span className="text-gray-700 text-sm leading-relaxed">
                      {topic}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="mt-16 bg-gradient-to-r from-military-600 to-blue-600 rounded-2xl p-8 text-white text-center">
          <h3 className="text-2xl font-bold mb-4">
            Why These Themes Matter for DIS Interviews
          </h3>
          <p className="text-lg text-white/90 max-w-3xl mx-auto leading-relaxed">
            These themes reflect the likely focus areas for Digital and Intelligence Service scholarship interviews, 
            which assess your understanding of world events, analysis capabilities, and strategic foresight. 
            Our AI ensures you're prepared with the most relevant intelligence insights.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Themes;