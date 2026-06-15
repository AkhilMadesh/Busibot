import axios, { AxiosInstance, AxiosError } from 'axios'
import { getSession, signOut } from 'next-auth/react'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

class ApiClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Request interceptor
    this.client.interceptors.request.use(
      async (config) => {
        const session = await getSession()
        if (session?.accessToken) {
          config.headers.Authorization = `Bearer ${session.accessToken}`
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        if (error.response?.status === 401) {
          await signOut({ redirect: true, callbackUrl: '/auth/login' })
        }
        return Promise.reject(error)
      }
    )
  }

  async get<T>(url: string, config = {}) {
    const response = await this.client.get<T>(url, config)
    return response.data
  }

  async post<T>(url: string, data = {}, config = {}) {
    const response = await this.client.post<T>(url, data, config)
    return response.data
  }

  async put<T>(url: string, data = {}, config = {}) {
    const response = await this.client.put<T>(url, data, config)
    return response.data
  }

  async patch<T>(url: string, data = {}, config = {}) {
    const response = await this.client.patch<T>(url, data, config)
    return response.data
  }

  async delete<T>(url: string, config = {}) {
    const response = await this.client.delete<T>(url, config)
    return response.data
  }
}

export const apiClient = new ApiClient()
