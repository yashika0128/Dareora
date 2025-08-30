from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from postdare.models import Dare_project
from django.db.models import Count

@login_required(login_url='login')
def dashboard_view(request):
    # Current logged-in user
    user = request.user
    
    # Sirf current user ke dares fetch kar rahe hain
    total_dares = Dare_project.objects.filter(user=user).count()
    
    # Recent trending dares - sirf current user ke latest 5
    trending_dares = Dare_project.objects.filter(user=user).order_by('-id')[:5]
    
    # Categories with their counts - sirf current user ke dares se
    categories_stats = Dare_project.objects.filter(user=user).values('category').annotate(
        count=Count('category')
    ).order_by('-count')
    
    # Popular categories (top 6) - sirf current user ke
    popular_categories = categories_stats[:6]
    
    # Active dares count (you can add is_active filter if needed)
    active_dares = Dare_project.objects.filter(user=user, is_active=True).count() if hasattr(Dare_project, 'is_active') else total_dares
    
    # Completed dares (example calculation)
    completed_dares = total_dares - active_dares if active_dares < total_dares else 0
    
    # Stats for cards
    stats = {
        'active_dares': active_dares,
        'completed_dares': completed_dares,
        'followers': 150,  # You can make this dynamic later
        'rating': 4.5  # You can make this dynamic later
    }
    
    # User engagement metrics
    user_engagement = {
        'engagement_score': min(85, max(25, total_dares * 10)),  # Between 25-85
        'completion_rate': (completed_dares / max(total_dares, 1)) * 100,
        'avg_rating': 4.2
    }
    
    # Growth percentage calculation
    growth_percentage = min(50, max(5, total_dares * 3))  # Between 5-50
    
    # Category insights - sirf user ke categories
    category_insights = []
    if categories_stats:
        total_category_count = sum([cat['count'] for cat in categories_stats])
        for cat in categories_stats[:4]:  # Top 4 categories
            percentage = (cat['count'] / max(total_category_count, 1)) * 100
            category_insights.append({
                'name': cat['category'],
                'count': cat['count'],
                'percentage': percentage
            })
    
    # Recent activities - user specific
    recent_activities = []
    if total_dares > 0:
        recent_dares = Dare_project.objects.filter(user=user).order_by('-id')[:3]
        for i, dare in enumerate(recent_dares):
            recent_activities.append({
                'icon': '🎯' if i == 0 else '✅',
                'title': f'{"Created" if i == 0 else "Updated"} "{dare.dare_title[:30]}..."',
                'category': dare.category,
                'time': f'{i+1} day{"s" if i > 0 else ""} ago'
            })
    
    # Achievements based on user's actual data
    achievements = []
    if total_dares >= 1:
        achievements.append({
            'icon': '🎯',
            'name': 'First Dare',
            'desc': 'Created your first dare'
        })
    if total_dares >= 5:
        achievements.append({
            'icon': '🔥',
            'name': 'Dare Creator',
            'desc': f'Created {total_dares} dares'
        })
    if len(categories_stats) >= 3:
        achievements.append({
            'icon': '🌟',
            'name': 'Category Explorer',
            'desc': f'Explored {len(categories_stats)} categories'
        })
    if total_dares >= 10:
        achievements.append({
            'icon': '⭐',
            'name': 'Rising Star',
            'desc': 'Active community member'
        })
    
    # Top categories for sidebar - user specific
    top_categories = []
    for cat in categories_stats[:5]:
        total_cat = sum([c['count'] for c in categories_stats])
        percentage = (cat['count'] / max(total_cat, 1)) * 100
        top_categories.append({
            'category': cat['category'],
            'count': cat['count'],
            'percentage': percentage
        })
    
    # Calculate average description length from user's dares
    user_dares = Dare_project.objects.filter(user=user)
    if user_dares.exists():
        total_chars = sum([len(dare.description) for dare in user_dares])
        avg_description_length = total_chars // max(user_dares.count(), 1)
    else:
        avg_description_length = 0
    
    # Suggested connections (can be made dynamic later)
    suggested_connections = [
        {
            'avatar': 'A', 
            'name': 'Alex Kumar', 
            'followers': 1200, 
            'following': False,
            'bio': 'Fitness enthusiast',
            'mutual_interests': 'fitness, adventure'
        },
        {
            'avatar': 'P', 
            'name': 'Priya Singh', 
            'followers': 850, 
            'following': True,
            'bio': 'Creative challenges',
            'mutual_interests': 'creativity, art'
        },
        {
            'avatar': 'R', 
            'name': 'Rahul Sharma', 
            'followers': 650, 
            'following': False,
            'bio': 'Adventure seeker',
            'mutual_interests': 'adventure, travel'
        },
        {
            'avatar': 'S', 
            'name': 'Sneha Patel', 
            'followers': 920, 
            'following': False,
            'bio': 'Lifestyle blogger',
            'mutual_interests': 'lifestyle, wellness'
        },
    ]
    
    context = {
        'user': user,
        'total_dares': total_dares,
        'active_dares': active_dares,
        'expired_dares': completed_dares,
        'trending_dares': trending_dares,
        'categories_stats': categories_stats,
        'popular_categories': popular_categories,
        'stats': stats,
        'suggested_connections': suggested_connections,
        'user_engagement': user_engagement,
        'growth_percentage': growth_percentage,
        'category_insights': category_insights,
        'recent_activities': recent_activities,
        'achievements': achievements,
        'top_categories': top_categories,
        'avg_description_length': avg_description_length,
    }
    
    return render(request, 'dashboard.html', context)