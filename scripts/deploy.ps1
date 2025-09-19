# Production Deployment Script for Django Blog Application (PowerShell)
# This script handles deployment to production with proper error handling and rollback

param(
    [string]$Environment = "",
    [switch]$NoBackup = $false,
    [switch]$NoRollback = $false,
    [switch]$DryRun = $false,
    [switch]$Help = $false
)

# Configuration
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$DeployUser = $env:DEPLOY_USER ?? "blogger"
$DeployHost = $env:DEPLOY_HOST ?? "your-server.com"
$DeployPath = $env:DEPLOY_PATH ?? "/var/www/blogger"
$BackupPath = $env:BACKUP_PATH ?? "/var/backups/blogger"
$DockerComposeFile = $env:DOCKER_COMPOSE_FILE ?? "docker-compose.prod.yml"
$ServiceName = $env:SERVICE_NAME ?? "blogger"

# Error handling
$ErrorActionPreference = "Stop"

# Logging functions
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Show usage information
function Show-Usage {
    Write-Host "Usage: .\deploy.ps1 [OPTIONS]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Environment ENV       Deployment environment (staging|production)"
    Write-Host "  -NoBackup              Skip backup creation"
    Write-Host "  -NoRollback            Disable rollback on failure"
    Write-Host "  -DryRun                Show what would be deployed without executing"
    Write-Host "  -Help                  Show this help message"
    Write-Host ""
    Write-Host "Environment Variables:"
    Write-Host "  DEPLOY_USER            SSH user for deployment (default: blogger)"
    Write-Host "  DEPLOY_HOST            Target deployment host"
    Write-Host "  DEPLOY_PATH            Deployment path on server (default: /var/www/blogger)"
    Write-Host "  BACKUP_PATH            Backup directory (default: /var/backups/blogger)"
    Write-Host "  SLACK_WEBHOOK_URL      Slack webhook for notifications"
    Write-Host "  DISCORD_WEBHOOK_URL    Discord webhook for notifications"
}

# Check prerequisites
function Test-Prerequisites {
    Write-Info "Checking prerequisites..."
    
    # Check if required commands exist
    $RequiredCommands = @("docker", "docker-compose", "git", "ssh", "scp")
    foreach ($cmd in $RequiredCommands) {
        if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
            Write-Error "Required command '$cmd' not found"
            exit 1
        }
    }
    
    # Check if .env file exists
    $EnvFile = Join-Path $ProjectRoot ".env"
    if (-not (Test-Path $EnvFile)) {
        Write-Error ".env file not found. Please create it from .env.example"
        exit 1
    }
    
    # Check if we can connect to the deployment server
    try {
        $TestConnection = ssh -o ConnectTimeout=10 "$DeployUser@$DeployHost" "echo 'Connection test successful'" 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "Connection failed"
        }
    }
    catch {
        Write-Error "Cannot connect to deployment server $DeployHost"
        exit 1
    }
    
    Write-Success "Prerequisites check passed"
}

# Create backup
function New-Backup {
    Write-Info "Creating backup..."
    
    $Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $BackupDir = "$BackupPath/$Timestamp"
    
    $BackupScript = @"
        mkdir -p '$BackupDir'
        if [ -d '$DeployPath' ]; then
            cp -r '$DeployPath' '$BackupDir/app'
        fi
        
        # Backup database
        if docker ps | grep -q '${ServiceName}_db'; then
            docker exec ${ServiceName}_db pg_dump -U blogger blogger > '$BackupDir/database.sql'
        fi
        
        # Keep only last 5 backups
        cd '$BackupPath'
        ls -t | tail -n +6 | xargs -r rm -rf
"@
    
    ssh "$DeployUser@$DeployHost" $BackupScript
    
    $Timestamp | Out-File -FilePath "$env:TEMP\backup_timestamp.txt" -Encoding UTF8
    Write-Success "Backup created: $BackupDir"
}

# Deploy application
function Deploy-Application {
    Write-Info "Deploying application..."
    
    # Sync files to server using scp (since rsync might not be available on Windows)
    Write-Info "Syncing files to server..."
    
    # Create a temporary archive
    $TempArchive = "$env:TEMP\blogger_deploy.tar.gz"
    $ExcludeFile = "$env:TEMP\exclude.txt"
    
    # Create exclude file
    @(
        ".git",
        "__pycache__",
        "*.pyc",
        ".env",
        "node_modules",
        "media"
    ) | Out-File -FilePath $ExcludeFile -Encoding UTF8
    
    # Create archive (requires tar command or 7-zip)
    if (Get-Command tar -ErrorAction SilentlyContinue) {
        tar -czf $TempArchive -C $ProjectRoot --exclude-from=$ExcludeFile .
    } else {
        Write-Error "tar command not found. Please install Git for Windows or use WSL."
        exit 1
    }
    
    # Copy archive to server and extract
    scp $TempArchive "$DeployUser@${DeployHost}:/tmp/blogger_deploy.tar.gz"
    scp "$ProjectRoot\.env" "$DeployUser@${DeployHost}:$DeployPath/.env"
    
    $DeployScript = @"
        mkdir -p '$DeployPath'
        cd '$DeployPath'
        tar -xzf /tmp/blogger_deploy.tar.gz
        rm /tmp/blogger_deploy.tar.gz
        
        # Pull latest images
        docker-compose -f '$DockerComposeFile' pull
        
        # Build application image
        docker-compose -f '$DockerComposeFile' build --no-cache web
        
        # Run database migrations
        docker-compose -f '$DockerComposeFile' run --rm web python manage.py migrate
        
        # Collect static files
        docker-compose -f '$DockerComposeFile' run --rm web python manage.py collectstatic --noinput
        
        # Start services
        docker-compose -f '$DockerComposeFile' up -d
        
        # Wait for services to be healthy
        sleep 30
        
        # Check if services are running
        if ! docker-compose -f '$DockerComposeFile' ps | grep -q 'Up'; then
            echo 'Services failed to start properly'
            exit 1
        fi
"@
    
    ssh "$DeployUser@$DeployHost" $DeployScript
    
    # Cleanup temporary files
    Remove-Item $TempArchive -ErrorAction SilentlyContinue
    Remove-Item $ExcludeFile -ErrorAction SilentlyContinue
    
    Write-Success "Application deployed successfully"
}

# Health check
function Test-Health {
    Write-Info "Performing health check..."
    
    $MaxAttempts = 30
    $Attempt = 1
    
    while ($Attempt -le $MaxAttempts) {
        try {
            $HealthCheck = ssh "$DeployUser@$DeployHost" "curl -f http://localhost/health/ > /dev/null 2>&1"
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Health check passed"
                return $true
            }
        }
        catch {
            # Continue to retry
        }
        
        Write-Info "Health check attempt $Attempt/$MaxAttempts failed, retrying in 10 seconds..."
        Start-Sleep -Seconds 10
        $Attempt++
    }
    
    Write-Error "Health check failed after $MaxAttempts attempts"
    return $false
}

# Rollback deployment
function Restore-Deployment {
    Write-Warning "Rolling back deployment..."
    
    $BackupTimestampFile = "$env:TEMP\backup_timestamp.txt"
    if (-not (Test-Path $BackupTimestampFile)) {
        Write-Error "No backup timestamp found, cannot rollback"
        return $false
    }
    
    $BackupTimestamp = Get-Content $BackupTimestampFile -Raw
    $BackupTimestamp = $BackupTimestamp.Trim()
    $BackupDir = "$BackupPath/$BackupTimestamp"
    
    $RollbackScript = @"
        if [ -d '$BackupDir/app' ]; then
            # Stop current services
            cd '$DeployPath'
            docker-compose -f '$DockerComposeFile' down
            
            # Restore application files
            rm -rf '$DeployPath'
            cp -r '$BackupDir/app' '$DeployPath'
            
            # Restore database if backup exists
            if [ -f '$BackupDir/database.sql' ]; then
                docker-compose -f '$DockerComposeFile' up -d db
                sleep 10
                docker exec -i ${ServiceName}_db psql -U blogger blogger < '$BackupDir/database.sql'
            fi
            
            # Start services
            docker-compose -f '$DockerComposeFile' up -d
        else
            echo 'Backup directory not found: $BackupDir'
            exit 1
        fi
"@
    
    ssh "$DeployUser@$DeployHost" $RollbackScript
    
    Write-Success "Rollback completed"
    return $true
}

# Cleanup old Docker images
function Remove-UnusedDockerResources {
    Write-Info "Cleaning up old Docker images..."
    
    $CleanupScript = @"
        # Remove unused images
        docker image prune -f
        
        # Remove unused volumes
        docker volume prune -f
        
        # Remove unused networks
        docker network prune -f
"@
    
    ssh "$DeployUser@$DeployHost" $CleanupScript
    
    Write-Success "Docker cleanup completed"
}

# Send deployment notification
function Send-Notification {
    param(
        [string]$Status,
        [string]$Message
    )
    
    if ($env:SLACK_WEBHOOK_URL) {
        try {
            $Body = @{ text = "🚀 Deployment $Status`: $Message" } | ConvertTo-Json
            Invoke-RestMethod -Uri $env:SLACK_WEBHOOK_URL -Method Post -Body $Body -ContentType "application/json"
        }
        catch {
            # Ignore notification failures
        }
    }
    
    if ($env:DISCORD_WEBHOOK_URL) {
        try {
            $Body = @{ content = "🚀 Deployment $Status`: $Message" } | ConvertTo-Json
            Invoke-RestMethod -Uri $env:DISCORD_WEBHOOK_URL -Method Post -Body $Body -ContentType "application/json"
        }
        catch {
            # Ignore notification failures
        }
    }
}

# Main deployment function
function Start-Deployment {
    $StartTime = Get-Date
    
    Write-Info "Starting deployment to $DeployHost..."
    Send-Notification "STARTED" "Deployment to $DeployHost initiated"
    
    try {
        Test-Prerequisites
        
        if (-not $NoBackup) {
            New-Backup
        }
        
        Deploy-Application
        
        if (Test-Health) {
            Remove-UnusedDockerResources
            
            $EndTime = Get-Date
            $Duration = [math]::Round(($EndTime - $StartTime).TotalSeconds)
            
            Write-Success "Deployment completed successfully in ${Duration}s"
            Send-Notification "SUCCESS" "Deployment completed successfully in ${Duration}s"
        } else {
            Write-Error "Deployment failed health check"
            Send-Notification "FAILED" "Deployment failed health check"
            
            if (-not $NoRollback) {
                Restore-Deployment
            }
            
            exit 1
        }
    }
    catch {
        Write-Error "Deployment failed: $($_.Exception.Message)"
        Send-Notification "FAILED" "Deployment failed: $($_.Exception.Message)"
        
        if (-not $NoRollback) {
            Restore-Deployment
        }
        
        exit 1
    }
}

# Main script logic
if ($Help) {
    Show-Usage
    exit 0
}

# Set environment-specific configurations
if ($Environment -eq "staging") {
    $DeployHost = $env:STAGING_HOST ?? "staging.yourdomain.com"
    $DockerComposeFile = "docker-compose.staging.yml"
    $ServiceName = "blogger-staging"
} elseif ($Environment -eq "production") {
    $DeployHost = $env:PRODUCTION_HOST ?? "yourdomain.com"
    $DockerComposeFile = "docker-compose.prod.yml"
    $ServiceName = "blogger-prod"
}

# Dry run mode
if ($DryRun) {
    Write-Info "DRY RUN MODE - No actual deployment will be performed"
    Write-Info "Would deploy to: $DeployHost"
    Write-Info "Using compose file: $DockerComposeFile"
    Write-Info "Service name: $ServiceName"
    exit 0
}

# Run main deployment
Start-Deployment