from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from tenants.models import Tenant
from storefronts.models import Storefront
from orders.models import Order
from products.models import Product


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Get dashboard statistics"""
    try:
        # Get basic counts
        total_tenants = Tenant.objects.count()
        total_storefronts = Storefront.objects.count()
        total_orders = Order.objects.count()
        total_revenue = Order.objects.aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        # Get recent activity counts
        last_7_days = timezone.now() - timedelta(days=7)
        recent_orders = Order.objects.filter(created_at__gte=last_7_days).count()
        recent_tenants = Tenant.objects.filter(created_at__gte=last_7_days).count()

        return Response({
            'total_tenants': total_tenants,
            'total_storefronts': total_storefronts,
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'recent_orders': recent_orders,
            'recent_tenants': recent_tenants,
        })
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_activity(request):
    """Get recent activity data"""
    try:
        # Get recent orders
        recent_orders = Order.objects.order_by('-created_at')[:10]
        orders_data = [{
            'id': str(order.id),
            'order_number': order.order_number,
            'customer_name': order.customer_name or 'Anonymous',
            'total_amount': float(order.total_amount),
            'status': order.status,
            'created_at': order.created_at.isoformat(),
        } for order in recent_orders]

        # Get recent tenants
        recent_tenants = Tenant.objects.order_by('-created_at')[:5]
        tenants_data = [{
            'id': str(tenant.id),
            'name': tenant.name,
            'created_at': tenant.created_at.isoformat(),
        } for tenant in recent_tenants]

        # Get recent storefronts
        recent_storefronts = Storefront.objects.select_related('tenant').order_by('-created_at')[:5]
        storefronts_data = [{
            'id': str(storefront.id),
            'store_name': storefront.store_name,
            'tenant_name': storefront.tenant.name if storefront.tenant else 'Unknown',
            'created_at': storefront.created_at.isoformat(),
        } for storefront in recent_storefronts]

        return Response({
            'recent_orders': orders_data,
            'recent_tenants': tenants_data,
            'recent_storefronts': storefronts_data,
        })
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_health(request):
    """Get system health status"""
    try:
        # Mock health data for now
        health_data = {
            'status': 'healthy',
            'services': {
                'database': {
                    'status': 'ok',
                    'response_time': 15
                },
                'redis': {
                    'status': 'ok',
                    'response_time': 5
                },
                'api': {
                    'status': 'ok',
                    'response_time': 25
                }
            },
            'uptime': 86400,  # 24 hours in seconds
            'memory_usage': 45.2,
            'cpu_usage': 12.8
        }

        return Response(health_data)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
