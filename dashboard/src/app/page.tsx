'use client';

import Link from 'next/link';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Welcome to KatKat
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Create and manage your multi-tenant e-commerce storefronts
          </p>
          <div className="flex justify-center space-x-4">
            <Link
              href="/auth/register"
              className="bg-blue-600 text-white px-6 py-3 rounded-md font-medium hover:bg-blue-700 transition-colors"
            >
              Get Started
            </Link>
            <Link
              href="/auth/login"
              className="bg-gray-200 text-gray-900 px-6 py-3 rounded-md font-medium hover:bg-gray-300 transition-colors"
            >
              Sign In
            </Link>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <span className="text-2xl mr-2">🚀</span>
                Quick Setup
              </CardTitle>
              <CardDescription>
                Create your storefront in minutes with our intuitive builder
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                Register an account, create your first storefront, and start selling online with our streamlined process.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <span className="text-2xl mr-2">🎨</span>
                Customizable
              </CardTitle>
              <CardDescription>
                Fully customizable themes and branding options
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                Customize colors, fonts, layouts, and more to match your brand identity perfectly.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <span className="text-2xl mr-2">📊</span>
                Analytics
              </CardTitle>
              <CardDescription>
                Track performance and insights
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                Monitor sales, traffic, and customer behavior with comprehensive analytics and reporting.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Link
              href="/auth/register"
              className="block p-6 border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-md transition-all"
            >
              <div className="text-center">
                <div className="text-3xl mb-2">👤</div>
                <h3 className="font-semibold text-gray-900">Create Account</h3>
                <p className="text-sm text-gray-600 mt-1">Start your journey</p>
              </div>
            </Link>

            <Link
              href="/auth/login"
              className="block p-6 border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-md transition-all"
            >
              <div className="text-center">
                <div className="text-3xl mb-2">🔐</div>
                <h3 className="font-semibold text-gray-900">Sign In</h3>
                <p className="text-sm text-gray-600 mt-1">Access your dashboard</p>
              </div>
            </Link>

            <Link
              href="/storefronts/create"
              className="block p-6 border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-md transition-all"
            >
              <div className="text-center">
                <div className="text-3xl mb-2">🏪</div>
                <h3 className="font-semibold text-gray-900">Create Storefront</h3>
                <p className="text-sm text-gray-600 mt-1">Build your online store</p>
              </div>
            </Link>

            <Link
              href="/dashboard"
              className="block p-6 border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-md transition-all"
            >
              <div className="text-center">
                <div className="text-3xl mb-2">📈</div>
                <h3 className="font-semibold text-gray-900">View Dashboard</h3>
                <p className="text-sm text-gray-600 mt-1">Monitor performance</p>
              </div>
            </Link>
          </div>
        </div>

        {/* Status Indicators */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
              <span className="text-green-800 font-medium">Backend API</span>
            </div>
            <p className="text-green-600 text-sm mt-1">Running on port 8000</p>
          </div>

          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
              <span className="text-green-800 font-medium">Dashboard</span>
            </div>
            <p className="text-green-600 text-sm mt-1">Running on port 3000</p>
          </div>

          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
              <span className="text-green-800 font-medium">Database</span>
            </div>
            <p className="text-green-600 text-sm mt-1">PostgreSQL connected</p>
          </div>
        </div>
      </div>
    </div>
  );
}
