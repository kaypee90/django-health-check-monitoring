export type HealthCheckCount = {
    name: string
    status: number
    count: number
}

export interface HealthCheckSummary {
    name: string;
    statusId: number;
    status: string;
    count: number;
  }
