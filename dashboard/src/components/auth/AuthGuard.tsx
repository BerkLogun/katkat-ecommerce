'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/stores/auth-store';

interface AuthGuardProps {
  children: React.ReactNode;
  requireAuth?: boolean;
  redirectTo?: string;
}

export default function AuthGuard({ 
  children, 
  requireAuth = true, 
  redirectTo = '/auth/login' 
}: AuthGuardProps) {
  const { isAuthenticated, isLoading } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading) {
      if (requireAuth && !isAuthenticated) {
        router.push(redirectTo);
      } else if (!requireAuth && isAuthenticated) {
        // If user is authenticated but trying to access auth pages, redirect to dashboard
        router.push('/dashboard');
      }
    }
  }, [isAuthenticated, isLoading, requireAuth, redirectTo, router]);

  // Show loading spinner while checking authentication
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  // If authentication check is complete and conditions are met, render children
  if (requireAuth && isAuthenticated) {
    return <>{children}</>;
  }

  if (!requireAuth && !isAuthenticated) {
    return <>{children}</>;
  }

  // Don't render anything while redirecting
  return null;
} 