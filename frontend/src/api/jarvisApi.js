import axios from 'axios';

const API_BASE = '/api';

class JarvisAPI {
  async processText(text, contextId = null) {
    const response = await axios.post(`${API_BASE}/text`, {
      text,
      context_id: contextId
    });
    return response.data;
  }

  async processMultimodal(formData) {
    const response = await axios.post(`${API_BASE}/process`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  }

  async getScene(contextId) {
    const response = await axios.get(`${API_BASE}/scene/${contextId}`);
    return response.data;
  }

  async listScenes() {
    const response = await axios.get(`${API_BASE}/scenes`);
    return response.data;
  }

  async deleteScene(contextId) {
    const response = await axios.delete(`${API_BASE}/scene/${contextId}`);
    return response.data;
  }

  async healthCheck() {
    const response = await axios.get('/health');
    return response.data;
  }
}

export default new JarvisAPI();

