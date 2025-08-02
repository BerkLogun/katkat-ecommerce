import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { Storefront, CreateStorefrontForm, Theme, PaginatedResponse } from '@/types';

// Query keys
export const storefrontKeys = {
  all: ['storefronts'] as const,
  lists: () => [...storefrontKeys.all, 'list'] as const,
  list: (filters: Record<string, unknown>) => [...storefrontKeys.lists(), filters] as const,
  details: () => [...storefrontKeys.all, 'detail'] as const,
  detail: (id: string) => [...storefrontKeys.details(), id] as const,
  themes: () => [...storefrontKeys.all, 'themes'] as const,
  theme: (id: string) => [...storefrontKeys.themes(), id] as const,
};

// Get all storefronts
export const useStorefronts = (params?: Record<string, string | number | boolean>) => {
  return useQuery({
    queryKey: storefrontKeys.list(params || {}),
    queryFn: async (): Promise<PaginatedResponse<Storefront>> => {
      return apiClient.get<PaginatedResponse<Storefront>>('/storefronts/', { params });
    },
  });
};

// Get single storefront
export const useStorefront = (id: string) => {
  return useQuery({
    queryKey: storefrontKeys.detail(id),
    queryFn: async (): Promise<Storefront> => {
      return apiClient.get<Storefront>(`/storefronts/${id}/`);
    },
    enabled: !!id,
  });
};

// Create storefront
export const useCreateStorefront = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateStorefrontForm): Promise<Storefront> => {
      return apiClient.post<Storefront>('/storefronts/', data);
    },
    onSuccess: () => {
      // Invalidate and refetch storefronts list
      queryClient.invalidateQueries({ queryKey: storefrontKeys.lists() });
    },
  });
};

// Update storefront
export const useUpdateStorefront = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, data }: { id: string; data: Partial<Storefront> }): Promise<Storefront> => {
      return apiClient.patch<Storefront>(`/storefronts/${id}/`, data);
    },
    onSuccess: (updatedStorefront) => {
      // Update the specific storefront in cache
      queryClient.setQueryData(storefrontKeys.detail(updatedStorefront.id), updatedStorefront);
      
      // Invalidate and refetch storefronts list
      queryClient.invalidateQueries({ queryKey: storefrontKeys.lists() });
    },
  });
};

// Delete storefront
export const useDeleteStorefront = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string): Promise<void> => {
      return apiClient.delete<void>(`/storefronts/${id}/`);
    },
    onSuccess: (_, deletedId) => {
      // Remove from cache
      queryClient.removeQueries({ queryKey: storefrontKeys.detail(deletedId) });
      
      // Invalidate and refetch storefronts list
      queryClient.invalidateQueries({ queryKey: storefrontKeys.lists() });
    },
  });
};

// Get storefront theme
export const useStorefrontTheme = (storefrontId: string) => {
  return useQuery({
    queryKey: storefrontKeys.theme(storefrontId),
    queryFn: async (): Promise<Theme> => {
      return apiClient.get<Theme>(`/storefronts/${storefrontId}/theme/`);
    },
    enabled: !!storefrontId,
  });
};

// Update storefront theme
export const useUpdateStorefrontTheme = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ storefrontId, data }: { storefrontId: string; data: Partial<Theme> }): Promise<Theme> => {
      return apiClient.patch<Theme>(`/storefronts/${storefrontId}/theme/`, data);
    },
    onSuccess: (updatedTheme, variables) => {
      // Update the theme in cache
      queryClient.setQueryData(storefrontKeys.theme(variables.storefrontId), updatedTheme);
    },
  });
};

// Publish storefront
export const usePublishStorefront = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string): Promise<Storefront> => {
      return apiClient.post<Storefront>(`/storefronts/${id}/publish/`);
    },
    onSuccess: (updatedStorefront) => {
      // Update the specific storefront in cache
      queryClient.setQueryData(storefrontKeys.detail(updatedStorefront.id), updatedStorefront);
      
      // Invalidate and refetch storefronts list
      queryClient.invalidateQueries({ queryKey: storefrontKeys.lists() });
    },
  });
};

// Unpublish storefront
export const useUnpublishStorefront = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string): Promise<Storefront> => {
      return apiClient.post<Storefront>(`/storefronts/${id}/unpublish/`);
    },
    onSuccess: (updatedStorefront) => {
      // Update the specific storefront in cache
      queryClient.setQueryData(storefrontKeys.detail(updatedStorefront.id), updatedStorefront);
      
      // Invalidate and refetch storefronts list
      queryClient.invalidateQueries({ queryKey: storefrontKeys.lists() });
    },
  });
}; 