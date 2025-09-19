#!/usr/bin/env python3
"""
Generate SQL dump for blog_app with 1000 records.
This script creates realistic sample data for the Django blog application.
"""

import random
from datetime import datetime, timedelta
from typing import List, Tuple

# Sample data for generating realistic content
SAMPLE_TITLES = [
    "Getting Started with Python Web Development",
    "Advanced JavaScript Techniques for Modern Web Apps",
    "Building Scalable React Applications",
    "Django Best Practices for Production",
    "Introduction to Machine Learning with Python",
    "Docker Containerization for Beginners",
    "Kubernetes Deployment Strategies",
    "AWS Cloud Architecture Patterns",
    "Database Optimization Techniques",
    "RESTful API Design Principles",
    "GraphQL vs REST: Which to Choose?",
    "Microservices Architecture Guide",
    "CI/CD Pipeline Implementation",
    "Test-Driven Development in Practice",
    "Security Best Practices for Web Applications",
    "Performance Optimization Strategies",
    "Mobile App Development with React Native",
    "Flutter vs React Native Comparison",
    "iOS Development with Swift",
    "Android Development Best Practices",
    "Data Science with Python and Pandas",
    "Machine Learning Model Deployment",
    "Deep Learning Fundamentals",
    "Natural Language Processing Basics",
    "Computer Vision Applications",
    "Blockchain Technology Overview",
    "Cryptocurrency Development Guide",
    "Web3 and Decentralized Applications",
    "Cloud Computing Fundamentals",
    "Serverless Architecture Benefits",
    "DevOps Culture and Practices",
    "Monitoring and Logging Strategies",
    "Infrastructure as Code with Terraform",
    "Git Workflow Best Practices",
    "Code Review Guidelines",
    "Agile Development Methodologies",
    "Scrum Framework Implementation",
    "Project Management for Developers",
    "Remote Work Best Practices",
    "Developer Productivity Tips"
]

SAMPLE_CONTENT_TEMPLATES = [
    """In this comprehensive guide, we'll explore {topic} and how it can improve your development workflow. 

## Introduction

{topic} has become increasingly important in modern software development. This article will cover the fundamental concepts and practical applications.

## Key Concepts

1. **Understanding the Basics**: We'll start with the core principles
2. **Implementation Strategies**: Practical approaches to implementation
3. **Best Practices**: Industry-standard recommendations
4. **Common Pitfalls**: What to avoid and how to troubleshoot

## Getting Started

To begin with {topic}, you'll need to understand the following prerequisites:

- Basic programming knowledge
- Familiarity with development tools
- Understanding of software architecture principles

## Implementation Example

Here's a practical example of how to implement {topic}:

```python
# Sample code implementation
def example_function():
    return "This is an example of {topic}"
```

## Conclusion

{topic} is a powerful tool that can significantly improve your development process. By following the guidelines in this article, you'll be able to implement it effectively in your projects.

## Further Reading

- Official documentation
- Community resources
- Advanced tutorials
""",
    """This article provides an in-depth look at {topic} and its applications in modern software development.

## Overview

{topic} has revolutionized the way we approach software development. In this guide, we'll explore its benefits and implementation strategies.

## Why {topic} Matters

- Improved efficiency
- Better code quality
- Enhanced maintainability
- Reduced development time

## Step-by-Step Implementation

### Step 1: Planning
Before implementing {topic}, it's crucial to plan your approach carefully.

### Step 2: Setup
Configure your development environment with the necessary tools.

### Step 3: Implementation
Follow these best practices for implementation:

1. Start with a simple example
2. Gradually add complexity
3. Test thoroughly
4. Document your code

### Step 4: Testing
Ensure your implementation works correctly with comprehensive testing.

## Real-World Examples

Many successful companies have implemented {topic} to improve their development processes:

- Company A saw a 40% improvement in deployment speed
- Company B reduced bugs by 60%
- Company C improved team collaboration

## Conclusion

{topic} is an essential skill for modern developers. By mastering these concepts, you'll be better equipped to build robust, scalable applications.
"""
]

def generate_slug(title: str) -> str:
    """Generate a URL-friendly slug from a title."""
    return title.lower().replace(' ', '-').replace(':', '').replace('?', '').replace(',', '').replace("'", '')

def generate_excerpt(content: str) -> str:
    """Generate an excerpt from content."""
    sentences = content.split('. ')
    return '. '.join(sentences[:2]) + '.' if len(sentences) > 1 else content[:200]

def generate_meta_description(title: str) -> str:
    """Generate a meta description from title."""
    return f"Learn about {title.lower()} with this comprehensive guide. Practical tips and best practices for developers."

def generate_random_date(start_date: datetime, end_date: datetime) -> str:
    """Generate a random datetime between start and end dates."""
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime('%Y-%m-%d %H:%M:%S')

def generate_posts_sql(num_posts: int = 920) -> str:
    """Generate SQL INSERT statements for posts."""
    sql_parts = []
    
    # Date range for posts (last 2 years)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    
    for i in range(1, num_posts + 1):
        # Select random title or generate variation
        if i <= len(SAMPLE_TITLES):
            title = SAMPLE_TITLES[i-1]
        else:
            base_title = random.choice(SAMPLE_TITLES)
            title = f"{base_title} - Part {(i-1) // len(SAMPLE_TITLES) + 1}"
        
        slug = generate_slug(title)
        if i > len(SAMPLE_TITLES):
            slug += f"-{i}"
        
        # Generate content
        topic = title.lower()
        content_template = random.choice(SAMPLE_CONTENT_TEMPLATES)
        content = content_template.format(topic=topic).replace("'", "''")
        
        excerpt = generate_excerpt(content)[:300]
        meta_description = generate_meta_description(title)
        
        # Random assignments
        author_id = random.randint(1, 5)  # Assuming 5 users exist
        category_id = random.randint(1, 20)
        status_id = random.choice([1, 2, 3, 4, 5, 7])  # Mostly active statuses
        
        # Random dates
        created_at = generate_random_date(start_date, end_date)
        updated_at = created_at
        
        # Published date only for published/featured posts
        published_at = 'NULL'
        if status_id in [3, 7]:  # Published or Featured
            pub_date = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S') + timedelta(hours=random.randint(1, 48))
            published_at = f"'{pub_date.strftime('%Y-%m-%d %H:%M:%S')}'"
        
        # Featured image (some posts have images)
        featured_image = ''
        if random.random() < 0.3:  # 30% chance of having featured image
            featured_image = f'posts/featured_{i}.jpg'
        
        sql_part = f"""({i}, '{title.replace("'", "''")}', '{slug}', {author_id}, '{content}', '{excerpt.replace("'", "''")}', {category_id}, {status_id}, {'NULL' if not featured_image else f"'{featured_image}'"}, '{meta_description.replace("'", "''")}', '{created_at}', '{updated_at}', {published_at})"""
        
        sql_parts.append(sql_part)
    
    return ',\n'.join(sql_parts) + ';'

def generate_post_tags_sql(num_posts: int = 920) -> str:
    """Generate SQL INSERT statements for post-tag relationships."""
    sql_parts = []
    relationship_id = 1
    
    for post_id in range(1, num_posts + 1):
        # Each post gets 1-5 random tags
        num_tags = random.randint(1, 5)
        selected_tags = random.sample(range(1, 51), num_tags)  # 50 tags available
        
        for tag_id in selected_tags:
            sql_parts.append(f"({relationship_id}, {post_id}, {tag_id})")
            relationship_id += 1
    
    return ',\n'.join(sql_parts) + ';'

def main():
    """Generate the complete SQL dump."""
    print("-- SQL Dump for blog_app with 1000 records")
    print("-- Generated for Django blog application")
    print("-- Models: PostStatus, Category, Tag, Post")
    print()
    print("-- Disable foreign key checks for easier insertion")
    print("SET foreign_key_checks = 0;")
    print()
    
    # PostStatus data (already defined in the partial file)
    print("-- ============================================================================")
    print("-- PostStatus Data (10 records)")
    print("-- ============================================================================")
    print()
    
    poststatus_data = """INSERT INTO blog_app_poststatus (id, name, slug, description, icon, color, is_published, is_active, sort_order, created_at, updated_at) VALUES
(1, 'Draft', 'draft', 'Post is being written and not ready for publication', 'draft', '#6B7280', 0, 1, 1, '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(2, 'Review', 'review', 'Post is ready for editorial review', 'review', '#F59E0B', 0, 1, 2, '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(3, 'Published', 'published', 'Post is live and publicly visible', 'published', '#10B981', 1, 1, 3, '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(4, 'Scheduled', 'scheduled', 'Post is scheduled for future publication', 'scheduled', '#3B82F6', 0, 1, 4, '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(5, 'Private', 'private', 'Post is private and only visible to author', 'private', '#8B5CF6', 0, 1, 5, '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(6, 'Archived', 'archived', 'Post is archived and no longer active', 'archived', '#6B7280', 0, 1, 6, '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(7, 'Featured', 'featured', 'Post is featured and highlighted', 'featured', '#EF4444', 1, 1, 7, '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(8, 'Pending', 'pending', 'Post is pending approval', 'pending', '#F97316', 0, 1, 8, '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(9, 'Rejected', 'rejected', 'Post has been rejected and needs revision', 'rejected', '#DC2626', 0, 1, 9, '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(10, 'Trash', 'trash', 'Post is in trash and will be deleted', 'trash', '#374151', 0, 0, 10, '2024-01-01 10:00:00', '2024-01-01 10:00:00');"""
    
    print(poststatus_data)
    print()
    
    # Category data
    print("-- ============================================================================")
    print("-- Category Data (20 records)")
    print("-- ============================================================================")
    print()
    
    categories = [
        ('Technology', 'Latest trends and insights in technology'),
        ('Programming', 'Programming tutorials, tips, and best practices'),
        ('Web Development', 'Frontend and backend web development topics'),
        ('Mobile Development', 'iOS, Android, and cross-platform mobile development'),
        ('Data Science', 'Data analysis, machine learning, and AI topics'),
        ('DevOps', 'Development operations, CI/CD, and infrastructure'),
        ('Design', 'UI/UX design, graphic design, and user experience'),
        ('Business', 'Business strategies, entrepreneurship, and startups'),
        ('Career', 'Career advice, job hunting, and professional development'),
        ('Tutorials', 'Step-by-step guides and how-to articles'),
        ('Reviews', 'Product reviews and comparisons'),
        ('News', 'Latest news and updates in tech industry'),
        ('Open Source', 'Open source projects and contributions'),
        ('Security', 'Cybersecurity, privacy, and data protection'),
        ('Cloud Computing', 'Cloud platforms, services, and architecture'),
        ('Databases', 'Database design, optimization, and management'),
        ('Testing', 'Software testing, QA, and quality assurance'),
        ('Performance', 'Performance optimization and monitoring'),
        ('Tools', 'Development tools, IDEs, and productivity software'),
        ('Lifestyle', 'Work-life balance and developer lifestyle')
    ]
    
    category_sql = "INSERT INTO blog_app_category (id, name, slug, description, created_at, updated_at) VALUES\n"
    category_values = []
    for i, (name, desc) in enumerate(categories, 1):
        slug = generate_slug(name)
        category_values.append(f"({i}, '{name}', '{slug}', '{desc}', '2024-01-01 10:00:00', '2024-01-01 10:00:00')")
    
    print(category_sql + ',\n'.join(category_values) + ';')
    print()
    
    # Tag data
    print("-- ============================================================================")
    print("-- Tag Data (50 records)")
    print("-- ============================================================================")
    print()
    
    tags = [
        'Python', 'JavaScript', 'React', 'Django', 'Node.js', 'TypeScript', 'Vue.js', 'Angular',
        'CSS', 'HTML', 'Machine Learning', 'AI', 'Docker', 'Kubernetes', 'AWS', 'Azure',
        'Google Cloud', 'PostgreSQL', 'MongoDB', 'Redis', 'GraphQL', 'REST API', 'Microservices',
        'Serverless', 'Git', 'GitHub', 'CI/CD', 'Testing', 'TDD', 'Agile', 'Scrum', 'Performance',
        'Security', 'Authentication', 'Authorization', 'JWT', 'OAuth', 'HTTPS', 'SSL', 'Encryption',
        'Mobile', 'iOS', 'Android', 'React Native', 'Flutter', 'Swift', 'Kotlin', 'Java', 'C#', 'Go'
    ]
    
    tag_sql = "INSERT INTO blog_app_tag (id, name, slug, created_at) VALUES\n"
    tag_values = []
    for i, tag in enumerate(tags, 1):
        slug = generate_slug(tag)
        tag_values.append(f"({i}, '{tag}', '{slug}', '2024-01-01 10:00:00')")
    
    print(tag_sql + ',\n'.join(tag_values) + ';')
    print()
    
    # Post data
    print("-- ============================================================================")
    print("-- Post Data (920 records)")
    print("-- ============================================================================")
    print()
    
    print("INSERT INTO blog_app_post (id, title, slug, author_id, content, excerpt, category_id, status_id, featured_image, meta_description, created_at, updated_at, published_at) VALUES")
    print(generate_posts_sql())
    print()
    
    # Post-Tag relationships
    print("-- ============================================================================")
    print("-- Post-Tag Relationships (Many-to-Many)")
    print("-- ============================================================================")
    print()
    
    print("INSERT INTO blog_app_post_tags (id, post_id, tag_id) VALUES")
    print(generate_post_tags_sql())
    print()
    
    # Re-enable foreign key checks
    print("-- Re-enable foreign key checks")
    print("SET foreign_key_checks = 1;")
    print()
    print("-- Total records: 1000+ (10 PostStatus + 20 Categories + 50 Tags + 920 Posts + relationships)")

if __name__ == "__main__":
    main()