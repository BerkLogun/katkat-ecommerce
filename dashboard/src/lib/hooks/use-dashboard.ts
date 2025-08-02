import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { DashboardStats, ChartData, TimeSeriesData } from '@/types';

// Query keys
export const dashboardKeys = {
  all: ['dashboard'] as const,
  stats: () => [...dashboardKeys.all, 'stats'] as const,
  charts: () => [...dashboardKeys.all, 'charts'] as const,
  revenue: () => [...dashboardKeys.charts(), 'revenue'] as const,
  orders: () => [...dashboardKeys.charts(), 'orders'] as const,
  products: () => [...dashboardKeys.charts(), 'products'] as const,
};

// Get dashboard statistics
export const useDashboardStats = () => {
  return useQuery({
    queryKey: dashboardKeys.stats(),
    queryFn: async (): Promise<DashboardStats> => {
      return apiClient.get<DashboardStats>('/api/dashboard/stats/');
    },
    refetchInterval: 30000, // Refetch every 30 seconds
  });
};

// Get revenue chart data
export const useRevenueChart = (period: '7d' | '30d' | '90d' = '30d') => {
  return useQuery({
    queryKey: dashboardKeys.revenue(),
    queryFn: async (): Promise<TimeSeriesData[]> => {
      return apiClient.get<TimeSeriesData[]>(`/api/dashboard/charts/revenue/?period=${period}`);
    },
  });
};

// Get orders chart data
export const useOrdersChart = (period: '7d' | '30d' | '90d' = '30d') => {
  return useQuery({
    queryKey: dashboardKeys.orders(),
    queryFn: async (): Promise<TimeSeriesData[]> => {
      return apiClient.get<TimeSeriesData[]>(`/api/dashboard/charts/orders/?period=${period}`);
    },
  });
};

// Get top products chart data
export const useTopProductsChart = (limit: number = 10) => {
  return useQuery({
    queryKey: dashboardKeys.products(),
    queryFn: async (): Promise<ChartData[]> => {
      return apiClient.get<ChartData[]>(`/api/dashboard/charts/products/?limit=${limit}`);
    },
  });
};

// Get recent activity
export const useRecentActivity = () => {
  return useQuery({
    queryKey: [...dashboardKeys.all, 'activity'],
    queryFn: async (): Promise<{
      recent_orders: Array<{
        id: string;
        order_number: string;
        customer_name: string;
        total_amount: number;
        status: string;
        created_at: string;
      }>;
      recent_tenants: Array<{
        id: string;
        name: string;
        created_at: string;
      }>;
      recent_storefronts: Array<{
        id: string;
        store_name: string;
        tenant_name: string;
        created_at: string;
      }>;
    }> => {
      return apiClient.get('/api/dashboard/activity/');
    },
    refetchInterval: 60000, // Refetch every minute
  });
};

// Get system health
export const useSystemHealth = () => {
  return useQuery({
    queryKey: [...dashboardKeys.all, 'health'],
    queryFn: async (): Promise<{
      status: 'healthy' | 'warning' | 'error';
      services: {
        database: { status: string; response_time: number };
        redis: { status: string; response_time: number };
        api: { status: string; response_time: number };
      };
      uptime: number;
      memory_usage: number;
      cpu_usage: number;
    }> => {
      return apiClient.get('/api/dashboard/health/');
    },
    refetchInterval: 30000, // Refetch every 30 seconds
  });
}; 