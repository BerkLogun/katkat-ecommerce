from rest_framework import serializers
from .models import Storefront, Theme, StorefrontSettings, Page, Navigation


class ThemeSerializer(serializers.ModelSerializer):
    """Serializer for storefront theme"""
    
    class Meta:
        model = Theme
        fields = '__all__'
        read_only_fields = ('storefront',)


class StorefrontSettingsSerializer(serializers.ModelSerializer):
    """Serializer for storefront settings"""
    
    class Meta:
        model = StorefrontSettings
        fields = '__all__'
        read_only_fields = ('storefront',)


class PageSerializer(serializers.ModelSerializer):
    """Serializer for storefront pages"""
    
    class Meta:
        model = Page
        fields = '__all__'
        read_only_fields = ('storefront',)


class NavigationSerializer(serializers.ModelSerializer):
    """Serializer for storefront navigation"""
    
    class Meta:
        model = Navigation
        fields = '__all__'
        read_only_fields = ('storefront',)


class StorefrontSerializer(serializers.ModelSerializer):
    """Serializer for storefront with nested theme and settings"""
    theme = ThemeSerializer(read_only=True)
    settings = StorefrontSettingsSerializer(read_only=True)
    pages = PageSerializer(many=True, read_only=True)
    navigation = NavigationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Storefront
        fields = '__all__'
        read_only_fields = ('tenant', 'created_at', 'updated_at')
    
    def to_representation(self, instance):
        """Custom representation to map model fields to expected API fields"""
        data = super().to_representation(instance)
        # Map model fields to API fields for backward compatibility
        data['name'] = data.get('store_name', '')
        data['description'] = data.get('store_description', '')
        return data


class CreateStorefrontSerializer(serializers.ModelSerializer):
    """Serializer for creating a new storefront"""
    
    class Meta:
        model = Storefront
        fields = ('store_name', 'store_description', 'logo_url', 'favicon_url', 'meta_title', 'meta_description')


class StorefrontListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing storefronts"""
    theme = ThemeSerializer(read_only=True)
    
    class Meta:
        model = Storefront
        fields = ('id', 'store_name', 'store_description', 'logo_url', 'is_published', 'created_at', 'theme')
    
    def to_representation(self, instance):
        """Custom representation to map model fields to expected API fields"""
        data = super().to_representation(instance)
        # Map model fields to API fields for backward compatibility
        data['name'] = data.get('store_name', '')
        data['description'] = data.get('store_description', '')
        return data 