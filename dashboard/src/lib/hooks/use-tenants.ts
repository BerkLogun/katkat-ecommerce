import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { Tenant, CreateTenantForm, PaginatedResponse } from '@/types';

// Query keys
export const tenantKeys = {
  all: ['tenants'] as const,
  lists: () => [...tenantKeys.all, 'list'] as const,
  list: (filters: Record<string, unknown>) => [...tenantKeys.lists(), filters] as const,
  details: () => [...tenantKeys.all, 'detail'] as const,
  detail: (id: string) => [...tenantKeys.details(), id] as const,
};

// Get all tenants
export const useTenants = (params?: Record<string, string | number | boolean>) => {
  return useQuery({
    queryKey: tenantKeys.list(params || {}),
    queryFn: async (): Promise<PaginatedResponse<Tenant>> => {
      return apiClient.get<PaginatedResponse<Tenant>>('/tenants/', { params });
    },
  });
};

// Get single tenant
export const useTenant = (id: string) => {
  return useQuery({
    queryKey: tenantKeys.detail(id),
    queryFn: async (): Promise<Tenant> => {
      return apiClient.get<Tenant>(`/tenants/${id}/`);
    },
    enabled: !!id,
  });
};

// Create tenant
export const useCreateTenant = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateTenantForm): Promise<Tenant> => {
      return apiClient.post<Tenant>('/tenants/', data);
    },
    onSuccess: () => {
      // Invalidate and refetch tenants list
      queryClient.invalidateQueries({ queryKey: tenantKeys.lists() });
    },
  });
};

// Update tenant
export const useUpdateTenant = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, data }: { id: string; data: Partial<Tenant> }): Promise<Tenant> => {
      return apiClient.patch<Tenant>(`/tenants/${id}/`, data);
    },
    onSuccess: (updatedTenant) => {
      // Update the specific tenant in cache
      queryClient.setQueryData(tenantKeys.detail(updatedTenant.id), updatedTenant);
      
      // Invalidate and refetch tenants list
      queryClient.invalidateQueries({ queryKey: tenantKeys.lists() });
    },
  });
};

// Delete tenant
export const useDeleteTenant = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string): Promise<void> => {
      return apiClient.delete<void>(`/tenants/${id}/`);
    },
    onSuccess: (_, deletedId) => {
      // Remove from cache
      queryClient.removeQueries({ queryKey: tenantKeys.detail(deletedId) });
      
      // Invalidate and refetch tenants list
      queryClient.invalidateQueries({ queryKey: tenantKeys.lists() });
    },
  });
};

// Get tenant statistics
export const useTenantStats = (id: string) => {
  return useQuery({
    queryKey: [...tenantKeys.detail(id), 'stats'],
    queryFn: async (): Promise<{
      products_count: number;
      orders_count: number;
      storage_used_mb: number;
    }> => {
      return apiClient.get(`/tenants/${id}/stats/`);
    },
    enabled: !!id,
  });
};

// Get tenant usage
export const useTenantUsage = (id: string) => {
  return useQuery({
    queryKey: [...tenantKeys.detail(id), 'usage'],
    queryFn: async (): Promise<{
      products_used: number;
      orders_used: number;
      storage_used: number;
      limits: {
        products: number;
        orders: number;
        storage: number;
      };
    }> => {
      return apiClient.get(`/tenants/${id}/usage/`);
    },
    enabled: !!id,
  });
}; 