import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000'

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const registerTourist = async (touristData) => {
  const response = await api.post('/register', touristData)
  return response.data
}

export const getAllTourists = async () => {
  const response = await api.get('/tourists')
  return response.data
}

export const getTourist = async (touristId) => {
  const response = await api.get(`/tourists/${touristId}`)
  return response.data
}

export const sendSOS = async (sosData) => {
  const response = await api.post('/sos', sosData)
  return response.data
}

export const getAllAlerts = async () => {
  const response = await api.get('/alerts')
  return response.data
}

export const getAlert = async (alertId) => {
  const response = await api.get(`/alerts/${alertId}`)
  return response.data
}

export const resolveAlert = async (alertId) => {
  const response = await api.post(`/alerts/${alertId}/resolve`)
  return response.data
}

export const getZones = async () => {
  const response = await api.get('/zones')
  return response.data
}

export default api