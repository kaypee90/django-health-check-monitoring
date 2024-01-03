import axios, { AxiosResponse } from 'axios'

const baseUrl = process.env.API_BASE_URL || ""

export const instance = axios.create({
    baseURL: baseUrl
  })

instance.interceptors.response.use(response => response.data as AxiosResponse<unknown>)
