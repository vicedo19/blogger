# Project Rules & Guidelines

## 📋 Table of Contents
- [Code Standards](#code-standards)
- [AI Development Guidelines](#ai-development-guidelines)
- [Git Workflow](#git-workflow)
- [Testing Requirements](#testing-requirements)
- [Security Guidelines](#security-guidelines)
- [Performance Standards](#performance-standards)
- [Documentation Rules](#documentation-rules)
- [Deployment Guidelines](#deployment-guidelines)

## 🎯 Code Standards

### Python/Django Standards
- **PEP 8 Compliance**: All Python code must follow PEP 8 style guidelines
- **Type Hints**: Use type hints for all function parameters and return values
- **Docstrings**: All classes and functions must have comprehensive docstrings
- **Line Length**: Maximum 88 characters (Black formatter standard)
- **Import Organization**: Use isort for consistent import ordering
- **Environment Variables**: Use python-decouple for environment variable management with proper type casting
- **Class Names**: PascalCase (e.g., `BlogPost`, `UserProfile`)
- **Function Names**: snake_case (e.g., `create_blog_post`, `get_user_data`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_TITLE_LENGTH`, `DEFAULT_PAGE_SIZE`)

#### Environment Variable Examples
```python
from decouple import config, Csv

# Basic string configuration
SECRET_KEY = config('SECRET_KEY')

# Boolean with type casting
DEBUG = config('DEBUG', default=False, cast=bool)

# Integer with type casting
DATABASE_PORT = config('DATABASE_PORT', default=5432, cast=int)

# CSV list with type casting
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())

# With default values
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
```

### JavaScript/TypeScript Standards
- **ESLint Configuration**: Follow Airbnb style guide with TypeScript extensions
- **Prettier Formatting**: Use Prettier for consistent code formatting
- **Type Safety**: Strict TypeScript configuration, no `any` types allowed
- **Component Names**: PascalCase for React components (e.g., `BlogPostCard`, `UserProfile`)
- **File Names**: kebab-case for files (e.g., `blog-post-card.tsx`, `user-profile.ts`)
- **Hook Names**: Start with `use` prefix (e.g., `useBlogPosts`, `useAuth`)
- **Interface Names**: Start with `I` prefix (e.g., `IBlogPost`, `IUserData`)

### CSS/Styling Standards
- **Tailwind CSS**: Primary styling framework
- **Mobile-First**: Always design mobile-first, then scale up
- **Semantic Classes**: Use semantic class names for custom CSS
- **Color Palette**: Stick to defined color palette in Tailwind config
- **Responsive Design**: All components must be responsive across all breakpoints

## 🤖 AI Development Guidelines

### AI Usage Principles
1. **AI-First Approach**: Use AI for all scaffolding, testing, and documentation
2. **Human Review**: All AI-generated code must be reviewed before merging
3. **Iterative Refinement**: Use AI to refine and optimize existing code
4. **Consistency**: Maintain consistent patterns across AI-generated components

### AI Prompt Standards
- **Specific Requirements**: Always provide detailed, specific requirements
- **Context Inclusion**: Include relevant project context and existing patterns
- **Output Format**: Specify exact output format and file structure
- **Testing Requirements**: Always request comprehensive tests with generated code
- **Documentation**: Request inline documentation and README updates

### AI Code Review Process
1. **Initial Generation**: Use AI to generate initial code structure
2. **Human Validation**: Review for logic, security, and performance
3. **AI Optimization**: Use AI to optimize and refine the code
4. **Final Review**: Human final review before commit
5. **Documentation**: AI generates/updates relevant documentation

## 📝 Git Workflow

### Branch Naming Convention
- **Feature branches**: `feature/description-of-feature`
- **Bug fixes**: `fix/description-of-bug`
- **Hotfixes**: `hotfix/critical-issue-description`
- **Releases**: `release/version-number`
- **AI-generated**: `ai/component-or-feature-name`

### Commit Message Standards
- **Format**: `type(scope): description`
- **Types**: feat, fix, docs, style, refactor, test, chore, ai
- **AI Commits**: Use `ai(scope): description` for AI-generated code
- **Examples**:
  - `feat(blog): add blog post creation API`
  - `ai(components): generate BlogPostCard component`
  - `fix(auth): resolve login validation issue`
  - `docs(readme): update AI integration section`

### Pull Request Requirements
- **AI Agent Review**: Use AI agent for initial code review
- **Human Approval**: Minimum one human reviewer approval required
- **Tests Passing**: All tests must pass before merge
- **Documentation**: Update relevant documentation
- **Performance Check**: No performance regressions allowed

## 🧪 Testing Requirements

### Test Coverage Standards
- **Minimum Coverage**: 90% code coverage for all modules
- **Unit Tests**: Every function and component must have unit tests
- **Integration Tests**: All API endpoints must have integration tests
- **E2E Tests**: Critical user flows must have end-to-end tests

### Testing Frameworks
- **Backend**: pytest for Django testing
- **Frontend**: Jest + React Testing Library
- **E2E**: Playwright or Cypress
- **API Testing**: Django REST Framework test client

### AI-Generated Test Requirements
- **Comprehensive Scenarios**: Tests must cover success, error, and edge cases
- **Mock Data**: Use realistic, AI-generated test data
- **Performance Tests**: Include performance benchmarks
- **Security Tests**: Test for common vulnerabilities

## 🔒 Security Guidelines

### Authentication & Authorization
- **JWT Tokens**: Use secure JWT implementation with proper expiration
- **Password Security**: Implement strong password requirements
- **Rate Limiting**: Implement rate limiting on all API endpoints
- **CORS Configuration**: Properly configure CORS for production

### Data Protection
- **Input Validation**: Validate and sanitize all user inputs
- **SQL Injection**: Use Django ORM to prevent SQL injection
- **XSS Protection**: Implement proper XSS protection measures
- **CSRF Protection**: Enable CSRF protection for all forms

### Environment Security
- **Environment Variables**: Use python-decouple for secure environment variable management
- **Type Safety**: Utilize python-decouple's type casting (cast=bool, cast=int, cast=Csv())
- **Default Values**: Always provide sensible default values for non-critical settings
- **Secret Management**: Never commit secrets to version control, use .env files locally
- **Production Configuration**: Use environment-specific configuration management
- **HTTPS Only**: All production traffic must use HTTPS
- **Security Headers**: Implement proper security headers

## ⚡ Performance Standards

### Backend Performance
- **Response Time**: API responses must be under 200ms for 95% of requests
- **Database Queries**: Optimize N+1 queries, use select_related/prefetch_related
- **Caching**: Implement Redis caching for frequently accessed data
- **Pagination**: Implement pagination for all list endpoints

### Frontend Performance
- **Bundle Size**: Keep JavaScript bundles under 250KB gzipped
- **Code Splitting**: Implement route-based code splitting
- **Image Optimization**: Use WebP format and proper sizing
- **Lazy Loading**: Implement lazy loading for images and components

### Database Performance
- **Indexing**: Proper database indexing for all query patterns
- **Query Optimization**: Regular query performance analysis
- **Connection Pooling**: Use connection pooling for database connections
- **Monitoring**: Implement database performance monitoring

## 📚 Documentation Rules

### Code Documentation
- **Inline Comments**: Explain complex logic with clear comments
- **API Documentation**: Auto-generate API docs from code
- **Component Documentation**: Document all React components with Storybook
- **README Updates**: Keep README.md current with all changes

### AI Documentation Standards
- **Prompt Documentation**: Document all AI prompts used
- **Generated Code**: Mark AI-generated code with appropriate comments
- **Review Notes**: Document human review and modifications
- **Learning Notes**: Document lessons learned from AI interactions

### Migration Guidelines
- **Environment Variable Migration**: When migrating from python-dotenv to python-decouple:
  1. Remove python-dotenv from dependencies (Pipfile/requirements.txt)
  2. Update imports: `from decouple import config, Csv`
  3. Replace `os.getenv()` calls with `config()` calls
  4. Add type casting where appropriate (cast=bool, cast=int, cast=Csv())
  5. Provide sensible default values for non-critical settings
  6. Test all environment variable configurations thoroughly

## 🚀 Deployment Guidelines

### Environment Management
- **Development**: Local development with SQLite
- **Staging**: Staging environment with Supabase PostgreSQL
- **Production**: Production deployment on Railway/Render

### Deployment Process
1. **AI Code Review**: Run AI agent review on all changes
2. **Test Suite**: All tests must pass in CI/CD pipeline
3. **Security Scan**: Run security vulnerability scans
4. **Performance Test**: Validate performance benchmarks
5. **Staging Deployment**: Deploy to staging for final validation
6. **Production Deployment**: Deploy to production with monitoring

### Monitoring & Logging
- **Error Tracking**: Implement comprehensive error tracking
- **Performance Monitoring**: Monitor application performance metrics
- **User Analytics**: Track user behavior and feature usage
- **AI Usage Tracking**: Monitor AI agent usage and effectiveness

## 🔄 Continuous Improvement

### Code Quality
- **Regular Refactoring**: Schedule regular code refactoring sessions
- **Dependency Updates**: Keep all dependencies up to date
- **Security Audits**: Regular security vulnerability assessments
- **Performance Audits**: Regular performance optimization reviews

### AI Integration Evolution
- **Prompt Optimization**: Continuously improve AI prompts
- **New AI Features**: Explore and integrate new AI capabilities
- **Feedback Loop**: Collect feedback on AI-generated code quality
- **Training Data**: Use project learnings to improve AI interactions

## 📊 Metrics & KPIs

### Development Metrics
- **Code Coverage**: Maintain >90% test coverage
- **Build Time**: Keep CI/CD pipeline under 10 minutes
- **Bug Rate**: Less than 1 bug per 100 lines of code
- **AI Efficiency**: Track time saved through AI automation

### Performance Metrics
- **Page Load Time**: <3 seconds for initial page load
- **API Response Time**: <200ms for 95% of requests
- **Uptime**: 99.9% application uptime
- **User Satisfaction**: >4.5/5 user satisfaction score

---

## 🎯 Enforcement

These rules are enforced through:
- **Automated Linting**: ESLint, Prettier, Black, isort
- **Pre-commit Hooks**: Automated code quality checks
- **CI/CD Pipeline**: Automated testing and deployment
- **AI Agent Integration**: Automated code review and suggestions
- **Human Review**: Manual code review process

**Remember**: These rules are living guidelines that evolve with the project. Regular reviews and updates ensure they remain relevant and effective.