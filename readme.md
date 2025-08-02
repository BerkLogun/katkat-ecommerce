# KatKat - Multi-Tenant E-commerce Platform

A comprehensive, fully customizable multi-tenant e-commerce platform where each tenant gets their own isolated environment with complete control over their storefront design, features, and branding.

## 🚀 Features

### Multi-Tenancy
- **Isolated Environments**: Each tenant has their own database schema, products, orders, and configurations
- **API Key Authentication**: Secure tenant identification using API keys
- **Subdomain Routing**: Automatic tenant detection via subdomains (e.g., `teststore.localhost:3000`)
- **Complete Data Isolation**: Tenants cannot see or access each other's data

### Storefront Builder
- **Visual Theme Editor**: Real-time color scheme customization with color pickers
- **Layout Options**: Choose from Grid, List, or Masonry product layouts
- **Feature Toggles**: Enable/disable search, filters, wishlist, reviews, and more
- **Custom Branding**: Upload logos, favicons, and customize store information
- **SEO Optimization**: Meta titles, descriptions, and keywords for each store
- **Analytics Integration**: Google Analytics and Facebook Pixel support
- **Custom Code**: Inject custom CSS and JavaScript for advanced customization
- **Live Preview**: See changes instantly in a real-time preview

### E-commerce Features
- **Product Management**: Full CRUD operations for products with images, descriptions, and pricing
- **Inventory Management**: Track stock levels with automatic updates
- **Shopping Cart**: Persistent cart with quantity management
- **Checkout System**: Guest checkout with customer information collection
- **Order Management**: Complete order lifecycle with status tracking
- **Statistics Dashboard**: Revenue, sales, and product performance analytics

### Technical Architecture
- **Django Backend**: Robust API with multi-tenant middleware
- **PostgreSQL**: Multi-schema database design for tenant isolation
- **Docker Compose**: Easy deployment and development setup
- **Nginx**: Static file serving and subdomain routing
- **Redis**: Caching layer for improved performance

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Dashboard     │    │   Storefront    │    │   Backend API   │
│   (Port 9000)   │    │   (Port 3000)   │    │   (Port 8000)   │
│                 │    │                 │    │                 │
│ • Store Builder │    │ • Dynamic UI    │    │ • Multi-tenant  │
│ • Admin Panel   │    │ • Shopping Cart │    │ • API Keys      │
│ • Analytics     │    │ • Checkout      │    │ • Products      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    │   (Port 5432)   │
                    │                 │
                    │ • Public Schema │
                    │ • Tenant Schemas│
                    │ • Multi-tenancy │
                    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd katkat
   ```

2. **Start the services**
   ```bash
   docker compose up -d
   ```

3. **Access the platform**
   - **Dashboard**: http://localhost:9000
   - **Storefront Builder**: http://localhost:9000/builder.html
   - **Admin Dashboard**: http://localhost:9000/admin.html
   - **API Documentation**: http://localhost:8000

### Creating Your First Tenant

1. **Access the Dashboard**
   - Go to http://localhost:9000
   - Click "Create New Tenant"

2. **Configure Your Store**
   - Enter store name and domain
   - The system will create an isolated environment

3. **Customize Your Storefront**
   - Go to http://localhost:9000/builder.html
   - Use the visual builder to customize:
     - Colors and themes
     - Layout and features
     - Branding and content
     - SEO settings
     - Analytics integration

4. **Access Your Store**
   - Your store will be available at: `http://[your-tenant].localhost:3000/dynamic-storefront.html`
   - Example: `http://teststore.localhost:3000/dynamic-storefront.html`

## 🎨 Storefront Builder Features

### General Settings
- **Store Information**: Name, description, logo, favicon
- **Contact Details**: Email, phone, address
- **Social Media**: Facebook, Twitter, Instagram, LinkedIn links

### Theme Customization
- **Color Scheme**: Primary, secondary, accent, background, and text colors
- **Layout Options**: Grid, List, or Masonry product displays
- **Product Display**: Show/hide images, prices, descriptions
- **Pagination**: Configure products per page

### Feature Management
- **Search Functionality**: Enable/disable product search
- **Filters & Sorting**: Product filtering and sorting options
- **Wishlist**: Save favorite products
- **Product Reviews**: Customer reviews and ratings
- **Related Products**: Cross-selling recommendations

### Checkout Settings
- **Guest Checkout**: Allow purchases without account creation
- **Account Requirements**: Force customer registration
- **Coupon Codes**: Discount functionality
- **Gift Cards**: Gift card purchase options

### Advanced Features
- **SEO Optimization**: Meta titles, descriptions, keywords
- **Analytics**: Google Analytics and Facebook Pixel integration
- **Custom Code**: CSS and JavaScript injection for advanced customization

## 🔧 API Endpoints

### Tenant Management
- `POST /api/management/tenants/create/` - Create new tenant
- `GET /api/management/tenants/` - List all tenants
- `POST /api/management/keys/generate/` - Generate API key
- `GET /api/management/tenants/{tenant}/keys/` - List tenant API keys
- `DELETE /api/management/keys/{key_id}/revoke/` - Revoke API key

### Storefront Configuration
- `GET /api/storefront/config/` - Get storefront configuration
- `PUT /api/storefront/config/update/` - Update storefront configuration
- `GET /api/storefront/products/` - Get products with tenant-specific settings
- `POST /api/storefront/orders/create/` - Create order with tenant-specific checkout

### Product Management
- `GET /api/products/` - List products
- `POST /api/products/create/` - Create product
- `PUT /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/delete/` - Delete product

### Order Management
- `GET /api/orders/` - List orders
- `POST /api/orders/create/` - Create order
- `PUT /api/orders/{id}/status/` - Update order status

### Analytics
- `GET /api/statistics/` - Get store statistics (revenue, orders, top products)

## 🗄️ Database Schema

### Public Schema (Shared)
- `tenants` - Tenant information and configuration
- `api_keys` - API key management and validation

### Tenant Schemas (Isolated)
- `products` - Product catalog with images, prices, stock
- `orders` - Order management with status tracking
- `order_items` - Order line items with quantities and prices
- `tenant_storefronts` - Storefront customization settings

## 🔐 Security Features

- **API Key Authentication**: Secure tenant identification
- **Schema Isolation**: Complete data separation between tenants
- **CORS Configuration**: Proper cross-origin request handling
- **Input Validation**: Server-side validation for all inputs
- **SQL Injection Protection**: Parameterized queries

## 🎯 Use Cases

### E-commerce Agencies
- Manage multiple client stores from a single platform
- Provide white-label solutions with custom branding
- Offer different feature sets based on client needs

### Multi-Brand Companies
- Separate product catalogs for different brands
- Custom storefronts for each brand identity
- Centralized order and inventory management

### SaaS Platforms
- Provide e-commerce capabilities to SaaS customers
- Isolated environments for each customer
- Customizable storefronts without technical knowledge

### Marketplace Operators
- Allow vendors to create their own storefronts
- Maintain brand consistency while enabling customization
- Scale to hundreds or thousands of stores

## 🛠️ Development

### Local Development
```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Rebuild services
docker compose up -d --build

# Access database
docker exec -it katkat-db-1 psql -U saleor -d saleor
```

### Adding New Features
1. **Backend**: Add models in `saleor/django_project/models.py`
2. **API**: Create endpoints in `saleor/django_project/api.py`
3. **Frontend**: Update storefront templates and builder
4. **Database**: Run migrations or create tables manually

### Customization
- **Themes**: Modify CSS variables in the dynamic storefront
- **Features**: Add new feature toggles in the builder
- **API**: Extend API endpoints for new functionality
- **Database**: Add new tables to tenant schemas

## 📊 Performance

- **Database Optimization**: Indexed queries for fast product searches
- **Caching**: Redis integration for improved response times
- **Static Assets**: Nginx serving for fast frontend delivery
- **Lazy Loading**: Products loaded on-demand with pagination
- **CDN Ready**: Static assets can be served from CDN

## 🔄 Deployment

### Production Setup
1. **Environment Variables**: Configure production settings
2. **SSL Certificates**: Set up HTTPS for secure transactions
3. **Database Backup**: Implement automated backup strategy
4. **Monitoring**: Add application and database monitoring
5. **Scaling**: Configure load balancers and multiple instances

### Docker Production
```bash
# Build production images
docker compose -f docker-compose.prod.yml build

# Deploy to production
docker compose -f docker-compose.prod.yml up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the API endpoints

## 🎉 What's Next?

- **Mobile App**: Native mobile applications for storefronts
- **Advanced Analytics**: Detailed reporting and insights
- **Payment Integration**: Multiple payment gateway support
- **Inventory Management**: Advanced stock tracking and alerts
- **Marketing Tools**: Email campaigns and promotions
- **Multi-language**: Internationalization support
- **Advanced Customization**: Drag-and-drop page builder
- **API Marketplace**: Third-party integrations and plugins

---

**Built with ❤️ for scalable, customizable e-commerce solutions**
