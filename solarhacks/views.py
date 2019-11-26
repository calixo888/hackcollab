from django.shortcuts import render
from . import models, forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from random import randint
import json

# Function to create random ID for users and teams
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def index(request):
    return render(request, "solarhacks/index.html")

def register(request):
    # Check if form was submitted
    if request.method == "POST":
        # Shortcut variable
        data = request.POST

        # Grabbing all form data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        birthday = data.get("birthday")
        school = data.get("school")
        gender = data.get("gender")
        email = data.get("email")
        phone_number = data.get("phone_number")
        notification_type = data.get("notification_type")
        areas_of_expertise = data.get("areas_of_expertise")
        past_accomplishments = data.get("past_accomplishments")
        github_link = data.get("github_link")
        linkedin_link = data.get("linkedin_link")
        personal_website_link = data.get("personal_website_link")
        profile_picture = data.get("profile_picture")
        looking_to_join = data.get("looking_to_join")

        # Modifying looking_to_join variable - default returns "on"/"off"
        if looking_to_join == "on":
            looking_to_join = True
        else:
            looking_to_join = False

        username = data.get("username")
        password = data.get("password")
        communication = data.get("communication")
        public_speaking = data.get("public_speaking")
        teamwork = data.get("teamwork")
        leadership = data.get("leadership")

        # Creating and saving default User
        user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        user.set_password(password)
        user.save()

        # Creating and saving user profile - linked to User
        profile = models.UserProfile(user=user, id=random_with_N_digits(8), birthday=birthday, school=school, gender=gender, phone_number=phone_number, notification_type=notification_type, areas_of_expertise=areas_of_expertise, past_accomplishments=past_accomplishments, github_link=github_link, linkedin_link=linkedin_link, personal_website_link=personal_website_link, profile_picture=profile_picture, looking_to_join=looking_to_join, communication=communication, public_speaking=public_speaking, teamwork=teamwork, leadership=leadership)

        profile.save()

        login(request, user)

        return HttpResponseRedirect("/")

    form = forms.UserForm()

    return render(request, "solarhacks/register.html", context={"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                print("Inactive account")
        else:
            print("Invalid credentials")

    return render(request, "solarhacks/login.html")

@login_required(login_url="/login/")
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required(login_url="/login/")
def competitors(request):
    # Loads and displays all competitors within hackathon circle
    competitors = models.UserProfile.objects.all()
    return render(request, "solarhacks/competitors.html", context={"competitors": competitors})

@login_required(login_url="/login/")
def create_team(request):
    if request.method == "POST":
        data = request.POST

        # Getting data from form
        name = data.get("name")
        description = data.get("description")

        # Creating team with unique and branded ID
        team = models.Team(id="team-" + str(random_with_N_digits(8)), name=name, description=description, leader=request.user.profile.id)
        team.save()

        # Getting currently authenticated user and setting their team_id to team created
        user = models.UserProfile.objects.get(user=request.user)
        user.team_id = team.id
        user.save()

        return HttpResponseRedirect("/")

    return render(request, "solarhacks/create_team.html")

@login_required(login_url="/login/")
def teams(request):
    # Loading and displaying all teams
    teams = {}

    for team in models.Team.objects.all():
        id = team.id
        teammates = []
        for user in models.UserProfile.objects.all():
            if user.team_id == id:
                teammates.append(user)

        teams[team] = teammates

    return render(request, "solarhacks/teams.html", context={"teams": teams})

@login_required(login_url="/login/")
def notifications(request):
    notifications = models.Notification.objects.filter(target_id=request.user.profile.id)

    return render(request, "solarhacks/notifications.html", context={"notifications": notifications})


@login_required(login_url="/login/")
def view_profile(request, user_id):
    profile = models.UserProfile.objects.get(id=user_id)
    context = {"profile": profile}

    if profile.team_id:
        team = models.Team.objects.get(id=profile.team_id)
        context["team"] = team
    return render(request, "solarhacks/profile.html", context=context)

@login_required(login_url="/login/")
def view_team(request, team_id):
    team = models.Team.objects.get(id=team_id)

    if request.user.profile.team_id == team.id:
        team = models.Team.objects.get(id=team_id)

        # Loading all notifications for the team
        notifications = {}
        for notification in models.Notification.objects.filter(target_id=team_id):
            notifications[notification] = models.UserProfile.objects.get(id=notification.source_id)

        return render(request, "solarhacks/team.html", context={
            "team": team,
            "leader": models.UserProfile.objects.get(id=team.leader),
            "notifications": notifications
        })
    else:
        # Return error if user is not part of the team
        return HttpResponse("You are not on this team.")

@login_required(login_url="/login/")
def join_team(request, team_id):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        # Source_id = user_id; target_id = team_id
        source_id = request.user.profile.id
        target_id = team_id

        notification = models.Notification(id="notification-" + str(random_with_N_digits(8)), title=title, description=description, source_id=source_id, target_id=target_id)
        notification.save()
        return HttpResponseRedirect("/")

    return render(request, "solarhacks/join_team.html")

@login_required(login_url="/login/")
def leave_team(request, team_id):
    # Getting current user and setting team_id to null
    profile = models.UserProfile.objects.get(user=request.user)
    profile.team_id = None
    profile.save()

    # Removing team if no one else is in it
    if not models.UserProfile.objects.filter(team_id=team_id):
        models.Team.objects.get(id=team_id).delete()

    return HttpResponseRedirect("/")

@login_required(login_url="/login/")
def invite_to_team(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        # Source_id = user_id; target_id = team_id
        source_id = request.GET.get("team_id")
        target_id = request.GET.get("user_id")

        notification = models.Notification(id="notification-" + str(random_with_N_digits(8)), title=title, description=description, source_id=source_id, target_id=target_id)
        notification.save()
        return HttpResponseRedirect("/")

    return render(request, "solarhacks/invite_to_team.html")

@login_required(login_url="/login/")
def accept_user(request):
    # Grabbing query parameters
    notification_id = request.GET.get("notification_id")
    user_id = request.GET.get("user_id")
    team_id = request.GET.get("team_id")

    # Deleting notification
    notification = models.Notification.objects.get(id=notification_id)
    notification.delete()

    # Creating notification for user
    notification = models.Notification(id="notification-" + str(random_with_N_digits(8)), title="Accepted into " + team.name, description="Congrats!", source_id=team_id, target_id=user_id)
    notification.save()

    # Adding user to team
    profile = models.UserProfile.objects.get(id=user_id)
    profile.team_id = team_id
    profile.save()

    return HttpResponseRedirect("/")

@login_required(login_url="/login/")
def reject_user(request):
    # Grabbing query parameters
    notification_id = request.GET.get("notification_id")
    user_id = request.GET.get("user_id")
    team_id = request.GET.get("team_id")

    team = models.Team.objects.get(id=team_id)

    # Deleting notification
    notification = models.Notification.objects.get(id=notification_id)
    notification.delete()

    # Creating notification for user
    notification = models.Notification(id="notification-" + str(random_with_N_digits(8)), title="Rejected from " + team.name, description="We're sorry", source_id=team_id, target_id=user_id)
    notification.save()

    return HttpResponseRedirect("/")

@login_required(login_url="/login/")
def accept_invite(request):
    # Grabbing query parameters
    notification_id = request.GET.get("notification_id")
    user_id = request.GET.get("user_id")
    team_id = request.GET.get("team_id")

    # Adding user to team
    profile = models.UserProfile.objects.get(id=user_id)
    profile.team_id = team_id
    profile.save()

    # Deleting notification
    notification = models.Notification.objects.get(id=notification_id)
    notification.delete()

    # Creating notification for team
    notification = models.Notification(id="notification-" + str(random_with_N_digits(8)), title=profile.user.username + " accepted invite!", description="Invitation accepted!", source_id=user_id, target_id=team_id)
    notification.save()

    return HttpResponseRedirect("/")

@login_required(login_url="/login/")
def reject_invite(request):
    # Grabbing query parameters
    notification_id = request.GET.get("notification_id")
    user_id = request.GET.get("user_id")
    team_id = request.GET.get("team_id")

    # Deleting notification
    notification = models.Notification.objects.get(id=notification_id)
    notification.delete()

    profile = models.UserProfile.objects.get(id=user_id)

    # Creating notification for team
    notification = models.Notification(id="notification-" + str(random_with_N_digits(8)), title=profile.user.username + " rejected team invitation.", description="Invitation rejected.", source_id=user_id, target_id=team_id)
    notification.save()

    return HttpResponseRedirect("/")
