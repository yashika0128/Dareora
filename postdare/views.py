from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Dare_project
from django.contrib import messages
import google.generativeai as genai
from django.conf import settings
import traceback

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

#==================gen ai wala python ka function jisse coll karege=============

def analyze_dare_with_gemini(dare_text, description):
    """
    Gemini AI se dare analyze karne ke liye function banaya he mene
    """
    model = genai.GenerativeModel('models/gemini-2.0-flash')

    prompt = f"""
    Analyze this dare:
    Title: "{dare_text}"
    Description: "{description}"
    
    Please do the following:
    1. Check if it contains abusive, illegal, or extremely dangerous content. Reply with 'REJECT' or 'ACCEPT'
    2. If ACCEPT, rewrite the description to make it more creative, exciting, and engaging while keeping the original intent.
    3. Format your response as:
    STATUS: [ACCEPT/REJECT]
    ENHANCED_DESCRIPTION: [Your enhanced description here]
    """

    try:
        response = model.generate_content(prompt)
        reply = response.candidates[0].content.parts[0].text.strip()
        return reply
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None

#=========================================create dare=======================================
@login_required
def postdare(request, id=None):
    if id:
        # Edit karne ke liye
        dare = get_object_or_404(Dare_project, id=id)
        # Security check - user can only edit their own dares
        if dare.user != request.user:
            messages.error(request, "You can only edit your own dares!")
            return redirect("explore")
    else:
        # Create Mode 
        dare = None

    if request.method == "POST":
        dare_title = request.POST.get("dare_title")
        description = request.POST.get("description")
        time_limit = request.POST.get("time_limit")
        category = request.POST.get("category")
        use_ai = request.POST.get("use_ai")  # Checkbox jisse user se puch sake kya vo gen ai se inhancement karna chahega

        # Validation
        if not dare_title or not description or not category:
            messages.error(request, "Please fill all required fields!")
            return render(request, "postdare.html", {'dare': dare})

        # AI Enhancement (only for new dares and if user opts in)
        enhanced_description = description
        if use_ai and not dare:  # sirf naye dares ke liye check karega ki kuch gaali ya ganda dare to nahi he
            try:
                ai_response = analyze_dare_with_gemini(dare_title, description)
                
                if ai_response:
                    lines = ai_response.split('\n')
                    status_line = next((line for line in lines if 'STATUS:' in line), '')
                    
                    if 'REJECT' in status_line:
                        messages.error(request, "This dare contains inappropriate content and cannot be posted!")
                        return render(request, "postdare.html", {'dare': dare})
                    
                    # inhancement nikalne ke liye 
                    enhanced_desc_line = next((line for line in lines if 'ENHANCED_DESCRIPTION:' in line), '')
                    if enhanced_desc_line:
                        enhanced_description = enhanced_desc_line.replace('ENHANCED_DESCRIPTION:', '').strip()
                        messages.info(request, "Your dare has been enhanced using AI!")
                
            except Exception as e:
                print(f"AI Enhancement Error: {e}")
                traceback.print_exc()
                messages.warning(request, "AI enhancement failed, using original description.")

        if dare:
            # Update pehle se dare jo he
            dare.dare_title = dare_title
            dare.description = enhanced_description
            dare.time_limit = time_limit if time_limit else None
            dare.category = category
            dare.save()
            messages.success(request, "Dare Updated Successfully!")
            print(f"Dare Updated: {dare.dare_title}")
        else:
            # Create New Dare - YAHAN USER ASSIGN KARNA ZAROORI HAI
            new_dare = Dare_project.objects.create(
                user=request.user,  # ⭐ YE LINE ADD KIYA HAI - Current logged in user assign kar rahe hain
                dare_title=dare_title,
                description=enhanced_description,
                time_limit=time_limit if time_limit else None,
                category=category
            )
            messages.success(request, "New Dare Posted Successfully!")
            print(f"New Dare Created: {new_dare.dare_title} in category: {new_dare.category} by user: {request.user.username}")
        
        return redirect("explore")

    return render(request, "postdare.html", {'dare': dare})

# ========================================delete dare=========================
@login_required
def delete_dare(request, id):
    dare = get_object_or_404(Dare_project, id=id)
    
    # Security check - user can only delete their own dares
    if dare.user != request.user:
        messages.error(request, "You can only delete your own dares!")
        return redirect('explore')
    
    category = dare.category
    dare_title = dare.dare_title  # Store title before deletion
    dare.delete()
    messages.success(request, f"Dare '{dare_title}' deleted successfully!")
    return redirect('category_dares', category_slug=category)