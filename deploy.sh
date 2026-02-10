#!/bin/bash

# ============================================================
# NUROTHON AI SMB - PRODUCTION DEPLOYMENT SCRIPT
# ============================================================

set -e  # Exit on error

echo "============================================================"
echo "🚀 NUROTHON AI SMB - PRODUCTION DEPLOYMENT"
echo "============================================================"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker and Docker Compose are installed${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.production...${NC}"
    cp .env.production .env
    echo -e "${YELLOW}⚠️  Please edit .env file and update production values!${NC}"
    echo -e "${YELLOW}⚠️  Press Enter to continue or Ctrl+C to abort...${NC}"
    read
fi

echo -e "${GREEN}✅ Environment file found${NC}"

# Build and start containers
echo ""
echo "============================================================"
echo "📦 BUILDING DOCKER IMAGES"
echo "============================================================"

docker-compose -f docker-compose.prod.yml build

echo ""
echo "============================================================"
echo "🚀 STARTING CONTAINERS"
echo "============================================================"

docker-compose -f docker-compose.prod.yml up -d

echo ""
echo "============================================================"
echo "⏳ WAITING FOR SERVICES TO BE HEALTHY"
echo "============================================================"

# Wait for database
echo "Waiting for database..."
timeout 60 bash -c 'until docker-compose -f docker-compose.prod.yml exec -T database pg_isready -U nurothon_user; do sleep 2; done' || {
    echo -e "${RED}❌ Database failed to start${NC}"
    docker-compose -f docker-compose.prod.yml logs database
    exit 1
}
echo -e "${GREEN}✅ Database is ready${NC}"

# Wait for backend
echo "Waiting for backend..."
timeout 90 bash -c 'until curl -f http://localhost:8000/health; do sleep 3; done' || {
    echo -e "${RED}❌ Backend failed to start${NC}"
    docker-compose -f docker-compose.prod.yml logs backend
    exit 1
}
echo -e "${GREEN}✅ Backend is ready${NC}"

# Wait for frontend
echo "Waiting for frontend..."
timeout 30 bash -c 'until curl -f http://localhost/; do sleep 2; done' || {
    echo -e "${RED}❌ Frontend failed to start${NC}"
    docker-compose -f docker-compose.prod.yml logs frontend
    exit 1
}
echo -e "${GREEN}✅ Frontend is ready${NC}"

echo ""
echo "============================================================"
echo "🎉 DEPLOYMENT SUCCESSFUL!"
echo "============================================================"
echo ""
echo "📊 Service URLs:"
echo "   Frontend:  http://localhost"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo "   Database:  localhost:5432"
echo ""
echo "📝 Useful Commands:"
echo "   View logs:        docker-compose -f docker-compose.prod.yml logs -f"
echo "   Stop services:    docker-compose -f docker-compose.prod.yml down"
echo "   Restart:          docker-compose -f docker-compose.prod.yml restart"
echo "   View status:      docker-compose -f docker-compose.prod.yml ps"
echo ""
echo "🔒 Security Reminder:"
echo "   - Update SECRET_KEY in .env"
echo "   - Update POSTGRES_PASSWORD in .env"
echo "   - Configure ALLOWED_ORIGINS for your domain"
echo ""
echo "============================================================"
