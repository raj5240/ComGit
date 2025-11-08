import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
})

// Add token to requests
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// Handle token expiration
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token')
            localStorage.removeItem('user')
            window.location.href = '/login'
        }
        return Promise.reject(error)
    }
)

export const authAPI = {
    signup: async (username, email, password) => {
        const response = await api.post('/signup', { username, email, password })
        return response.data
    },

    login: async (email, password) => {
        const response = await api.post('/login', { email, password })
        return response.data
    },
}

export const compareAPI = {
    compare: async (url1, url2) => {
        const response = await api.post('/compare', { url1, url2 })
        return response.data
    },
}

export default api

