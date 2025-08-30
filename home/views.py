from django.shortcuts import render
from postdare.models import Dare_project
from django.db.models import Count
import random

def home(request):

    # Real statistics from database
    total_dares = Dare_project.objects.count()
    categories_count = Dare_project.objects.values('category').distinct().count()
    
    # Get trending dares (latest 8 dares)
    trending_dares_raw = Dare_project.objects.all().order_by('-id')[:8]
    
    # Category wise count
    category_stats = Dare_project.objects.values('category').annotate(
        count=Count('category')
    ).order_by('-count')
    
    # Category ke liye emoji mapping
    category_emoji = {
        'fun': '🎉',
        'mental': '🧠', 
        'creative': '🎨',
        'adventure': '🌍',
        'fitness': '💪',
        'social': '👥',
        'cooking': '👨‍🍳',
        'technology': '💻'
    }
    
    # Difficulty options
    difficulty_levels = ['easy', 'medium', 'hard', 'extreme']
    
    # Process trending dares with extra info
    trending_dares = []
    for dare in trending_dares_raw:
        processed_dare = {
            'id': dare.id,
            'title': dare.dare_title,
            'description': dare.description,
            'category': dare.category,
            'category_emoji': category_emoji.get(dare.category.lower(), '🎯'),
            'difficulty': random.choice(difficulty_levels),
            'participants': random.randint(50, 1500),
            'likes': random.randint(20, 500),
            'views': random.randint(100, 9999),
            'timeLeft': f"{random.randint(1, 7)} days left",
            'creator': f"User{dare.id}",
            'reward': f"{random.randint(100, 500)} points"
        }
        
        # Extreme difficulty ke liye special reward
        if processed_dare['difficulty'] == 'extreme':
            processed_dare['reward'] = '500 points + Badge'
            
        trending_dares.append(processed_dare)
    
    # Calculate completed challenges (estimation)
    completed_challenges = total_dares * 50 if total_dares > 0 else 0
    
    context = {
        'total_dares': total_dares,
        'categories_count': categories_count,
        'trending_dares': trending_dares,
        'category_stats': category_stats,
        'completed_challenges': completed_challenges,
        'community_members': '50K+',
        'success_rate': '89%'
    }
    
    return render(request, 'home.html', context)