-- SQL Dump for blog_app with 1000 records
-- Generated for Django blog application
-- Models: PostStatus, Category, Tag, Post

-- Disable foreign key checks for easier insertion
SET foreign_key_checks = 0;

-- ============================================================================
-- PostStatus Data (10 records)
-- ============================================================================

INSERT INTO blog_app_poststatus (id, name, slug, description, icon, color, is_published, is_active, sort_order, created_at, updated_at) VALUES
(1, 'Draft', 'draft', 'Post is being written and not ready for publication', '📝', '#6B7280', 0, 1, 1, '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(2, 'Review', 'review', 'Post is ready for editorial review', '👀', '#F59E0B', 0, 1, 2, '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(3, 'Published', 'published', 'Post is live and publicly visible', '✅', '#10B981', 1, 1, 3, '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(4, 'Scheduled', 'scheduled', 'Post is scheduled for future publication', '⏰', '#3B82F6', 0, 1, 4, '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(5, 'Private', 'private', 'Post is private and only visible to author', '🔒', '#8B5CF6', 0, 1, 5, '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(6, 'Archived', 'archived', 'Post is archived and no longer active', '📦', '#6B7280', 0, 1, 6, '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(7, 'Featured', 'featured', 'Post is featured and highlighted', '⭐', '#EF4444', 1, 1, 7, '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(8, 'Pending', 'pending', 'Post is pending approval', '⏳', '#F97316', 0, 1, 8, '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(9, 'Rejected', 'rejected', 'Post has been rejected and needs revision', '❌', '#DC2626', 0, 1, 9, '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(10, 'Trash', 'trash', 'Post is in trash and will be deleted', '🗑️', '#374151', 0, 0, 10, '2024-01-01 10:00:00', '2024-01-01 10:00:00');

-- ============================================================================
-- Category Data (20 records)
-- ============================================================================

INSERT INTO blog_app_category (id, name, slug, description, created_at, updated_at) VALUES
(1, 'Technology', 'technology', 'Latest trends and insights in technology', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(2, 'Programming', 'programming', 'Programming tutorials, tips, and best practices', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(3, 'Web Development', 'web-development', 'Frontend and backend web development topics', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(4, 'Mobile Development', 'mobile-development', 'iOS, Android, and cross-platform mobile development', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(5, 'Data Science', 'data-science', 'Data analysis, machine learning, and AI topics', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(6, 'DevOps', 'devops', 'Development operations, CI/CD, and infrastructure', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(7, 'Design', 'design', 'UI/UX design, graphic design, and user experience', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(8, 'Business', 'business', 'Business strategies, entrepreneurship, and startups', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(9, 'Career', 'career', 'Career advice, job hunting, and professional development', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(10, 'Tutorials', 'tutorials', 'Step-by-step guides and how-to articles', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(11, 'Reviews', 'reviews', 'Product reviews and comparisons', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(12, 'News', 'news', 'Latest news and updates in tech industry', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(13, 'Open Source', 'open-source', 'Open source projects and contributions', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(14, 'Security', 'security', 'Cybersecurity, privacy, and data protection', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(15, 'Cloud Computing', 'cloud-computing', 'Cloud platforms, services, and architecture', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(16, 'Databases', 'databases', 'Database design, optimization, and management', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(17, 'Testing', 'testing', 'Software testing, QA, and quality assurance', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(18, 'Performance', 'performance', 'Performance optimization and monitoring', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(19, 'Tools', 'tools', 'Development tools, IDEs, and productivity software', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(20, 'Lifestyle', 'lifestyle', 'Work-life balance and developer lifestyle', '2024-01-01 10:00:00', '2024-01-01 10:00:00');

-- ============================================================================
-- Tag Data (50 records)
-- ============================================================================

INSERT INTO blog_app_tag (id, name, slug, created_at) VALUES
(1, 'Python', 'python', '2024-01-01 10:00:00'),
(2, 'JavaScript', 'javascript', '2024-01-01 10:00:00'),
(3, 'React', 'react', '2024-01-01 10:00:00'),
(4, 'Django', 'django', '2024-01-01 10:00:00'),
(5, 'Node.js', 'nodejs', '2024-01-01 10:00:00'),
(6, 'TypeScript', 'typescript', '2024-01-01 10:00:00'),
(7, 'Vue.js', 'vuejs', '2024-01-01 10:00:00'),
(8, 'Angular', 'angular', '2024-01-01 10:00:00'),
(9, 'CSS', 'css', '2024-01-01 10:00:00'),
(10, 'HTML', 'html', '2024-01-01 10:00:00'),
(11, 'Machine Learning', 'machine-learning', '2024-01-01 10:00:00'),
(12, 'AI', 'ai', '2024-01-01 10:00:00'),
(13, 'Docker', 'docker', '2024-01-01 10:00:00'),
(14, 'Kubernetes', 'kubernetes', '2024-01-01 10:00:00'),
(15, 'AWS', 'aws', '2024-01-01 10:00:00'),
(16, 'Azure', 'azure', '2024-01-01 10:00:00'),
(17, 'Google Cloud', 'google-cloud', '2024-01-01 10:00:00'),
(18, 'PostgreSQL', 'postgresql', '2024-01-01 10:00:00'),
(19, 'MongoDB', 'mongodb', '2024-01-01 10:00:00'),
(20, 'Redis', 'redis', '2024-01-01 10:00:00'),
(21, 'GraphQL', 'graphql', '2024-01-01 10:00:00'),
(22, 'REST API', 'rest-api', '2024-01-01 10:00:00'),
(23, 'Microservices', 'microservices', '2024-01-01 10:00:00'),
(24, 'Serverless', 'serverless', '2024-01-01 10:00:00'),
(25, 'Git', 'git', '2024-01-01 10:00:00'),
(26, 'GitHub', 'github', '2024-01-01 10:00:00'),
(27, 'CI/CD', 'cicd', '2024-01-01 10:00:00'),
(28, 'Testing', 'testing', '2024-01-01 10:00:00'),
(29, 'TDD', 'tdd', '2024-01-01 10:00:00'),
(30, 'Agile', 'agile', '2024-01-01 10:00:00'),
(31, 'Scrum', 'scrum', '2024-01-01 10:00:00'),
(32, 'Performance', 'performance', '2024-01-01 10:00:00'),
(33, 'Security', 'security', '2024-01-01 10:00:00'),
(34, 'Authentication', 'authentication', '2024-01-01 10:00:00'),
(35, 'Authorization', 'authorization', '2024-01-01 10:00:00'),
(36, 'JWT', 'jwt', '2024-01-01 10:00:00'),
(37, 'OAuth', 'oauth', '2024-01-01 10:00:00'),
(38, 'HTTPS', 'https', '2024-01-01 10:00:00'),
(39, 'SSL', 'ssl', '2024-01-01 10:00:00'),
(40, 'Encryption', 'encryption', '2024-01-01 10:00:00'),
(41, 'Mobile', 'mobile', '2024-01-01 10:00:00'),
(42, 'iOS', 'ios', '2024-01-01 10:00:00'),
(43, 'Android', 'android', '2024-01-01 10:00:00'),
(44, 'React Native', 'react-native', '2024-01-01 10:00:00'),
(45, 'Flutter', 'flutter', '2024-01-01 10:00:00'),
(46, 'Swift', 'swift', '2024-01-01 10:00:00'),
(47, 'Kotlin', 'kotlin', '2024-01-01 10:00:00'),
(48, 'Java', 'java', '2024-01-01 10:00:00'),
(49, 'C#', 'csharp', '2024-01-01 10:00:00'),
(50, 'Go', 'go', '2024-01-01 10:00:00');

-- ============================================================================
-- Post Data (920 records to reach 1000 total)
-- ============================================================================

-- Sample posts with realistic content
INSERT INTO blog_app_post (id, title, slug, author_id, content, excerpt, category_id, status_id, featured_image, meta_description, created_at, updated_at, published_at) VALUES