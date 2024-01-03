import { HealthCheckCount } from '../models/index'
import { instance } from './api-client'

export type HealthCheckCountResponse = {
    data: HealthCheckCount[]
}

export const getHealthCheckCountData = (): Promise<HealthCheckCountResponse> => instance.get('/healthcheckjobs')