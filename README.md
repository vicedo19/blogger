# Blogger - Django Blogging Platform

A modern blogging platform built with Django and designed for scalability and performance.

## 🚀 Tech Stack

### Backend
- **Django 5.2.6** - Python web framework
- **Django REST Framework** - API development (to be added)
- **Python 3.x** - Programming language

### Database
- **Supabase PostgreSQL** - Primary database (to be configured)
- **SQLite** - Development database (current)

### Frontend (Planned)
- **React** - User interface library
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework

### Authentication & Security
- **Supabase Auth** - Authentication service (planned)
- **Django's built-in auth** - Current authentication system

### Deployment
- **Backend**: Railway/Render - Django API hosting
- **Frontend**: Netlify - Static site hosting
- **Database**: Supabase - Managed PostgreSQL

### Additional Tools
- **Pipenv** - Python dependency management
- **Rich Text Editor** - For blog post creation (to be added)
- **Image Upload** - Supabase Storage (planned)

## 📁 Project Structure

```
blogger/
├── blog/                 # Django project configuration
│   ├── __init__.py
│   ├── asgi.py          # ASGI configuration
│   ├── settings.py      # Django settings
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI configuration
├── manage.py            # Django management script
├── Pipfile              # Python dependencies
├── Pipfile.lock         # Locked dependencies
└── README.md            # This file
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- Pipenv
- Supabase account (for production database)

### Local Development

1. **Clone and navigate to the project**
   ```bash
   cd c:\Users\vicedo\Desktop\blogger
   ```

2. **Install dependencies**
   ```bash
   pipenv install
   ```

3. **Activate virtual environment**
   ```bash
   pipenv shell
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Admin panel: http://127.0.0.1:8000/admin/
   - Main site: http://127.0.0.1:8000/

## 🔧 Configuration

### Supabase Integration (Planned)

To integrate with Supabase, update `blog/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_supabase_db_name',
        'USER': 'your_supabase_user',
        'PASSWORD': 'your_supabase_password',
        'HOST': 'your_project.supabase.co',
        'PORT': '5432',
    }
}
```

### Required Dependencies (To be added)
```bash
pipenv install djangorestframework
pipenv install psycopg2-binary
pipenv install supabase
pipenv install django-cors-headers
```

## 📝 Features (Planned)

- [ ] User authentication and profiles
- [ ] Create, edit, and delete blog posts
- [ ] Rich text editor for content creation
- [ ] Comment system
- [ ] Categories and tags
- [ ] Search functionality
- [ ] SEO optimization
- [ ] Responsive design
- [ ] Image upload and management
- [ ] Real-time notifications

## 🚀 Deployment

### Backend (Django API)
- Deploy to Railway, Render, or Heroku
- Configure Supabase PostgreSQL connection
- Set environment variables for production

### Frontend (React)
- Build React application
- Deploy to Netlify
- Configure API endpoints to point to backend

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🤖 AI-Driven Development

This project leverages AI extensively throughout the development lifecycle to accelerate development and maintain code quality.

### 🏗️ AI-Assisted Scaffolding

**Component Generation**
- AI generates React components with proper TypeScript interfaces
- Automatic creation of Django models with appropriate field types and relationships
- Scaffolding of Django views, serializers, and URL patterns
- Generation of reusable UI components with consistent styling

**Function & Route Creation**
- AI creates Django API endpoints based on requirements
- Automatic generation of CRUD operations for models
- Creation of custom business logic functions with proper error handling
- React hooks and utility functions generated on-demand

**Model Architecture**
- AI designs database schemas based on feature requirements
- Generates Django model classes with proper relationships
- Creates migration files and handles schema updates
- Suggests optimal indexing and performance improvements

### 🧪 AI-Generated Testing

**Unit Tests**
- Automatic generation of Django model tests
- React component unit tests with proper mocking
- API endpoint tests with various scenarios (success, error, edge cases)
- Utility function tests with comprehensive coverage

**Integration Tests**
- End-to-end API workflow tests
- Frontend-backend integration testing
- Database transaction and rollback tests
- Authentication and authorization flow tests

**Test Data & Fixtures**
- AI generates realistic test data and fixtures
- Creates mock data for development and testing
- Generates edge case scenarios for robust testing
- Maintains test data consistency across environments

### 📋 Schema-Driven Development

**OpenAPI Specification**
- AI generates comprehensive API documentation from Django models
- Creates OpenAPI specs with proper request/response schemas
- Generates client-side API functions from OpenAPI specs
- Maintains API versioning and backward compatibility

**Function Generation from Schema**
- Automatic creation of serializers from Django models
- Generation of TypeScript interfaces from API schemas
- Creation of form validation based on model constraints
- Database query functions optimized for specific use cases

**Code Consistency**
- AI ensures consistent coding patterns across the project
- Generates code following established conventions and best practices
- Maintains proper error handling and logging patterns
- Enforces security best practices in generated code

### 🔄 AI Development Workflow

1. **Requirement Analysis** - AI analyzes feature requirements and suggests optimal implementation
2. **Architecture Planning** - AI recommends database schema and API design
3. **Code Generation** - AI scaffolds components, models, and functions
4. **Test Creation** - AI generates comprehensive test suites
5. **Documentation** - AI creates and maintains technical documentation
6. **Code Review** - AI assists in code quality checks and optimization suggestions

### 🤖 AI Agent Integration

**Custom AI Agent (Bun + Google AI-SDK)**
This project integrates a custom-built AI agent that enhances the development workflow with intelligent automation:

**Core Features:**
- **File Directory Monitoring** - Tracks changes across the project structure
- **Intelligent Commit Messages** - Generates meaningful commit messages based on code changes
- **Markdown Documentation** - Automatically writes and updates project documentation
- **Code Review Assistance** - Provides detailed code analysis and suggestions
- **Pull Request Automation** - Generates PR descriptions and review comments

**Technical Stack:**
- **Runtime**: Bun (fast JavaScript runtime)
- **AI Engine**: Google AI-SDK for natural language processing
- **File System**: Real-time directory change detection
- **Git Integration**: Automated commit message generation
- **Documentation**: Markdown file generation and updates

**Workflow Integration:**
```bash
# Example usage in development workflow
ai-agent review --files src/
ai-agent commit --auto-generate
ai-agent docs --update README.md
ai-agent pr --create --auto-description
```

**Benefits:**
- ⚡ **Faster Development** - Automated routine tasks
- 📝 **Better Documentation** - Always up-to-date project docs
- 🔍 **Consistent Reviews** - Standardized code quality checks
- 📋 **Meaningful Commits** - Clear, descriptive commit history
- 🚀 **Streamlined PRs** - Automated pull request management

### 📝 Sample AI Prompts

**Component Generation Prompt:**
```
Create a Django model for a blog post with the following requirements:
- Title (max 200 characters)
- Content (rich text)
- Author (foreign key to User)
- Created and updated timestamps
- Published status (draft/published)
- Tags (many-to-many relationship)
- SEO meta description
- Slug for URLs

Also generate:
1. Django REST Framework serializer
2. ViewSet with CRUD operations
3. URL patterns
4. Unit tests for the model and API endpoints
5. Migration file

Follow Django best practices and include proper validation.
```

**Frontend Component Prompt:**
```
Generate a React TypeScript component for displaying a blog post card with:
- Responsive design using Tailwind CSS
- Props: title, excerpt, author, publishedDate, tags, imageUrl
- Click handler for navigation
- Hover effects and animations
- Accessibility features (ARIA labels, keyboard navigation)
- Loading and error states
- Mobile-first responsive design

Include:
1. TypeScript interfaces
2. Unit tests with React Testing Library
3. Storybook stories
4. CSS-in-JS styled components as fallback
```

**API Integration Prompt:**
```
Create API integration functions for the blog system:
- Fetch all blog posts with pagination
- Create new blog post
- Update existing post
- Delete post
- Search posts by title/content
- Filter by tags and author

Requirements:
1. Use Axios with TypeScript
2. Implement proper error handling
3. Add request/response interceptors
4. Include loading states
5. Cache management with React Query
6. Generate from OpenAPI specification
7. Include comprehensive unit tests
```

**Testing Prompt:**
```
Generate comprehensive test suite for the blog post feature:

Unit Tests:
- Django model validation tests
- API endpoint tests (CRUD operations)
- React component rendering tests
- Utility function tests

Integration Tests:
- End-to-end blog post creation workflow
- Authentication and authorization tests
- Database transaction tests
- Frontend-backend integration tests

Include:
1. Test fixtures and mock data
2. Edge case scenarios
3. Performance tests
4. Security tests (XSS, CSRF protection)
5. Accessibility tests
```

## 🔗 Links

- [Django Documentation](https://docs.djangoproject.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [React Documentation](https://react.dev/)
- [Deployment Guide](https://docs.djangoproject.com/en/5.2/howto/deployment/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Django REST Framework](https://www.django-rest-framework.org/)