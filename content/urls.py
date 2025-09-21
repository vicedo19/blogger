from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # API v1 endpoints
    path('api/v1/', include('content.api_urls')),
    
    # API Documentation - redirect to FastAPI docs
    path('api/docs/', RedirectView.as_view(url='http://localhost:8001/docs', permanent=False), name='api_docs'),
    path('api/docs/openapi.json', RedirectView.as_view(url='http://localhost:8001/openapi.json', permanent=False), name='api_openapi'),
]