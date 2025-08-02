'use client';

import Link from 'next/link';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Plus, Store, Eye, Edit, Settings } from 'lucide-react';
import AuthGuard from '@/components/auth/AuthGuard';
import AuthenticatedLayout from '@/components/layout/AuthenticatedLayout';

export default function StorefrontsPage() {
  // Mock data for now - this would come from the API
  const storefronts = [
    {
      id: 1,
      name: "My First Store",
      description: "A beautiful online store for my products",
      is_published: true,
      created_at: "2024-01-15T10:30:00Z",
      theme: {
        primary_color: "#3B82F6"
      }
    },
    {
      id: 2,
      name: "Fashion Boutique",
      description: "Trendy fashion items for everyone",
      is_published: false,
      created_at: "2024-01-10T14:20:00Z",
      theme: {
        primary_color: "#EC4899"
      }
    }
  ];

  return (
    <AuthGuard>
      <AuthenticatedLayout>
        <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Storefronts</h1>
          <p className="text-gray-600">Manage your online stores and e-commerce platforms</p>
        </div>
        <Link
          href="/storefronts/create"
          className="bg-blue-600 text-white px-4 py-2 rounded-md font-medium hover:bg-blue-700 transition-colors flex items-center"
        >
          <Plus className="h-4 w-4 mr-2" />
          Create Storefront
        </Link>
      </div>

      {storefronts.length === 0 ? (
        <Card>
          <CardContent className="text-center py-12">
            <Store className="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No storefronts yet</h3>
            <p className="text-gray-600 mb-6">Create your first storefront to start selling online</p>
            <Link
              href="/storefronts/create"
              className="bg-blue-600 text-white px-6 py-3 rounded-md font-medium hover:bg-blue-700 transition-colors inline-flex items-center"
            >
              <Plus className="h-4 w-4 mr-2" />
              Create Your First Storefront
            </Link>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {storefronts.map((storefront) => (
            <Card key={storefront.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="flex items-center">
                    <div 
                      className="w-4 h-4 rounded-full mr-3" 
                      style={{ backgroundColor: storefront.theme.primary_color }}
                    ></div>
                    {storefront.name}
                  </CardTitle>
                  <Badge variant={storefront.is_published ? "default" : "secondary"}>
                    {storefront.is_published ? "Published" : "Draft"}
                  </Badge>
                </div>
                <CardDescription>{storefront.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="text-sm text-gray-600">
                    Created: {new Date(storefront.created_at).toLocaleDateString()}
                  </div>
                  
                  <div className="flex space-x-2">
                    <Link
                      href={`/storefronts/${storefront.id}`}
                      className="flex-1 bg-gray-100 text-gray-700 px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-200 transition-colors flex items-center justify-center"
                    >
                      <Eye className="h-4 w-4 mr-1" />
                      View
                    </Link>
                    <Link
                      href={`/storefronts/${storefront.id}/edit`}
                      className="flex-1 bg-blue-100 text-blue-700 px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-200 transition-colors flex items-center justify-center"
                    >
                      <Edit className="h-4 w-4 mr-1" />
                      Edit
                    </Link>
                    <Link
                      href={`/storefronts/${storefront.id}/settings`}
                      className="flex-1 bg-gray-100 text-gray-700 px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-200 transition-colors flex items-center justify-center"
                    >
                      <Settings className="h-4 w-4 mr-1" />
                      Settings
                    </Link>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-blue-600">{storefronts.length}</div>
            <div className="text-sm text-gray-600">Total Storefronts</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-green-600">
              {storefronts.filter(s => s.is_published).length}
            </div>
            <div className="text-sm text-gray-600">Published</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-yellow-600">
              {storefronts.filter(s => !s.is_published).length}
            </div>
            <div className="text-sm text-gray-600">Drafts</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-purple-600">0</div>
            <div className="text-sm text-gray-600">Total Orders</div>
          </CardContent>
        </Card>
      </div>
        </div>
      </AuthenticatedLayout>
    </AuthGuard>
  );
} 