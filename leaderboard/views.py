from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta

# Create your views here.
@login_required
def leaderboard(request):
    # Period filter (weekly, monthly, alltime)
    period = request.GET.get('period', 'weekly')
    
    # Get current user's data
    current_user_data = get_current_user_data(request.user, period)
    
    # Get top 3 users for podium
    top_3_users = get_top_users(period, limit=3)
    
    # Get remaining users for main leaderboard (4th onwards)
    remaining_users = get_top_users(period, offset=3, limit=12)
    
    # Get category wise top users
    category_data = get_category_wise_leaders()
    
    context = {
        'current_user_data': current_user_data,
        'top_3_users': top_3_users,
        'remaining_users': remaining_users,
        'category_data': category_data,
        'current_period': period,
    }
    
    return render(request, "leaderboard.html", context)

def get_current_user_data(user, period):
    """Current user ke stats nikalne ke liye function"""
    try:
        from postdare.models import Dare_project
        
        # Period ke according date filter
        if period == 'weekly':
            start_date = timezone.now() - timedelta(days=7)
            date_filter = Q(created_at__gte=start_date) if hasattr(Dare_project, 'created_at') else Q()
        elif period == 'monthly':
            start_date = timezone.now() - timedelta(days=30)
            date_filter = Q(created_at__gte=start_date) if hasattr(Dare_project, 'created_at') else Q()
        else:  # alltime
            date_filter = Q()
        
        # User ke total dares
        user_dares = Dare_project.objects.filter(date_filter)
        if hasattr(Dare_project, 'created_by'):
            user_dares = user_dares.filter(created_by=user)
        
        total_dares = user_dares.count()
        
        # Points calculation (dummy data for now - tum apne hisab se modify kar sakte ho)
        difficulty_points = {
            'Easy': 10,
            'Moderate': 25,
            'Hard': 50,
            'Extreme': 100
        }
        
        total_points = 0
        for dare in user_dares:
            total_points += difficulty_points.get(dare.difficulty, 25)
        
        # Success rate (dummy calculation)
        success_rate = min(85 + (total_dares * 2), 100)  # Higher dares = better success rate
        
        # Current user ka position nikalna
        all_users_data = get_all_users_with_points(period)
        current_position = 1
        for i, user_data in enumerate(all_users_data):
            if user_data['user'] == user:
                current_position = i + 1
                break
        
        return {
            'position': current_position,
            'total_points': total_points,
            'total_dares': total_dares,
            'success_rate': success_rate,
            'avatar_letter': user.first_name[0].upper() if user.first_name else user.username[0].upper()
        }
    except:
        # Agar koi error aaye to default data return kar do
        return {
            'position': 47,
            'total_points': 2840,
            'total_dares': 47,
            'success_rate': 87,
            'avatar_letter': user.username[0].upper()
        }

def get_all_users_with_points(period):
    """All users ke points calculate karne ke liye"""
    try:
        from postdare.models import Dare_project
        
        # Period ke according date filter
        if period == 'weekly':
            start_date = timezone.now() - timedelta(days=7)
            date_filter = Q(created_at__gte=start_date) if hasattr(Dare_project, 'created_at') else Q()
        elif period == 'monthly':
            start_date = timezone.now() - timedelta(days=30)
            date_filter = Q(created_at__gte=start_date) if hasattr(Dare_project, 'created_at') else Q()
        else:  # alltime
            date_filter = Q()
        
        users_data = []
        all_users = User.objects.all()
        
        difficulty_points = {
            'Easy': 10,
            'Moderate': 25,
            'Hard': 50,
            'Extreme': 100
        }
        
        for user in all_users:
            user_dares = Dare_project.objects.filter(date_filter)
            if hasattr(Dare_project, 'created_by'):
                user_dares = user_dares.filter(created_by=user)
            
            total_points = 0
            total_dares = user_dares.count()
            
            for dare in user_dares:
                total_points += difficulty_points.get(dare.difficulty, 25)
            
            if total_points > 0:  # Sirf unhi users ko include karo jinke points hain
                users_data.append({
                    'user': user,
                    'total_points': total_points,
                    'total_dares': total_dares,
                })
        
        # Points ke hisab se sort karo
        users_data.sort(key=lambda x: x['total_points'], reverse=True)
        return users_data
        
    except:
        # Agar model nahi mila to dummy data return karo
        return []

def get_top_users(period, limit=10, offset=0):
    """Top users nikalne ke liye function"""
    try:
        all_users_data = get_all_users_with_points(period)
        
        # Offset aur limit apply karo
        selected_users = all_users_data[offset:offset+limit]
        
        leaderboard_data = []
        for i, user_data in enumerate(selected_users):
            user = user_data['user']
            
            # Success rate calculation (dummy)
            success_rate = min(75 + (user_data['total_dares'] * 2), 100)
            wins = int(user_data['total_dares'] * (success_rate / 100))
            
            leaderboard_data.append({
                'rank': offset + i + 1,
                'name': user.get_full_name() or user.username,
                'username': f"@{user.username}",
                'points': user_data['total_points'],
                'total_dares': user_data['total_dares'],
                'wins': wins,
                'avatar_letter': user.first_name[0].upper() if user.first_name else user.username[0].upper(),
                'user_obj': user
            })
        
        return leaderboard_data
        
    except Exception as e:
        print(f"Error in get_top_users: {e}")
        # Agar koi error aaye to dummy data return karo
        dummy_users = [
            {'rank': offset+1, 'name': 'Alex Thunder', 'username': '@alex_thunder', 'points': 12340, 'total_dares': 89, 'wins': 76, 'avatar_letter': 'A'},
            {'rank': offset+2, 'name': 'Maya Storm', 'username': '@maya_storm', 'points': 8450, 'total_dares': 72, 'wins': 65, 'avatar_letter': 'M'},
            {'rank': offset+3, 'name': 'Jake Blaze', 'username': '@jake_blaze', 'points': 7890, 'total_dares': 68, 'wins': 61, 'avatar_letter': 'J'},
        ]
        return dummy_users[:limit]

def get_category_wise_leaders():
    """Category wise top users nikalne ke liye"""
    try:
        from postdare.models import Dare_project
        
        categories = {
            'adventure': {'name': 'Adventure', 'icon': '🌍', 'users': []},
            'fitness': {'name': 'Fitness', 'icon': '💪', 'users': []},
            'creative': {'name': 'Creative', 'icon': '🎨', 'users': []},
        }
        
        difficulty_points = {
            'Easy': 10,
            'Moderate': 25,
            'Hard': 50,
            'Extreme': 100
        }
        
        # Har category ke liye top users nikalo
        for category_key, category_info in categories.items():
            category_users = []
            
            # Is category ke dares find karo
            category_dares = Dare_project.objects.filter(
                category__icontains=category_info['name']
            )
            
            # Har user ke liye is category mein points calculate karo
            for user in User.objects.all():
                user_category_dares = category_dares
                if hasattr(Dare_project, 'created_by'):
                    user_category_dares = user_category_dares.filter(created_by=user)
                
                total_points = 0
                for dare in user_category_dares:
                    total_points += difficulty_points.get(dare.difficulty, 25)
                
                if total_points > 0:
                    category_users.append({
                        'user': user,
                        'points': total_points,
                        'name': user.get_full_name() or user.username,
                        'avatar_letter': user.first_name[0].upper() if user.first_name else user.username[0].upper()
                    })
            
            # Points ke hisab se sort karo aur top 3 lo
            category_users.sort(key=lambda x: x['points'], reverse=True)
            categories[category_key]['users'] = category_users[:3]
        
        return categories
        
    except Exception as e:
        print(f"Error in category leaders: {e}")
        # Dummy data return karo agar error aaye
        return {
            'adventure': {
                'name': 'Adventure', 
                'icon': '🌍', 
                'users': [
                    {'name': 'Sarah Quest', 'points': 3240, 'avatar_letter': 'S'},
                    {'name': 'David Explorer', 'points': 2890, 'avatar_letter': 'D'},
                    {'name': 'Luna Wild', 'points': 2650, 'avatar_letter': 'L'},
                ]
            },
            'fitness': {
                'name': 'Fitness', 
                'icon': '💪', 
                'users': [
                    {'name': 'Mike Power', 'points': 4120, 'avatar_letter': 'M'},
                    {'name': 'Emma Fit', 'points': 3780, 'avatar_letter': 'E'},
                    {'name': 'Ryan Strong', 'points': 3450, 'avatar_letter': 'R'},
                ]
            },
            'creative': {
                'name': 'Creative', 
                'icon': '🎨', 
                'users': [
                    {'name': 'Aria Artist', 'points': 3890, 'avatar_letter': 'A'},
                    {'name': 'Zoe Creative', 'points': 3560, 'avatar_letter': 'Z'},
                    {'name': 'Ben Maker', 'points': 3230, 'avatar_letter': 'B'},
                ]
            },
        }