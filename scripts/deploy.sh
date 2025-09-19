#!/bin/bash

# Production Deployment Script for Django Blog Application
# This script handles deployment to production with proper error handling and rollback

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DEPLOY_USER="${DEPLOY_USER:-blogger}"
DEPLOY_HOST="${DEPLOY_HOST:-your-server.com}"
DEPLOY_PATH="${DEPLOY_PATH:-/var/www/blogger}"
BACKUP_PATH="${BACKUP_PATH:-/var/backups/blogger}"
DOCKER_COMPOSE_FILE="${DOCKER_COMPOSE_FILE:-docker-compose.prod.yml}"
SERVICE_NAME="${SERVICE_NAME:-blogger}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Error handling
cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log_error "Deployment failed with exit code $exit_code"
        if [ "${ROLLBACK_ON_FAILURE:-true}" = "true" ]; then
            log_warning "Initiating rollback..."
            rollback_deployment
        fi
    fi
    exit $exit_code
}

trap cleanup EXIT

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if required commands exist
    local required_commands=("docker" "docker-compose" "git" "ssh" "rsync")
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            log_error "Required command '$cmd' not found"
            exit 1
        fi
    done
    
    # Check if .env file exists
    if [ ! -f "$PROJECT_ROOT/.env" ]; then
        log_error ".env file not found. Please create it from .env.example"
        exit 1
    fi
    
    # Check if we can connect to the deployment server
    if ! ssh -o ConnectTimeout=10 "$DEPLOY_USER@$DEPLOY_HOST" "echo 'Connection test successful'" &> /dev/null; then
        log_error "Cannot connect to deployment server $DEPLOY_HOST"
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# Create backup
create_backup() {
    log_info "Creating backup..."
    
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_dir="$BACKUP_PATH/$timestamp"
    
    ssh "$DEPLOY_USER@$DEPLOY_HOST" "
        mkdir -p '$backup_dir'
        if [ -d '$DEPLOY_PATH' ]; then
            cp -r '$DEPLOY_PATH' '$backup_dir/app'
        fi
        
        # Backup database
        if docker ps | grep -q '${SERVICE_NAME}_db'; then
            docker exec ${SERVICE_NAME}_db pg_dump -U blogger blogger > '$backup_dir/database.sql'
        fi
        
        # Keep only last 5 backups
        cd '$BACKUP_PATH'
        ls -t | tail -n +6 | xargs -r rm -rf
    "
    
    echo "$timestamp" > /tmp/backup_timestamp
    log_success "Backup created: $backup_dir"
}

# Deploy application
deploy_application() {
    log_info "Deploying application..."
    
    # Sync files to server
    log_info "Syncing files to server..."
    rsync -avz --delete \
        --exclude='.git' \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        --exclude='.env' \
        --exclude='node_modules' \
        --exclude='media' \
        "$PROJECT_ROOT/" "$DEPLOY_USER@$DEPLOY_HOST:$DEPLOY_PATH/"
    
    # Copy environment file
    scp "$PROJECT_ROOT/.env" "$DEPLOY_USER@$DEPLOY_HOST:$DEPLOY_PATH/.env"
    
    # Deploy with Docker Compose
    ssh "$DEPLOY_USER@$DEPLOY_HOST" "
        cd '$DEPLOY_PATH'
        
        # Pull latest images
        docker-compose -f '$DOCKER_COMPOSE_FILE' pull
        
        # Build application image
        docker-compose -f '$DOCKER_COMPOSE_FILE' build --no-cache web
        
        # Run database migrations
        docker-compose -f '$DOCKER_COMPOSE_FILE' run --rm web python manage.py migrate
        
        # Collect static files
        docker-compose -f '$DOCKER_COMPOSE_FILE' run --rm web python manage.py collectstatic --noinput
        
        # Start services
        docker-compose -f '$DOCKER_COMPOSE_FILE' up -d
        
        # Wait for services to be healthy
        sleep 30
        
        # Check if services are running
        if ! docker-compose -f '$DOCKER_COMPOSE_FILE' ps | grep -q 'Up'; then
            echo 'Services failed to start properly'
            exit 1
        fi
    "
    
    log_success "Application deployed successfully"
}

# Health check
health_check() {
    log_info "Performing health check..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if ssh "$DEPLOY_USER@$DEPLOY_HOST" "curl -f http://localhost/health/ > /dev/null 2>&1"; then
            log_success "Health check passed"
            return 0
        fi
        
        log_info "Health check attempt $attempt/$max_attempts failed, retrying in 10 seconds..."
        sleep 10
        ((attempt++))
    done
    
    log_error "Health check failed after $max_attempts attempts"
    return 1
}

# Rollback deployment
rollback_deployment() {
    log_warning "Rolling back deployment..."
    
    if [ ! -f /tmp/backup_timestamp ]; then
        log_error "No backup timestamp found, cannot rollback"
        return 1
    fi
    
    local backup_timestamp=$(cat /tmp/backup_timestamp)
    local backup_dir="$BACKUP_PATH/$backup_timestamp"
    
    ssh "$DEPLOY_USER@$DEPLOY_HOST" "
        if [ -d '$backup_dir/app' ]; then
            # Stop current services
            cd '$DEPLOY_PATH'
            docker-compose -f '$DOCKER_COMPOSE_FILE' down
            
            # Restore application files
            rm -rf '$DEPLOY_PATH'
            cp -r '$backup_dir/app' '$DEPLOY_PATH'
            
            # Restore database if backup exists
            if [ -f '$backup_dir/database.sql' ]; then
                docker-compose -f '$DOCKER_COMPOSE_FILE' up -d db
                sleep 10
                docker exec -i ${SERVICE_NAME}_db psql -U blogger blogger < '$backup_dir/database.sql'
            fi
            
            # Start services
            docker-compose -f '$DOCKER_COMPOSE_FILE' up -d
        else
            echo 'Backup directory not found: $backup_dir'
            exit 1
        fi
    "
    
    log_success "Rollback completed"
}

# Cleanup old Docker images
cleanup_docker() {
    log_info "Cleaning up old Docker images..."
    
    ssh "$DEPLOY_USER@$DEPLOY_HOST" "
        # Remove unused images
        docker image prune -f
        
        # Remove unused volumes
        docker volume prune -f
        
        # Remove unused networks
        docker network prune -f
    "
    
    log_success "Docker cleanup completed"
}

# Send deployment notification
send_notification() {
    local status=$1
    local message=$2
    
    if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"🚀 Deployment $status: $message\"}" \
            "$SLACK_WEBHOOK_URL" || true
    fi
    
    if [ -n "${DISCORD_WEBHOOK_URL:-}" ]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"content\":\"🚀 Deployment $status: $message\"}" \
            "$DISCORD_WEBHOOK_URL" || true
    fi
}

# Main deployment function
main() {
    local start_time=$(date +%s)
    
    log_info "Starting deployment to $DEPLOY_HOST..."
    send_notification "STARTED" "Deployment to $DEPLOY_HOST initiated"
    
    check_prerequisites
    create_backup
    deploy_application
    
    if health_check; then
        cleanup_docker
        
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        
        log_success "Deployment completed successfully in ${duration}s"
        send_notification "SUCCESS" "Deployment completed successfully in ${duration}s"
    else
        log_error "Deployment failed health check"
        send_notification "FAILED" "Deployment failed health check"
        exit 1
    fi
}

# Script usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help              Show this help message"
    echo "  -e, --environment ENV   Deployment environment (staging|production)"
    echo "  --no-backup            Skip backup creation"
    echo "  --no-rollback          Disable rollback on failure"
    echo "  --dry-run              Show what would be deployed without executing"
    echo ""
    echo "Environment Variables:"
    echo "  DEPLOY_USER            SSH user for deployment (default: blogger)"
    echo "  DEPLOY_HOST            Target deployment host"
    echo "  DEPLOY_PATH            Deployment path on server (default: /var/www/blogger)"
    echo "  BACKUP_PATH            Backup directory (default: /var/backups/blogger)"
    echo "  SLACK_WEBHOOK_URL      Slack webhook for notifications"
    echo "  DISCORD_WEBHOOK_URL    Discord webhook for notifications"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -e|--environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --no-backup)
            SKIP_BACKUP=true
            shift
            ;;
        --no-rollback)
            ROLLBACK_ON_FAILURE=false
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            log_error "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Set environment-specific configurations
if [ "${ENVIRONMENT:-}" = "staging" ]; then
    DEPLOY_HOST="${STAGING_HOST:-staging.yourdomain.com}"
    DOCKER_COMPOSE_FILE="docker-compose.staging.yml"
    SERVICE_NAME="blogger-staging"
elif [ "${ENVIRONMENT:-}" = "production" ]; then
    DEPLOY_HOST="${PRODUCTION_HOST:-yourdomain.com}"
    DOCKER_COMPOSE_FILE="docker-compose.prod.yml"
    SERVICE_NAME="blogger-prod"
fi

# Dry run mode
if [ "${DRY_RUN:-false}" = "true" ]; then
    log_info "DRY RUN MODE - No actual deployment will be performed"
    log_info "Would deploy to: $DEPLOY_HOST"
    log_info "Using compose file: $DOCKER_COMPOSE_FILE"
    log_info "Service name: $SERVICE_NAME"
    exit 0
fi

# Run main deployment
main "$@"