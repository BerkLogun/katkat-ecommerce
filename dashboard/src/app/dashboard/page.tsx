'use client';

import Link from 'next/link';
import { useDashboardStats, useRecentActivity, useSystemHealth } from '@/lib/hooks/use-dashboard';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Activity, Users, ShoppingCart, Store, TrendingUp, AlertCircle, Plus } from 'lucide-react';
import AuthGuard from '@/components/auth/AuthGuard';
import AuthenticatedLayout from '@/components/layout/AuthenticatedLayout';

export default function DashboardPage() {
  const { data: stats, isLoading: statsLoading } = useDashboardStats();
  const { data: activity, isLoading: activityLoading } = useRecentActivity();
  const { data: health, isLoading: healthLoading } = useSystemHealth();

  if (statsLoading || activityLoading || healthLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <AuthGuard>
      <AuthenticatedLayout>
        <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-700">Welcome to your KatKat dashboard</p>
        </div>
        <div className="flex items-center space-x-4">
          <Link
            href="/storefronts/create"
            className="bg-blue-600 text-white px-4 py-2 rounded-md font-medium hover:bg-blue-700 transition-colors flex items-center"
          >
            <Plus className="h-4 w-4 mr-2" />
            Create Storefront
          </Link>
          <Badge 
            variant={health?.status === 'healthy' ? 'default' : 'destructive'}
            className="flex items-center space-x-1"
          >
            {health?.status === 'healthy' ? (
              <Activity className="h-3 w-3" />
            ) : (
              <AlertCircle className="h-3 w-3" />
            )}
            <span className="capitalize">{health?.status || 'unknown'}</span>
          </Badge>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Tenants</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.total_tenants || 0}</div>
            <p className="text-xs text-gray-700">
              Active multi-tenant organizations
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Storefronts</CardTitle>
            <Store className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.total_storefronts || 0}</div>
            <p className="text-xs text-gray-700">
              Published e-commerce stores
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Orders</CardTitle>
            <ShoppingCart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.total_orders || 0}</div>
            <p className="text-xs text-gray-700">
              Orders across all storefronts
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${(stats?.total_revenue || 0).toLocaleString()}
            </div>
            <p className="text-xs text-gray-700">
              Revenue across all storefronts
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription className="text-gray-700">Common tasks and shortcuts</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <Link
              href="/storefronts/create"
              className="block w-full text-left p-3 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors"
            >
              <div className="flex items-center">
                <Plus className="h-5 w-5 text-blue-600 mr-3" />
                <div>
                  <p className="font-medium text-gray-900">Create Storefront</p>
                  <p className="text-sm text-gray-700">Build a new online store</p>
                </div>
              </div>
            </Link>
            
            <Link
              href="/storefronts"
              className="block w-full text-left p-3 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors"
            >
              <div className="flex items-center">
                <Store className="h-5 w-5 text-blue-600 mr-3" />
                <div>
                  <p className="font-medium text-gray-900">Manage Storefronts</p>
                  <p className="text-sm text-gray-700">View and edit your stores</p>
                </div>
              </div>
            </Link>
            
            <Link
              href="/tenants"
              className="block w-full text-left p-3 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors"
            >
              <div className="flex items-center">
                <Users className="h-5 w-5 text-blue-600 mr-3" />
                <div>
                  <p className="font-medium text-gray-900">Manage Tenants</p>
                  <p className="text-sm text-gray-700">Organize your businesses</p>
                </div>
              </div>
            </Link>
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <div className="md:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Recent Activity</CardTitle>
              <CardDescription className="text-gray-700">Latest orders and storefront updates</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {activity?.recent_orders?.slice(0, 5).map((order) => (
                  <div key={order.id} className="flex items-center justify-between p-3 border border-gray-100 rounded-lg">
                    <div>
                      <p className="font-medium">{order.order_number}</p>
                      <p className="text-sm text-gray-700">{order.customer_name}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-medium">${order.total_amount}</p>
                      <Badge variant="outline" className="text-xs">
                        {order.status}
                      </Badge>
                    </div>
                  </div>
                ))}
                {(!activity?.recent_orders || activity.recent_orders.length === 0) && (
                  <div className="text-center py-8 text-gray-600">
                    <ShoppingCart className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                    <p>No recent orders</p>
                    <p className="text-sm">Orders will appear here once customers start shopping</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* System Health */}
      {health && (
        <Card>
          <CardHeader>
            <CardTitle>System Health</CardTitle>
            <CardDescription className="text-gray-700">Current system status and performance</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <p className="text-sm font-medium">Database</p>
                <div className="flex items-center space-x-2">
                  <Badge variant={health.services.database.status === 'ok' ? 'default' : 'destructive'}>
                    {health.services.database.status}
                  </Badge>
                  <span className="text-sm text-gray-700">
                    {health.services.database.response_time}ms
                  </span>
                </div>
              </div>
              <div className="space-y-2">
                <p className="text-sm font-medium">Redis</p>
                <div className="flex items-center space-x-2">
                  <Badge variant={health.services.redis.status === 'ok' ? 'default' : 'destructive'}>
                    {health.services.redis.status}
                  </Badge>
                  <span className="text-sm text-gray-700">
                    {health.services.redis.response_time}ms
                  </span>
                </div>
              </div>
              <div className="space-y-2">
                <p className="text-sm font-medium">API</p>
                <div className="flex items-center space-x-2">
                  <Badge variant={health.services.api.status === 'ok' ? 'default' : 'destructive'}>
                    {health.services.api.status}
                  </Badge>
                  <span className="text-sm text-gray-700">
                    {health.services.api.response_time}ms
                  </span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
        </div>
      </AuthenticatedLayout>
    </AuthGuard>
  );
} 