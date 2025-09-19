-- Database initialization script for Django Blog Application
-- This script sets up the database with proper permissions and extensions

-- Create database if it doesn't exist (handled by Docker environment variables)
-- CREATE DATABASE blogger;

-- Connect to the blogger database
\c blogger;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "unaccent";

-- Create additional user for read-only access (optional)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'blogger_readonly') THEN
        CREATE ROLE blogger_readonly;
    END IF;
END
$$;

-- Grant permissions
GRANT CONNECT ON DATABASE blogger TO blogger_readonly;
GRANT USAGE ON SCHEMA public TO blogger_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO blogger_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO blogger_readonly;

-- Create indexes for common queries (will be created by Django migrations, but good to have as reference)
-- These are examples and should match your Django models

-- Example: Index for blog post queries
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_blog_post_published_date ON blog_post(published_date) WHERE is_published = true;
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_blog_post_slug ON blog_post(slug);
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_blog_post_author ON blog_post(author_id);

-- Example: Full-text search index
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_blog_post_search ON blog_post USING gin(to_tsvector('english', title || ' ' || content));

-- Set up database configuration for better performance
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
ALTER SYSTEM SET pg_stat_statements.track = 'all';
ALTER SYSTEM SET log_statement = 'mod';
ALTER SYSTEM SET log_min_duration_statement = 1000;

-- Reload configuration
SELECT pg_reload_conf();

-- Create a health check function
CREATE OR REPLACE FUNCTION health_check()
RETURNS TABLE(status text, timestamp timestamptz) AS $$
BEGIN
    RETURN QUERY SELECT 'healthy'::text, now();
END;
$$ LANGUAGE plpgsql;

-- Grant execute permission on health check function
GRANT EXECUTE ON FUNCTION health_check() TO blogger;
GRANT EXECUTE ON FUNCTION health_check() TO blogger_readonly;

-- Log successful initialization
DO $$
BEGIN
    RAISE NOTICE 'Database initialization completed successfully at %', now();
END
$$;