from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from .models import PrivateRoom, PrivateRoomDare
import uuid

@login_required
def edit_private_room_dare(request, room_uuid, dare_id):
    room = get_object_or_404(PrivateRoom, uuid=room_uuid)
    dare = get_object_or_404(PrivateRoomDare, id=dare_id, room=room)
    if request.user != dare.created_by:
        return HttpResponseForbidden("You can only edit your own dares.")
    if request.method == "POST":
        title = request.POST.get('dare_title', '').strip()
        description = request.POST.get('dare_description', '').strip()
        if title and description:
            dare.title = title
            dare.description = description
            dare.save()
            messages.success(request, "Dare updated successfully!")
            return redirect('private_room', room_uuid=room.uuid)
    context = {"room": room, "dare": dare, "room_link": request.build_absolute_uri(request.path)}
    return render(request, "edit_private_room_dare.html", context)

@login_required
def delete_private_room_dare(request, room_uuid, dare_id):
    room = get_object_or_404(PrivateRoom, uuid=room_uuid)
    dare = get_object_or_404(PrivateRoomDare, id=dare_id, room=room)
    if request.user != dare.created_by:
        return HttpResponseForbidden("You can only delete your own dares.")
    dare.delete()
    messages.success(request, "Dare deleted successfully!")
    return redirect('private_room', room_uuid=room.uuid)

@login_required
def accept_private_room_dare(request, room_uuid, dare_id):
    from .models import DareCompletion
    room = get_object_or_404(PrivateRoom, uuid=room_uuid)
    dare = get_object_or_404(PrivateRoomDare, id=dare_id, room=room)
    user = request.user
    if user == dare.created_by:
        # Only show edit/delete, no accept/upload for owner
        context = {"room": room, "dare": dare, "room_link": request.build_absolute_uri(request.path), "user": user}
        return render(request, "accept_private_room_dare.html", context)
    if request.method == "POST":
        notes = request.POST.get('completion_notes', '').strip()
        proof_file = request.FILES.get('proof_file')
        if proof_file:
            DareCompletion.objects.create(
                dare=dare,
                user=user,
                completion_notes=notes,
                proof_file=proof_file
            )
            messages.success(request, "Dare completion submitted!")
            return redirect('private_room', room_uuid=room.uuid)
        else:
            messages.error(request, "Please upload a proof file.")
    context = {"room": room, "dare": dare, "room_link": request.build_absolute_uri(request.path), "user": user}
    return render(request, "accept_private_room_dare.html", context)

# --- Imports ---
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from .models import PrivateRoom, PrivateRoomDare
import uuid

# --- Private Room Views ---
@login_required
def create_private_room(request):
    if request.method == "POST":
        room_name = request.POST.get('room_name', '').strip()
        member_usernames = request.POST.get('members', '').split(',')
        members = User.objects.filter(username__in=[u.strip() for u in member_usernames if u.strip()])
        room = PrivateRoom.objects.create(name=room_name, created_by=request.user)
        room.members.add(request.user)
        for member in members:
            room.members.add(member)
        room.save()
        return redirect('private_room', room_uuid=room.uuid)
    return render(request, "create_private_room.html")

@login_required
def private_room(request, room_uuid):
    room = get_object_or_404(PrivateRoom, uuid=room_uuid)
    if request.user not in room.members.all():
        return HttpResponseForbidden("You are not a member of this room.")
    if request.method == "POST":
        title = request.POST.get('dare_title', '').strip()
        description = request.POST.get('dare_description', '').strip()
        if title and description:
            PrivateRoomDare.objects.create(room=room, title=title, description=description, created_by=request.user)
    room_link = request.build_absolute_uri(request.path)
    context = {"room": room, "room_link": room_link}
    return render(request, "private_room.html", context)

@login_required
def accept_dare(request, dare_id):
    from postdare.models import Dare_project
    from .models import DareCompletion
    dare = get_object_or_404(Dare_project, id=dare_id)
    if request.method == "POST":
        notes = request.POST.get('completion_notes', '').strip()
        proof_file = request.FILES.get('proof_file')
        if proof_file:
            completion = DareCompletion.objects.create(
                dare=dare,
                user=request.user,
                completion_notes=notes,
                proof_file=proof_file
            )
            messages.success(request, "Dare completion submitted!")
            return redirect('dashboard_home')
        else:
            messages.error(request, "Please upload a proof file.")
    return render(request, "accept_dare.html", {"dare": dare})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
@login_required
def user_profile(request):
    user = request.user
    bio = request.session.get('user_bio', "Professional dare-devil and challenge enthusiast. Always up for the next adventure! 🚀")
    location = getattr(user, 'location', None) or request.session.get('user_location', '')
    if request.method == "POST":
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        bio = request.POST.get('bio', '').strip()
        location = request.POST.get('location', '').strip()
        user.first_name = first_name
        user.last_name = last_name
        # Save location if User model has it, else save to session
        if hasattr(user, 'location'):
            user.location = location
        user.save()
        request.session['user_bio'] = bio
        request.session['user_location'] = location
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
    context = {
        'profile_user': user,
        'is_own_profile': True,
        'bio': bio,
        'location': location,
    }
    return render(request, "profile.html", context)

def network(request):
    return render(request, "network.html")