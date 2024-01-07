import axios, { AxiosResponse } from 'axios'

const baseUrl = process.env.API_BASE_URL ?? "http://localhost:8000/v1"

export const instance = axios.create({
    baseURL: baseUrl
  })

instance.interceptors.response.use(response => response.data as AxiosResponse<unknown>)
