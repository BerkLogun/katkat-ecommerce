import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { User, LoginForm } from '@/types';
import { useAuthStore } from '@/lib/stores/auth-store';

// Query keys
export const authKeys = {
  all: ['auth'] as const,
  user: () => [...authKeys.all, 'user'] as const,
  login: () => [...authKeys.all, 'login'] as const,
  register: () => [...authKeys.all, 'register'] as const,
};

// Get current user
export const useCurrentUser = () => {
  return useQuery({
    queryKey: authKeys.user(),
    queryFn: async (): Promise<User> => {
      return apiClient.get<User>('/api/auth/me/');
    },
    enabled: false, // We'll manually trigger this when needed
  });
};

// Login mutation
export const useLogin = () => {
  const queryClient = useQueryClient();
  const { setAuthData } = useAuthStore();

  return useMutation({
    mutationFn: async (credentials: LoginForm): Promise<{ user: User; access: string }> => {
      return apiClient.post<{ user: User; access: string }>('/api/auth/login/', credentials);
    },
    onSuccess: async (data) => {
      // Update auth store with user data and token
      setAuthData(data.user, data.access);
      
      // Invalidate and refetch user data
      await queryClient.invalidateQueries({ queryKey: authKeys.user() });
      
      // Prefetch user data
      await queryClient.prefetchQuery({
        queryKey: authKeys.user(),
        queryFn: () => Promise.resolve(data.user),
      });
    },
  });
};

// Logout mutation
export const useLogout = () => {
  const queryClient = useQueryClient();
  const { logout: authStoreLogout } = useAuthStore();

  return useMutation({
    mutationFn: async (): Promise<void> => {
      return apiClient.post<void>('/api/auth/logout/');
    },
    onSuccess: () => {
      // Clear auth store
      authStoreLogout();
      
      // Clear all queries
      queryClient.clear();
    },
    onError: () => {
      // Even if logout fails, clear local state
      authStoreLogout();
      queryClient.clear();
    },
  });
};

// Registration mutation
export const useRegister = () => {
  return useMutation({
    mutationFn: async (userData: {
      email: string;
      first_name: string;
      last_name: string;
      password: string;
      password_confirm: string;
    }): Promise<{ message: string }> => {
      return apiClient.post<{ message: string }>('/api/auth/register/', userData);
    },
  });
};

// Refresh token
export const useRefreshToken = () => {
  return useMutation({
    mutationFn: async (refresh: string): Promise<{ access: string }> => {
      return apiClient.post<{ access: string }>('/api/auth/refresh/', { refresh });
    },
    onSuccess: (data) => {
      // Update stored token
      const authStorage = localStorage.getItem('auth-storage');
      if (authStorage) {
        const parsed = JSON.parse(authStorage);
        parsed.state.token = data.access;
        localStorage.setItem('auth-storage', JSON.stringify(parsed));
      }
    },
  });
}; 