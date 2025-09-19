from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog_app.models import PostStatus, Category, Tag, Post
from datetime import datetime
import re


class Command(BaseCommand):
    help = 'Load seed data from seed3.sql file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='seed3.sql',
            help='Path to the SQL seed file'
        )

    def handle(self, *args, **options):
        sql_file = options['file']
        self.stdout.write(f'Loading data from {sql_file}...')
        
        # Create default user if needed
        if not User.objects.exists():
            self.stdout.write('Creating default admin user...')
            user = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123',
                is_staff=True,
                is_superuser=True
            )
        else:
            user = User.objects.first()

        # Load PostStatus data
        self.load_post_statuses()
        
        # Load Category data
        self.load_categories()
        
        # Load Tag data
        self.load_tags()
        
        # Load Post data
        self.load_posts(user)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded seed data!')
        )

    def load_post_statuses(self):
        """Load PostStatus data"""
        self.stdout.write('Loading PostStatus data...')
        PostStatus.objects.all().delete()
        
        statuses = [
            (1, 'Draft', 'draft', 'Post is being written and not ready for publication', 'draft', '#6B7280', False, True, 1),
            (2, 'Review', 'review', 'Post is ready for editorial review', 'review', '#F59E0B', False, True, 2),
            (3, 'Published', 'published', 'Post is live and publicly visible', 'published', '#10B981', True, True, 3),
            (4, 'Scheduled', 'scheduled', 'Post is scheduled for future publication', 'scheduled', '#3B82F6', False, True, 4),
            (5, 'Private', 'private', 'Post is private and only visible to author', 'private', '#8B5CF6', False, True, 5),
            (6, 'Archived', 'archived', 'Post is archived and no longer active', 'archived', '#6B7280', False, True, 6),
            (7, 'Featured', 'featured', 'Post is featured and highlighted', 'featured', '#EF4444', True, True, 7),
            (8, 'Pending', 'pending', 'Post is pending approval', 'pending', '#F97316', False, True, 8),
            (9, 'Rejected', 'rejected', 'Post has been rejected and needs revision', 'rejected', '#DC2626', False, True, 9),
            (10, 'Trash', 'trash', 'Post is in trash and will be deleted', 'trash', '#374151', False, False, 10),
        ]
        
        for status_data in statuses:
            PostStatus.objects.create(
                id=status_data[0],
                name=status_data[1],
                slug=status_data[2],
                description=status_data[3],
                icon=status_data[4],
                color=status_data[5],
                is_published=status_data[6],
                is_active=status_data[7],
                sort_order=status_data[8],
                created_at=datetime(2024, 1, 1, 10, 0, 0),
                updated_at=datetime(2024, 1, 1, 10, 0, 0)
            )
        
        self.stdout.write(f'Created {len(statuses)} PostStatus records')

    def load_categories(self):
        """Load Category data"""
        self.stdout.write('Loading Category data...')
        Category.objects.all().delete()
        
        categories = [
            (1, 'Technology', 'technology', 'Latest trends and insights in technology'),
            (2, 'Programming', 'programming', 'Programming tutorials, tips, and best practices'),
            (3, 'Web Development', 'web-development', 'Frontend and backend web development topics'),
            (4, 'Mobile Development', 'mobile-development', 'iOS, Android, and cross-platform mobile development'),
            (5, 'Data Science', 'data-science', 'Data analysis, machine learning, and AI topics'),
            (6, 'DevOps', 'devops', 'Development operations, CI/CD, and infrastructure'),
            (7, 'Design', 'design', 'UI/UX design, graphic design, and user experience'),
            (8, 'Business', 'business', 'Business strategies, entrepreneurship, and startups'),
            (9, 'Career', 'career', 'Career advice, job hunting, and professional development'),
            (10, 'Tutorials', 'tutorials', 'Step-by-step guides and how-to articles'),
            (11, 'Reviews', 'reviews', 'Product reviews and comparisons'),
            (12, 'News', 'news', 'Latest news and updates in tech industry'),
            (13, 'Open Source', 'open-source', 'Open source projects and contributions'),
            (14, 'Security', 'security', 'Cybersecurity, privacy, and data protection'),
            (15, 'Cloud Computing', 'cloud-computing', 'Cloud platforms, services, and architecture'),
            (16, 'Databases', 'databases', 'Database design, optimization, and management'),
            (17, 'Testing', 'testing', 'Software testing, QA, and quality assurance'),
            (18, 'Performance', 'performance', 'Performance optimization and monitoring'),
            (19, 'Tools', 'tools', 'Development tools, IDEs, and productivity software'),
            (20, 'Lifestyle', 'lifestyle', 'Work-life balance and developer lifestyle'),
        ]
        
        for cat_data in categories:
            Category.objects.create(
                id=cat_data[0],
                name=cat_data[1],
                slug=cat_data[2],
                description=cat_data[3],
                created_at=datetime(2024, 1, 1, 10, 0, 0),
                updated_at=datetime(2024, 1, 1, 10, 0, 0)
            )
        
        self.stdout.write(f'Created {len(categories)} Category records')

    def load_tags(self):
        """Load Tag data"""
        self.stdout.write('Loading Tag data...')
        Tag.objects.all().delete()
        
        tags = [
            'Python', 'JavaScript', 'React', 'Django', 'Node.js', 'TypeScript', 'Vue.js', 'Angular', 'CSS', 'HTML',
            'Machine Learning', 'AI', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'Google Cloud', 'PostgreSQL', 'MongoDB', 'Redis',
            'GraphQL', 'REST API', 'Microservices', 'Serverless', 'Git', 'GitHub', 'CI/CD', 'Testing', 'TDD', 'Agile',
            'Scrum', 'Performance', 'Security', 'Authentication', 'Authorization', 'JWT', 'OAuth', 'HTTPS', 'SSL', 'Encryption',
            'Mobile', 'iOS', 'Android', 'React Native', 'Flutter', 'Swift', 'Kotlin', 'Java', 'C#', 'Go'
        ]
        
        for i, tag_name in enumerate(tags, 1):
            Tag.objects.create(
                id=i,
                name=tag_name,
                slug=tag_name.lower().replace('.', '').replace('#', '').replace(' ', '-'),
                created_at=datetime(2024, 1, 1, 10, 0, 0)
            )
        
        self.stdout.write(f'Created {len(tags)} Tag records')

    def load_posts(self, user):
        """Load sample Post data"""
        self.stdout.write('Loading Post data...')
        Post.objects.all().delete()
        
        # Create some sample posts
        sample_posts = [
            {
                'title': 'Getting Started with Python Web Development',
                'slug': 'getting-started-with-python-web-development',
                'content': self.get_sample_content('Python web development'),
                'excerpt': 'Learn the fundamentals of Python web development with Django and Flask.',
                'category_id': 3,  # Web Development
                'status_id': 3,    # Published
                'meta_description': 'Complete guide to Python web development for beginners.',
            },
            {
                'title': 'Advanced JavaScript Techniques',
                'slug': 'advanced-javascript-techniques',
                'content': self.get_sample_content('JavaScript techniques'),
                'excerpt': 'Master advanced JavaScript concepts and modern ES6+ features.',
                'category_id': 2,  # Programming
                'status_id': 3,    # Published
                'meta_description': 'Learn advanced JavaScript techniques and best practices.',
            },
            {
                'title': 'Building Scalable React Applications',
                'slug': 'building-scalable-react-applications',
                'content': self.get_sample_content('React applications'),
                'excerpt': 'Best practices for building large-scale React applications.',
                'category_id': 3,  # Web Development
                'status_id': 1,    # Draft
                'meta_description': 'Guide to building scalable React applications.',
            },
            {
                'title': 'Django Best Practices for Production',
                'slug': 'django-best-practices-for-production',
                'content': self.get_sample_content('Django production'),
                'excerpt': 'Essential Django practices for production deployment.',
                'category_id': 3,  # Web Development
                'status_id': 3,    # Published
                'meta_description': 'Django best practices for production environments.',
            },
            {
                'title': 'Introduction to Machine Learning',
                'slug': 'introduction-to-machine-learning',
                'content': self.get_sample_content('Machine Learning'),
                'excerpt': 'Get started with machine learning concepts and Python libraries.',
                'category_id': 5,  # Data Science
                'status_id': 2,    # Review
                'meta_description': 'Beginner guide to machine learning with Python.',
            },
        ]
        
        for i, post_data in enumerate(sample_posts, 1):
            category = Category.objects.get(id=post_data['category_id'])
            status = PostStatus.objects.get(id=post_data['status_id'])
            
            post = Post.objects.create(
                id=i,
                title=post_data['title'],
                slug=post_data['slug'],
                author=user,
                content=post_data['content'],
                excerpt=post_data['excerpt'],
                category=category,
                status=status,
                meta_description=post_data['meta_description'],
                created_at=datetime(2024, 1, i, 10, 0, 0),
                updated_at=datetime(2024, 1, i, 10, 0, 0),
                published_at=datetime(2024, 1, i+5, 10, 0, 0) if post_data['status_id'] == 3 else None
            )
            
            # Add some tags to posts
            tag_ids = [1, 2, 3, 4, 5]  # First 5 tags
            for tag_id in tag_ids[:3]:  # Add 3 tags per post
                try:
                    tag = Tag.objects.get(id=tag_id)
                    post.tags.add(tag)
                except Tag.DoesNotExist:
                    pass
        
        self.stdout.write(f'Created {len(sample_posts)} Post records')

    def get_sample_content(self, topic):
        """Generate sample content for posts"""
        return f"""# {topic}

This comprehensive guide covers everything you need to know about {topic.lower()}.

## Introduction

{topic} has become increasingly important in modern software development. This article will walk you through the key concepts and practical applications.

## Key Features

- **Performance**: Optimized for speed and efficiency
- **Scalability**: Built to handle growing demands
- **Security**: Industry-standard security practices
- **Maintainability**: Clean, readable code structure

## Getting Started

To begin with {topic.lower()}, you'll need:

1. Basic understanding of programming concepts
2. Development environment setup
3. Required tools and libraries

## Best Practices

Here are some best practices to follow:

- Write clean, readable code
- Follow established conventions
- Test your implementation thoroughly
- Document your work properly

## Conclusion

{topic} is a powerful tool that can significantly improve your development workflow. By following the guidelines in this article, you'll be well on your way to mastering these concepts.

## Further Reading

- Official documentation
- Community resources
- Advanced tutorials and examples
"""