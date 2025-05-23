from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),

    # Authentication
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Role-Based Registration
    path('register/', views.register, name='register'), 
    path('register/journalist/', views.register_journalist, name='register_journalist'),
    path('register/subscriber/', views.register_subscriber, name='register_subscriber'),
    path('register/publisher/', views.register_publisher, name='register_publisher'),

    # Dashboards
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/journalist/', views.journalist_dashboard, name='journalist_dashboard'),
    path('dashboard/publisher/', views.publisher_dashboard, name='publisher_dashboard'),
    path('dashboard/reader/', views.reader_dashboard, name='reader_dashboard'),

    # Articles
    path('journalist/articles/create/', views.create_article, name='create_article'),
    path('journalist/articles/<int:pk>/edit/', views.update_article, name='update_article'),
    path('journalist/articles/<int:pk>/delete/', views.delete_article, name='delete_article'),
    path('journalist/profile/edit/', views.edit_journalist_profile, name='edit_profile'),
    path('journalist/<int:pk>/', views.journalist_detail, name='journalist_detail'),

    # Newsletters
    path('journalist/newsletters/create/', views.create_newsletter, name='create_newsletter'),
    path('journalist/newsletters/<int:pk>/edit/', views.update_newsletter, name='update_newsletter'),
    path('journalist/newsletters/<int:pk>/delete/', views.delete_newsletter, name='delete_newsletter'),

    # Editor Approval
    path('article/approve/<int:pk>/', views.approve_article, name='approve_article'),
    path('publishers/', views.publisher_list, name='publishers_list'),
    path('publisher/update/', views.update_publisher_profile, name='update_publisher_profile'),
    path('publisher/<int:publisher_id>/', views.publisher_detail, name='publisher_detail'),
    path('publisher/<int:publisher_id>/subscribe/', views.subscribe_publisher, name='subscribe_publisher'),

    # Reader dashoard
    path('publishers/', views.publisher_list, name='publisher_list'),
    path('journalists/', views.journalist_list, name='journalist_list'),
    path('journalists/<int:journalist_id>/subscribe/', views.subscribe_to_journalist, name='subscribe_to_journalist'),
    path('journalists/<int:journalist_id>/unsubscribe/', views.unsubscribe_from_journalist, name='unsubscribe_from_journalist'),
    path('articles/<int:id>/', views.article_detail, name='article_detail'),
    path('newsletter/<int:pk>/', views.newsletter_detail, name='newsletter_detail'),

    # APIs
    path('api-guide/', views.api_guide, name='api_guide'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
