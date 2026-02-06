// frontend/src/components/agents-skills/AgentsSkillsDisplay.tsx
import React, { useEffect, useState } from 'react';
import { getAgents, getSkills } from '@/services/agents';
import BrownCard from '@/components/theme/BrownCard';

interface Agent {
  id: string;
  name: string;
  description: string;
  createdAt: string;
  updatedAt: string;
}

interface Skill {
  id: string;
  name: string;
  description: string;
  categoryId: string;
  createdAt: string;
  updatedAt: string;
}

const AgentsSkillsDisplay = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAgentsAndSkills = async () => {
      try {
        const [agentsData, skillsData] = await Promise.all([
          getAgents(),
          getSkills()
        ]);

        setAgents(agentsData);
        setSkills(skillsData);
      } catch (err: any) {
        setError(err.message || 'Error fetching agents and skills');
      } finally {
        setLoading(false);
      }
    };

    fetchAgentsAndSkills();
  }, []);

  if (loading) {
    return (
      <div className="text-center py-4">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brown-accent mx-auto"></div>
        <p className="mt-2 text-black">Loading skills...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-brown-light text-brown-accent rounded-lg border border-brown-accent">
        {error}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-black mb-3">Skills</h3>
        <div className="space-y-3">
          {skills.map((skill) => (
            <BrownCard key={skill.id} className="p-3">
              <h4 className="font-medium text-black">{skill.name}</h4>
              <p className="text-sm text-black mt-1">{skill.description}</p>
            </BrownCard>
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold text-black mb-3">Agents</h3>
        <div className="space-y-3">
          {agents.map((agent) => (
            <BrownCard key={agent.id} className="p-3">
              <h4 className="font-medium text-black">{agent.name}</h4>
              <p className="text-sm text-black mt-1">{agent.description}</p>
            </BrownCard>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AgentsSkillsDisplay;