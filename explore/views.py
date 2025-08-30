from django.shortcuts import render, redirect, get_object_or_404
from postdare.models import Dare_project
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def explore(request):
    # Get all distinct categories
    categories = Dare_project.objects.values_list('category', flat=True).distinct()
    
    # Debug: Print categories to console
    print(f"Categories found: {list(categories)}")
    print(f"Total dares in database: {Dare_project.objects.count()}")
    
    return render(request, "explore.html", {'categories': categories})

@login_required
def category_dares(request, category_slug):
    # Get dares for specific category
    dares = Dare_project.objects.filter(category__iexact=category_slug).order_by('-id')
    
    # Debug: Print dares found
    print(f"Dares found for category '{category_slug}': {dares.count()}")
    for dare in dares:
        print(f"- {dare.dare_title}")
    
    return render(request, 'category_dares.html', {
        'dares': dares, 
        'category': category_slug
    })

@login_required
def update_dare(request, dare_id):
    dare = get_object_or_404(Dare_project, id=dare_id)
    if request.method == "POST":
        dare.dare_title = request.POST.get("dare_title")
        dare.description = request.POST.get("description")
        dare.time_limit = request.POST.get("time_limit")
        dare.category = request.POST.get("category")
        dare.save()
        messages.success(request, "Dare updated successfully!")
        return redirect('category_dares', category_slug=dare.category)
    return render(request, "postdare.html", {'dare': dare})

@login_required
def delete_dare(request, dare_id):
    dare = get_object_or_404(Dare_project, id=dare_id)
    category = dare.category
    messages.success(request, f"Dare '{dare.dare_title}' deleted successfully!")
    dare.delete()
    return redirect('category_dares', category_slug=category)