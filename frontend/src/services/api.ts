import axios from 'axios';
import { getToken } from '@/lib/auth';

const getBaseURL = () => {
  const url = process.env.NEXT_PUBLIC_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'https://javeria-nigar-todo-ai.hf.space/api/';
  return url.endsWith('/') ? url : `${url}/`;
};

// Create an axios instance with base configuration
// Create an axios instance with base configuration
const apiClient = axios.create({
  baseURL: getBaseURL(),
  timeout: 60000, // 60 seconds timeout (increased for AI processing)
});

// Add a request interceptor to include auth headers if needed
apiClient.interceptors.request.use(
  (config) => {
    // Add any auth tokens or other headers here
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle responses globally
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('>>> API Error Occurred <<<');
    console.error('Error Code:', error.code);
    console.error('Error Message:', error.message);

    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error('Server Responded with Error:', {
        status: error.response.status,
        statusText: error.response.statusText,
        data: error.response.data,
      });
    } else if (error.request) {
      // The request was made but no response was received
      console.error('No Response Received (Network Error):', error.request);
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('Request Setup Error:', error.message);
    }

    if (error.config) {
      console.error('Request Config:', {
        url: error.config.url,
        method: error.config.method,
        baseURL: error.config.baseURL,
        headers: error.config.headers,
      });
    }
    return Promise.reject(error);
  }
);

// Export specific API functions
export const chatApi = {
  sendMessage: async (userId: string, message: string, conversationId?: string) => {
    // The backend expects /api/{user_id}/chat
    // baseURL is already /api, so we just need {user_id}/chat
    const response = await apiClient.post(`${userId}/chat`, {
      message,
      conversation_id: conversationId,
    });
    return response.data;
  },

  deleteConversation: async (userId: string, conversationId: string) => {
    const response = await apiClient.delete(`${userId}/conversations/${conversationId}`);
    return response.data;
  },

  createTask: async (userId: string, title: string, description?: string) => {
    const response = await apiClient.post(`${userId}/tasks`, {
      title,
      description,
    });
    return response.data;
  },

  getTasks: async (userId: string, status: string = 'all') => {
    const response = await apiClient.get(`${userId}/tasks`, {
      params: { status },
    });
    return response.data;
  },

  checkHealth: async () => {
    const baseUrl = getBaseURL();
    const healthUrl = baseUrl.replace('/api/', '/health');
    const response = await axios.get(healthUrl);
    return response.data;
  },
};

export default apiClient;