from django.urls import path
from .views import (
    StorefrontListView,
    StorefrontDetailView,
    StorefrontThemeView,
    StorefrontSettingsView,
    publish_storefront,
    unpublish_storefront,
    public_storefront
)

urlpatterns = [
    # Storefront management
    path('', StorefrontListView.as_view(), name='storefront_list'),
    path('<int:pk>/', StorefrontDetailView.as_view(), name='storefront_detail'),
    path('<int:storefront_id>/theme/', StorefrontThemeView.as_view(), name='storefront_theme'),
    path('<int:storefront_id>/settings/', StorefrontSettingsView.as_view(), name='storefront_settings'),
    path('<int:storefront_id>/publish/', publish_storefront, name='publish_storefront'),
    path('<int:storefront_id>/unpublish/', unpublish_storefront, name='unpublish_storefront'),
    
    # Public storefront view
    path('public/<str:subdomain>/', public_storefront, name='public_storefront'),
] 