# KatKat - Multi-Tenant E-commerce Platform

A modern, scalable multi-tenant e-commerce platform built with Next.js, Django, and Docker.

## 🚀 Features

- **Multi-Tenant Architecture**: Isolated tenant environments with schema-based separation
- **Modern Frontend**: Next.js 14 with TypeScript, Tailwind CSS, and TanStack Query
- **Robust Backend**: Django with Django REST Framework and comprehensive API
- **State Management**: Zustand for client state, TanStack Query for server state
- **Real-time Dashboard**: Live statistics, system health monitoring, and activity tracking
- **Storefront Customization**: Theme system, layout options, and feature toggles
- **Secure Authentication**: JWT-based authentication with API key support
- **Background Tasks**: Celery for asynchronous task processing
- **Containerized**: Full Docker support with optimized builds

## 🏗️ Architecture

### Frontend (Next.js)
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS with custom components
- **State Management**: 
  - Zustand for global state (auth, UI)
  - TanStack Query for server state (API caching)
- **API Client**: Custom fetch-based client with authentication

### Backend (Django)
- **Framework**: Django 4.2 with Django REST Framework
- **Database**: PostgreSQL with schema-based tenant isolation
- **Authentication**: JWT with custom User model
- **Background Tasks**: Celery with Redis
- **Multi-tenancy**: Custom middleware for tenant routing

### Services
- **Dashboard**: Next.js admin interface (port 3000)
- **Backend API**: Django REST API (port 8000)
- **Database**: PostgreSQL (port 5432)
- **Cache/Queue**: Redis (port 6379)
- **Background Workers**: Celery workers and beat scheduler
- **Storefront Builder**: Placeholder for future implementation (port 3001)

## 🛠️ Tech Stack

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- TanStack Query
- Zustand
- Lucide React
- Headless UI

### Backend
- Django 4.2
- Django REST Framework
- Django CORS Headers
- Django Tenant Schemas
- Celery
- PostgreSQL
- Redis
- JWT Authentication

### DevOps
- Docker & Docker Compose
- Multi-stage builds
- Environment-based configuration
- Health checks

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Running with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd katkat
   ```

2. **Build and start all services**
   ```bash
   docker compose up --build
   ```

3. **Access the applications**
   - Dashboard: http://localhost:3000
   - Backend API: http://localhost:8000
   - Admin Interface: http://localhost:8000/admin

### Local Development

1. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

2. **Frontend Setup**
   ```bash
   cd dashboard
   npm install
   npm run dev
   ```

## 📁 Project Structure

```
katkat/
├── backend/                 # Django backend
│   ├── core/               # Django settings and configuration
│   ├── tenants/            # Multi-tenancy models and middleware
│   ├── users/              # User management
│   ├── storefronts/        # Storefront customization
│   ├── products/           # Product management
│   ├── orders/             # Order processing
│   └── api/                # API endpoints
├── dashboard/              # Next.js admin dashboard
│   ├── src/
│   │   ├── app/           # Next.js app router
│   │   ├── components/    # Reusable UI components
│   │   ├── lib/           # Utilities and configurations
│   │   │   ├── hooks/     # Custom TanStack Query hooks
│   │   │   ├── stores/    # Zustand stores
│   │   │   └── api.ts     # API client
│   │   └── types/         # TypeScript type definitions
│   └── public/            # Static assets
├── storefront-builder/     # Future storefront builder
├── envs/                   # Environment files
├── docker-compose.yml      # Docker services configuration
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

Create environment files in the `envs/` directory:

**backend.env**
```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=katkat
DB_USER=katkat
DB_PASSWORD=katkat
DB_HOST=db
REDIS_URL=redis://redis:6379/0
```

**dashboard.env**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```

## 🎯 Key Features

### Multi-Tenant Architecture
- Schema-based tenant isolation
- Subdomain-based tenant routing
- API key authentication
- Tenant-specific settings and limits

### Dashboard Features
- Real-time statistics and metrics
- System health monitoring
- Recent activity tracking
- Tenant management interface
- Storefront customization tools

### API Features
- RESTful API with comprehensive endpoints
- JWT authentication
- API key management
- Rate limiting and caching
- Comprehensive error handling

## 🔒 Security

- JWT-based authentication
- API key validation
- CORS configuration
- Tenant isolation
- Input validation and sanitization
- Secure headers and middleware

## 📊 Monitoring

- System health endpoints
- Performance metrics
- Error tracking
- Activity logging
- Database query optimization

## 🚀 Deployment

The project is containerized and ready for deployment:

1. **Production Build**
   ```bash
   docker compose -f docker-compose.prod.yml up --build
   ```

2. **Environment Configuration**
   - Set production environment variables
   - Configure database connections
   - Set up SSL certificates
   - Configure reverse proxy (nginx)

3. **Scaling**
   - Horizontal scaling with Docker Swarm or Kubernetes
   - Database replication
   - Redis clustering
   - Load balancing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code examples

---

**Built with ❤️ using modern web technologies**
