'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import AuthGuard from '@/components/auth/AuthGuard';
import AuthenticatedLayout from '@/components/layout/AuthenticatedLayout';

export default function CreateStorefrontPage() {
  const [formData, setFormData] = useState({
    store_name: '',
    store_description: '',
    logo_url: '',
    favicon_url: '',
    meta_title: '',
    meta_description: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await fetch('/api/storefronts/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('auth-storage') ? JSON.parse(localStorage.getItem('auth-storage')!).state.token : ''}`
        },
        body: JSON.stringify({
          ...formData,
          tenant_id: 1 // For now, using the first tenant
        }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Storefront created successfully:', data);
        router.push('/storefronts');
      } else {
        const errorData = await response.json();
        setError(errorData.message || 'Failed to create storefront');
      }
    } catch (err) {
      setError('An error occurred while creating the storefront');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthGuard>
      <AuthenticatedLayout>
        <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Create New Storefront</h1>
          <p className="mt-2 text-gray-600">Set up your online store with a custom storefront</p>
        </div>
        
        <Card>
          <CardHeader>
            <CardTitle>Storefront Details</CardTitle>
            <CardDescription>Configure your storefront settings and branding</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="store_name" className="block text-sm font-medium text-gray-700">
                  Storefront Name *
                </label>
                <input
                  id="store_name"
                  name="store_name"
                  type="text"
                  required
                  value={formData.store_name}
                  onChange={handleChange}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="My Awesome Store"
                />
              </div>

              <div>
                <label htmlFor="store_description" className="block text-sm font-medium text-gray-700">
                  Description
                </label>
                <textarea
                  id="store_description"
                  name="store_description"
                  rows={3}
                  value={formData.store_description}
                  onChange={handleChange}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="Describe your store and what you sell..."
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label htmlFor="logo_url" className="block text-sm font-medium text-gray-700">
                    Logo URL
                  </label>
                  <input
                    id="logo_url"
                    name="logo_url"
                    type="url"
                    value={formData.logo_url}
                    onChange={handleChange}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    placeholder="https://example.com/logo.png"
                  />
                </div>
                
                <div>
                  <label htmlFor="favicon_url" className="block text-sm font-medium text-gray-700">
                    Favicon URL
                  </label>
                  <input
                    id="favicon_url"
                    name="favicon_url"
                    type="url"
                    value={formData.favicon_url}
                    onChange={handleChange}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    placeholder="https://example.com/favicon.ico"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="meta_title" className="block text-sm font-medium text-gray-700">
                  Meta Title
                </label>
                <input
                  id="meta_title"
                  name="meta_title"
                  type="text"
                  value={formData.meta_title}
                  onChange={handleChange}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="SEO title for search engines"
                />
              </div>

              <div>
                <label htmlFor="meta_description" className="block text-sm font-medium text-gray-700">
                  Meta Description
                </label>
                <textarea
                  id="meta_description"
                  name="meta_description"
                  rows={2}
                  value={formData.meta_description}
                  onChange={handleChange}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="SEO description for search engines"
                />
              </div>

              {error && (
                <div className="text-red-600 text-sm bg-red-50 p-3 rounded-md">
                  {error}
                </div>
              )}

              <div className="flex justify-end space-x-4">
                <button
                  type="button"
                  onClick={() => router.back()}
                  className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? 'Creating...' : 'Create Storefront'}
                </button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
        </div>
      </AuthenticatedLayout>
    </AuthGuard>
  );
} 