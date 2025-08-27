# TalentScout Docker Containerization Guide

This guide explains how to containerize and deploy the TalentScout Hiring Assistant application using Docker.

## 🐳 Overview

The application is containerized with the following components:
- **Main App**: Streamlit application (Python 3.11)
- **Database**: MongoDB 7.0 with authentication
- **Web Interface**: MongoDB Express for database management
- **Reverse Proxy**: Nginx with SSL support (optional)
- **Cache**: Redis for performance optimization (optional)

## 📁 Project Structure

```
d:\internship\
├── Dockerfile                 # Main application container
├── docker-compose.yml         # Development environment
├── docker-compose.prod.yml    # Production environment
├── .dockerignore             # Files to exclude from build
├── env.example               # Environment variables template
├── nginx/                    # Nginx configuration
│   └── nginx.conf
├── mongo-init/               # MongoDB initialization
│   └── init.js
├── scripts/                  # Automation scripts
│   ├── build.sh
│   └── deploy.sh
└── README-Docker.md          # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Docker Desktop** installed and running
2. **Docker Compose** (included with Docker Desktop)
3. **Git** for cloning the repository

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd internship

# Copy environment template
cp env.example .env

# Edit .env file with your configuration
# Especially GROQ_API_KEY and MongoDB credentials
```

### 2. Build and Run (Development)

```bash
# Make scripts executable (Linux/Mac)
chmod +x scripts/*.sh

# Build and start services
./scripts/build.sh

# Or manually:
docker-compose up -d --build
```

### 3. Access the Application

- **Main App**: http://localhost:8501
- **MongoDB Express**: http://localhost:8081
- **MongoDB**: localhost:27017

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `env.example`:

```bash
# Application Configuration
APP_TITLE=TalentScout Hiring Assistant
APP_ICON=🤖
PAGE_LAYOUT=wide

# API Keys
GROQ_API_KEY=your_actual_groq_api_key

# MongoDB Configuration
MONGODB_URI=mongodb://admin:password@mongodb:27017/interview_db?authSource=admin
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=your_secure_password

# MongoDB Express
MONGO_EXPRESS_USERNAME=admin
MONGO_EXPRESS_PASSWORD=your_secure_password

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### MongoDB Credentials

**Important**: Change the default MongoDB credentials in production:

```bash
MONGO_ROOT_USERNAME=your_admin_username
MONGO_ROOT_PASSWORD=your_secure_password
MONGO_EXPRESS_USERNAME=your_express_username
MONGO_EXPRESS_PASSWORD=your_express_password
```

## 🏗️ Development vs Production

### Development Environment (`docker-compose.yml`)

- Single MongoDB instance
- Basic configuration
- All ports exposed for debugging
- No SSL/HTTPS
- No resource limits

### Production Environment (`docker-compose.prod.yml`)

- Enhanced security
- Resource limits and reservations
- SSL/HTTPS with Nginx
- Redis caching
- Log rotation
- Health checks
- Backup capabilities

## 📊 Production Deployment

### 1. Prepare Production Environment

```bash
# Create production environment file
cp env.example .env.prod

# Edit with production values
nano .env.prod

# Set production environment
export $(cat .env.prod | xargs)
```

### 2. Deploy to Production

```bash
# Deploy using production script
./scripts/deploy.sh

# Or manually:
docker-compose -f docker-compose.prod.yml up -d --build
```

### 3. Production Features

- **SSL/HTTPS**: Automatic HTTP to HTTPS redirect
- **Rate Limiting**: API protection against abuse
- **Security Headers**: XSS protection, CSRF prevention
- **Resource Management**: CPU and memory limits
- **Monitoring**: Health checks and logging
- **Backup**: Automatic MongoDB backups

## 🛠️ Management Commands

### View Status

```bash
# Development
docker-compose ps

# Production
docker-compose -f docker-compose.prod.yml ps
```

### View Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs app

# Follow logs
docker-compose logs -f app
```

### Stop Services

```bash
# Development
docker-compose down

# Production
docker-compose -f docker-compose.prod.yml down
```

### Restart Services

```bash
# Development
docker-compose restart

# Production
docker-compose -f docker-compose.prod.yml restart
```

### Update Application

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose up -d --build
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Port Already in Use

```bash
# Check what's using the port
netstat -tulpn | grep :8501

# Kill the process or change port in docker-compose.yml
```

#### 2. MongoDB Connection Issues

```bash
# Check MongoDB container status
docker-compose ps mongodb

# View MongoDB logs
docker-compose logs mongodb

# Test connection
docker exec talentscout-mongodb mongosh --eval "db.adminCommand('ping')"
```

#### 3. Application Won't Start

```bash
# Check application logs
docker-compose logs app

# Verify environment variables
docker-compose exec app env | grep GROQ_API_KEY

# Check if GROQ_API_KEY is set
```

#### 4. Permission Issues

```bash
# Fix script permissions
chmod +x scripts/*.sh

# Check Docker permissions
docker ps
```

### Health Checks

The application includes built-in health checks:

```bash
# Application health
curl http://localhost:8501/_stcore/health

# Nginx health (production)
curl http://localhost/health

# MongoDB health
docker exec talentscout-mongodb mongosh --eval "db.adminCommand('ping')"
```

## 📈 Monitoring and Logs

### Log Management

```bash
# View real-time logs
docker-compose logs -f

# Export logs to file
docker-compose logs > app.log

# View specific service logs
docker-compose logs app > app.log
docker-compose logs mongodb > mongodb.log
```

### Performance Monitoring

```bash
# Container resource usage
docker stats

# Specific container stats
docker stats talentscout-app
```

## 🔒 Security Considerations

### Production Security

1. **Change Default Passwords**: Update all default credentials
2. **Network Security**: Use internal Docker networks
3. **SSL Certificates**: Use valid SSL certificates in production
4. **Firewall**: Restrict access to necessary ports only
5. **Regular Updates**: Keep Docker images updated

### Environment Variables

- Never commit `.env` files to version control
- Use strong, unique passwords
- Rotate API keys regularly
- Use secrets management in production

## 📚 Additional Resources

### Docker Commands Reference

```bash
# Build image
docker build -t talentscout:latest .

# Run container
docker run -p 8501:8501 talentscout:latest

# Execute commands in running container
docker exec -it talentscout-app bash

# View container details
docker inspect talentscout-app
```

### Useful Scripts

- `./scripts/build.sh`: Development build and start
- `./scripts/deploy.sh`: Production deployment
- `./scripts/build.sh --logs`: View application logs
- `./scripts/build.sh --status`: Check service status

## 🤝 Support

If you encounter issues:

1. Check the logs: `docker-compose logs`
2. Verify environment variables
3. Ensure Docker is running
4. Check port availability
5. Review this documentation

## 📝 Changelog

- **v1.0.0**: Initial Docker containerization
- Added development and production environments
- MongoDB integration with authentication
- Nginx reverse proxy with SSL support
- Automated build and deployment scripts
- Health checks and monitoring
- Backup and rollback capabilities
