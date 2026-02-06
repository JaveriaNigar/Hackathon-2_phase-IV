// frontend/src/services/agents.ts

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

/**
 * Fetch all agents
 * @returns Promise resolving to array of agents
 */
export const getAgents = async (): Promise<Agent[]> => {
  try {
    // For frontend-only implementation, return sample agents
    const sampleAgents: Agent[] = [
      {
        id: 'agent_1',
        name: 'Productivity Assistant',
        description: 'Helps with organizing tasks and scheduling',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      },
      {
        id: 'agent_2',
        name: 'Focus Master',
        description: 'Assists with maintaining concentration',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      }
    ];

    return sampleAgents;
  } catch (error) {
    console.error('Error fetching agents:', error);
    throw error;
  }
};

/**
 * Fetch all skills
 * @returns Promise resolving to array of skills
 */
export const getSkills = async (): Promise<Skill[]> => {
  try {
    // For frontend-only implementation, return sample skills
    const sampleSkills: Skill[] = [
      {
        id: 'skill_1',
        name: 'Time Management',
        description: 'Optimize your schedule and prioritize tasks',
        categoryId: 'productivity',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      },
      {
        id: 'skill_2',
        name: 'Goal Setting',
        description: 'Define and track your objectives',
        categoryId: 'planning',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      },
      {
        id: 'skill_3',
        name: 'Focus Enhancement',
        description: 'Techniques to maintain attention',
        categoryId: 'focus',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      }
    ];

    return sampleSkills;
  } catch (error) {
    console.error('Error fetching skills:', error);
    throw error;
  }
};