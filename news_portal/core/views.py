from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseForbidden

from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Article, Publisher, Newsletter, JournalistProfile
from .forms import (
    ArticleForm, UserRegisterForm, NewsletterForm,
    JournalistProfileForm, PublisherUpdateForm
)
from .serializers import ArticleSerializer

User = get_user_model()

# --- Role Check Helpers ---
def is_journalist(user):
    """Checks if the user is a journalist."""
    return user.is_authenticated and user.role == 'JOURNALIST'

def is_editor(user):
    """Checks if the user is an editor."""
    return user.is_authenticated and user.role == 'EDITOR'

def is_reader(user):
    """Checks if the user is a reader."""
    return user.is_authenticated and user.role == 'READER'

def is_publisher(user):
    """Checks if the user is a publisher."""
    return user.is_authenticated and user.role == 'PUBLISHER'

# --- Home Page ---
def home(request):
    """The public home page."""
    return render(request, 'core/home.html')

# --- Authentication Views ---
def user_login(request):
    """Handles user login."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'core/login.html')

def user_logout(request):
    """Logs out the user."""
    logout(request)
    return redirect('login')

def register(request):
    """Generic registration for any user (not used for role-specific signups)."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User registered successfully! Please log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

# --- Role-Specific Registration Views ---
def register_journalist(request):
    """Registers a user as a journalist."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'JOURNALIST'
            user.save()
            login(request, user)
            return redirect('journalist_dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

def register_subscriber(request):
    """Registers a user as a reader/subscriber."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'READER'
            user.save()
            login(request, user)
            return redirect('reader_dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

def register_publisher(request):
    """Registers a user as a publisher."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'PUBLISHER'
            user.save()
            login(request, user)
            return redirect('publisher_dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

# --- Dashboard Router ---
@login_required
def dashboard(request):
    """Redirects user to the appropriate dashboard based on their role."""
    if request.user.role == 'JOURNALIST':
        return redirect('journalist_dashboard')
    elif request.user.role == 'READER':
        return redirect('reader_dashboard')
    elif request.user.role == 'PUBLISHER':
        return redirect('publisher_dashboard')
    return render(request, 'core/dashboard.html')

# --- Journalist Dashboard ---
@login_required
@user_passes_test(is_journalist)
def journalist_dashboard(request):
    """
    Shows the journalist's dashboard with independent articles and newsletters.
    Only shows content not linked to any publisher.
    """
    independent_articles = Article.objects.filter(author=request.user, publisher__isnull=True)
    independent_newsletters = Newsletter.objects.filter(author=request.user, publisher__isnull=True)
    return render(request, 'core/journalist_dashboard.html', {
        'articles': independent_articles,
        'newsletters': independent_newsletters,
    })

# --- Publisher Dashboard ---
@login_required
@user_passes_test(is_publisher)
def publisher_dashboard(request):
    """
    Shows the publisher's dashboard.
    If a publisher profile doesn't exist for this user, create one.
    """
    try:
        my_publisher = Publisher.objects.get(editors=request.user)
    except Publisher.DoesNotExist:
        my_publisher = Publisher.objects.create(
            user=request.user,
            name=request.user.get_full_name() or request.user.username
        )
        my_publisher.editors.add(request.user)
        messages.info(request, "A publisher profile was automatically created for you.")

    articles = Article.objects.filter(publisher=my_publisher)
    pending_articles = articles.filter(approved=False)

    return render(request, 'core/publisher_dashboard.html', {
        'publisher': my_publisher,
        'articles': articles,
        'pending_articles': pending_articles,
    })

# --- Reader Dashboard ---
@login_required
@user_passes_test(is_reader)
def reader_dashboard(request):
    """
    Reader dashboard shows articles and newsletters from subscriptions.
    """
    subscribed_journalists = request.user.subscriptions_to_journalists.all()
    subscribed_publishers = request.user.subscriptions_to_publishers.all()

    articles = Article.objects.filter(
        Q(author__in=subscribed_journalists) |
        Q(publisher__in=subscribed_publishers)
    ).order_by('-created_at')

    newsletters = Newsletter.objects.filter(
        Q(author__in=subscribed_journalists) |
        Q(publisher__in=subscribed_publishers)
    ).order_by('-created_at')

    return render(request, 'core/reader_dashboard.html', {
        'articles': articles,
        'newsletters': newsletters,
    })

# --- Article CRUD ---
@login_required
def create_article(request):
    """Handles creation of a new article by a journalist."""
    form = ArticleForm(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        form.save_m2m()
        messages.success(request, "Article submitted successfully!")
        return redirect('journalist_dashboard')

    model_verbose_name = form._meta.model._meta.verbose_name.title()
    return render(request, 'core/article_form.html', {
        'form': form,
        'model_verbose_name': model_verbose_name
    })

@login_required
def update_article(request, pk):
    """Updates an article if it's an independent one by the author."""
    article = get_object_or_404(Article, pk=pk, author=request.user, publisher__isnull=True)
    form = ArticleForm(request.POST or None, instance=article, user=request.user)
    if form.is_valid():
        form.save()
        return redirect('journalist_dashboard')
    return render(request, 'core/article_form.html', {'form': form})

@login_required
def delete_article(request, pk):
    """Deletes an article if it's an independent one by the author."""
    article = get_object_or_404(Article, pk=pk, author=request.user, publisher__isnull=True)
    if request.method == 'POST':
        article.delete()
        return redirect('journalist_dashboard')
    return render(request, 'core/article_confirm_delete.html', {'article': article})

# --- Newsletter CRUD ---
@login_required
def create_newsletter(request):
    """Creates a new newsletter."""
    form = NewsletterForm(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        newsletter = form.save(commit=False)
        newsletter.author = request.user
        newsletter.save()
        form.save_m2m()
        messages.success(request, "Newsletter submitted successfully!")
        return redirect('journalist_dashboard')

    model_verbose_name = form._meta.model._meta.verbose_name.title()
    return render(request, 'core/article_form.html', {
        'form': form,
        'model_verbose_name': model_verbose_name
    })

@login_required
def update_newsletter(request, pk):
    """Updates an existing newsletter."""
    newsletter = get_object_or_404(Newsletter, pk=pk, author=request.user, publisher__isnull=True)
    form = NewsletterForm(request.POST or None, instance=newsletter)
    if form.is_valid():
        form.save()
        return redirect('journalist_dashboard')
    return render(request, 'core/newsletter_form.html', {'form': form})

@login_required
def delete_newsletter(request, pk):
    """Deletes an existing newsletter."""
    newsletter = get_object_or_404(Newsletter, pk=pk, author=request.user, publisher__isnull=True)
    if request.method == 'POST':
        newsletter.delete()
        return redirect('journalist_dashboard')
    return render(request, 'core/newsletter_confirm_delete.html', {'newsletter': newsletter})

# --- Detail Views ---
@login_required
def article_detail(request, id):
    """Displays the full article."""
    article = get_object_or_404(Article, id=id)
    return render(request, 'core/article_detail.html', {'article': article})

@login_required
def newsletter_detail(request, pk):
    """Displays the full newsletter."""
    newsletter = get_object_or_404(Newsletter, pk=pk)
    return render(request, 'core/newsletter_detail.html', {'newsletter': newsletter})

# --- Subscriptions ---
@login_required
def subscribe_publisher(request, publisher_id):
    """Subscribe to a publisher."""
    publisher = get_object_or_404(Publisher, id=publisher_id)
    if request.user in publisher.editors.all():
        messages.warning(request, "You cannot subscribe to yourself.")
    elif publisher in request.user.subscriptions_to_publishers.all():
        messages.info(request, "Already subscribed.")
    else:
        request.user.subscriptions_to_publishers.add(publisher)
        messages.success(request, f"Subscribed to {publisher.name}.")
    return redirect('reader_dashboard')

@login_required
def subscribe_to_journalist(request, journalist_id):
    """Subscribe to a journalist."""
    journalist = get_object_or_404(User, id=journalist_id, role='JOURNALIST')
    if journalist == request.user:
        messages.warning(request, "You cannot subscribe to yourself.")
    elif journalist in request.user.subscriptions_to_journalists.all():
        messages.info(request, "Already subscribed.")
    else:
        request.user.subscriptions_to_journalists.add(journalist)
        messages.success(request, f"Subscribed to {journalist.get_full_name() or journalist.username}.")
    return redirect('reader_dashboard')

@login_required
def unsubscribe_from_journalist(request, journalist_id):
    """Unsubscribe from a journalist."""
    journalist = get_object_or_404(User, id=journalist_id, role='JOURNALIST')
    if request.user.role != 'READER':
        messages.error(request, "Only readers can unsubscribe.")
    else:
        request.user.subscriptions_to_journalists.remove(journalist)
        messages.success(request, f"Unsubscribed from {journalist.get_full_name() or journalist.username}.")
    return redirect('reader_dashboard')

# --- Article Approval (Editor Action) ---
@login_required
@user_passes_test(is_publisher)
def approve_article(request, pk):
    """Approve an article and notify subscribers."""
    article = get_object_or_404(Article, pk=pk)
    if not article.publisher or request.user not in article.publisher.editors.all():
        return HttpResponseForbidden("You are not authorized to approve this article.")

    article.approved = True
    article.save()

    subscribers = User.objects.filter(role='READER').filter(
        Q(subscriptions_to_publishers=article.publisher) |
        Q(subscriptions_to_journalists=article.author)
    ).distinct()

    subject = f"New Article Published: {article.title}"
    label = f"[{article.publisher.name}]" if article.publisher else "[Independent]"
    message = f"{label} - {article.title} by {article.author.get_full_name() or article.author.username}\n\n{article.body}"

    for user in subscribers:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)

    messages.success(request, f"Article '{article.title}' approved and notifications sent.")
    return redirect('publisher_dashboard')

# --- Journalist and Publisher Info ---
@login_required
def journalist_list(request):
    """List of all journalists."""
    journalists = User.objects.filter(role='JOURNALIST')
    return render(request, 'core/journalist_list.html', {'journalists': journalists})

@login_required
def edit_journalist_profile(request):
    """Allows a journalist to edit their profile."""
    profile = get_object_or_404(JournalistProfile, user=request.user)
    form = JournalistProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('journalist_detail', pk=request.user.pk)
    return render(request, 'core/edit_journalist_profile.html', {'form': form})

@login_required
def journalist_detail(request, pk):
    """Displays a journalist's profile."""
    user = get_object_or_404(User, pk=pk)
    profile = get_object_or_404(JournalistProfile, user=user)
    return render(request, 'core/journalist_detail.html', {'journalist': user, 'profile': profile})

@login_required
@user_passes_test(is_publisher)
def update_publisher_profile(request):
    """Allows a publisher to update their profile."""
    try:
        publisher = Publisher.objects.get(editors=request.user)
    except Publisher.DoesNotExist:
        return HttpResponseForbidden("You are not linked to any publisher.")

    form = PublisherUpdateForm(request.POST or None, request.FILES or None, instance=publisher)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('publisher_dashboard')
    return render(request, 'core/publisher_update.html', {'form': form})

# --- Misc Pages ---
def publisher_list(request):
    """Public list of all publishers."""
    publishers = Publisher.objects.all()
    return render(request, 'core/publisher_list.html', {'publishers': publishers})

@login_required
def publisher_detail(request, publisher_id):
    """Shows detail page for a publisher including their approved articles."""
    publisher = get_object_or_404(Publisher, id=publisher_id)
    articles = Article.objects.filter(publisher=publisher, approved=True)
    return render(request, 'core/publisher_detail.html', {
        'publisher': publisher,
        'articles': articles,
    })

def api_guide(request):
    """Static page that explains how to use the REST API."""
    return render(request, 'core/api_guide.html')
