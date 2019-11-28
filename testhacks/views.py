from django.shortcuts import render
from . import models, forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import EmailMessage
from random import randint
import json
import datetime

# Function to create random ID for users and teams
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def index(request):
    return render(request, "testhacks/index.html")

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
        # notification_type = data.get("notification_type")
        areas_of_expertise = data.get("areas_of_expertise")
        past_accomplishments = data.get("past_accomplishments")
        github_link = data.get("github_link")
        linkedin_link = data.get("linkedin_link")
        personal_website_link = data.get("personal_website_link")
        profile_picture = data.get("profile_picture")
        username = data.get("username")
        password = data.get("password")
        communication = data.get("communication")
        public_speaking = data.get("public-speaking")
        teamwork = data.get("teamwork")
        leadership = data.get("leadership")

        # Modifying birthday to correct date format
        birthday = datetime.datetime.strptime(birthday, '%m/%d/%Y').strftime('%Y-%m-%d')

        # Creating and saving default User
        user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        user.set_password(password)
        user.save()

        # Creating and saving user profile - linked to User
        profile = models.UserProfile(user=user, id=random_with_N_digits(8), birthday=birthday, school=school, gender=gender, phone_number=phone_number, areas_of_expertise=areas_of_expertise, past_accomplishments=past_accomplishments, github_link=github_link, linkedin_link=linkedin_link, personal_website_link=personal_website_link, profile_picture=profile_picture, communication=communication, public_speaking=public_speaking, teamwork=teamwork, leadership=leadership)

        # Grabbing profile picture
        if 'profile_picture' in request.FILES: # checking if they provided picture
            profile.profile_picture = request.FILES['profile_picture']

        else:
            profile.profile_picture = "default.png"

        profile.save()

        login(request, user)

        messages.success(request, "Account successfully created.")

        return HttpResponseRedirect("/")

    form = forms.UserForm()

    return render(request, "testhacks/register.html", context={"form": form})

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
            messages.success(request, "Invalid credentials. Please try again.")

    return render(request, "testhacks/login.html")

@login_required(login_url="/login/")
def user_logout(request):
    logout(request)
    messages.success(request, "Successfully logged out.")
    return HttpResponseRedirect("/")

@login_required(login_url="/login/")
def update(request):
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
        # notification_type = data.get("notification_type")
        areas_of_expertise = data.get("areas_of_expertise")
        past_accomplishments = data.get("past_accomplishments")
        github_link = data.get("github_link")
        linkedin_link = data.get("linkedin_link")
        personal_website_link = data.get("personal_website_link")
        profile_picture = data.get("profile_picture")
        username = data.get("username")
        communication = data.get("communication")
        public_speaking = data.get("public-speaking")
        teamwork = data.get("teamwork")
        leadership = data.get("leadership")

        # Modifying birthday to correct date format
        birthday = datetime.datetime.strptime(birthday, '%m/%d/%Y').strftime('%Y-%m-%d')

        # Updating and saving user profile - linked to User
        profile = models.UserProfile.objects.get(user=request.user)
        profile.user.first_name = first_name
        profile.user.last_name = last_name
        profile.user.email = email
        profile.user.username = username
        profile.birthday = birthday
        profile.school = school
        profile.gender = gender
        profile.phone_number = phone_number
        profile.areas_of_expertise = areas_of_expertise
        profile.past_accomplishments = past_accomplishments
        profile.github_link = github_link
        profile.linkedin_link = linkedin_link
        profile.personal_website_link = personal_website_link
        profile.communication = communication
        profile.public_speaking = public_speaking
        profile.teamwork = teamwork
        profile.leadership = leadership

        # Grabbing profile picture
        if 'profile_picture' in request.FILES: # checking if they provided picture
            profile.profile_picture = request.FILES['profile_picture']

        else:
            profile.profile_picture = "default.png"

        profile.save()

        messages.success(request, "Account successfully updated.")

        return HttpResponseRedirect("/")

    # Setting form values to automatically fill
    form = forms.UserForm(initial={
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "username": request.user.username,
        "birthday": datetime.datetime.strptime(str(request.user.testhacks_profile.birthday), '%Y-%m-%d').strftime('%m/%d/%Y'),
        "school": request.user.testhacks_profile.school,
        "gender": request.user.testhacks_profile.gender,
        "phone_number": request.user.testhacks_profile.phone_number,
        "areas_of_expertise": request.user.testhacks_profile.areas_of_expertise,
        "past_accomplishments": request.user.testhacks_profile.past_accomplishments,
        "github_link": request.user.testhacks_profile.github_link,
        "linkedin_link": request.user.testhacks_profile.linkedin_link,
        "personal_website_link": request.user.testhacks_profile.personal_website_link,
        "profile_picture": request.user.testhacks_profile.profile_picture,
    })

    return render(request, "testhacks/update.html", context={
        "form": form,
        # Adding in soft skill values to manually add to form in HTML file
        "communication": request.user.testhacks_profile.communication,
        "public_speaking": request.user.testhacks_profile.public_speaking,
        "teamwork": request.user.testhacks_profile.teamwork,
        "leadership": request.user.testhacks_profile.leadership,
    })

@login_required(login_url="/login/")
def competitors(request):
    # Loads and displays all competitors within hackathon circle
    competitors = models.UserProfile.objects.all()
    return render(request, "testhacks/competitors.html", context={"competitors": competitors})

@login_required(login_url="/login/")
def create_team(request):
    if request.method == "POST":
        data = request.POST

        # Getting data from form
        name = data.get("name")
        description = data.get("description")

        # Creating team with unique and branded ID
        team = models.Team(id="team-" + str(random_with_N_digits(8)), name=name, description=description)
        team.save()

        # Getting currently authenticated user and setting their team_id to team created
        user = models.UserProfile.objects.get(user=request.user)
        user.team_id = team.id
        user.save()

        messages.success(request, "Team successfully created.")

        return HttpResponseRedirect("/")

    return render(request, "testhacks/create_team.html")

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

    return render(request, "testhacks/teams.html", context={"teams": teams})

@login_required(login_url="/login/")
def notifications(request):
    notifications = models.Notification.objects.filter(target_id=request.user.testhacks_profile.id)

    return render(request, "testhacks/notifications.html", context={"notifications": notifications})


@login_required(login_url="/login/")
def view_profile(request, user_id):
    profile = models.UserProfile.objects.get(id=user_id)
    context = {"profile": profile}

    if profile.team_id:
        team = models.Team.objects.get(id=profile.team_id)
        context["team"] = team
    return render(request, "testhacks/profile.html", context=context)

@login_required(login_url="/login/")
def view_team(request, team_id):
    team = models.Team.objects.get(id=team_id)

    if request.user.testhacks_profile.team_id == team.id:
        team = models.Team.objects.get(id=team_id)

        # Loading all notifications for the team
        notifications = {}
        for notification in models.Notification.objects.filter(target_id=team_id):
            notifications[notification] = models.UserProfile.objects.get(id=notification.source_id)

        # Loading all members
        teammates = []
        for user in models.UserProfile.objects.all():
            if user.team_id == team_id:
                teammates.append(user)

        return render(request, "testhacks/team.html", context={
            "team": team,
            "teammates": teammates,
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
        source_id = request.user.testhacks_profile.id
        target_id = team_id

        notification = models.Notification(id="notification-" + str(random_with_N_digits(8)), title=title, description=description, source_id=source_id, target_id=target_id, type="action")
        notification.save()

        # Sending email to each member of team
        for profile in models.UserProfile.objects.filter(team_id=team_id):
            email = profile.user.email
            EmailMessage("Join Team Request", "Please view your team page for more information", to=[email]).send()

        messages.success(request, "Join Team request successfully sent!")

        return HttpResponseRedirect("/")

    return render(request, "testhacks/join_team.html")

@login_required(login_url="/login/")
def leave_team(request, team_id):
    # Getting current user and setting team_id to null
    profile = models.UserProfile.objects.get(user=request.user)
    profile.team_id = None
    profile.save()

    # Removing team if no one else is in it
    if not models.UserProfile.objects.filter(team_id=team_id):
        models.Team.objects.get(id=team_id).delete()

    # Sending email to whole team
    for temp_profile in models.UserProfile.objects.filter(team_id=team_id):
        email = temp_profile.user.email
        EmailMessage(profile.user.username + " has the left the team", "Please view your team page for more information", to=[email]).send()

    messages.success(request, "Team successfully left.")

    return HttpResponseRedirect("/")

@login_required(login_url="/login/")
def invite_to_team(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        # Source_id = user_id; target_id = team_id
        source_id = request.GET.get("team_id")
        target_id = request.GET.get("user_id")

        notification = models.Notification(id="notification-" + str(random_with_N_digits(8)), title=title, description=description, source_id=source_id, target_id=target_id, type="action")
        notification.save()

        # Sending email to user
        profile = models.UserProfile.objects.get(id=target_id)
        email = profile.user.email
        print(email)
        email_message = EmailMessage("Team invitation received", "Please view your team page for more information", to=[email])
        email_message.send()

        messages.success(request, "Team invitation successfully sent!")

        return HttpResponseRedirect("/")

    return render(request, "testhacks/invite_to_team.html")

@login_required(login_url="/login/")
def accept_user(request):
    # Grabbing query parameters
    notification_id = request.GET.get("notification_id")
    user_id = request.GET.get("user_id")
    team_id = request.GET.get("team_id")

    team = models.Team.objects.get(id=team_id)

    # Deleting notification
    notification = models.Notification.objects.get(id=notification_id)
    notification.delete()

    # Creating notification for user
    notification = models.Notification(id="notification-" + str(random_with_N_digits(8)), title="Accepted into " + team.name, description="Congrats!", source_id=team_id, target_id=user_id, type="info")
    notification.save()

    profile = models.UserProfile.objects.get(id=user_id)
    email = profile.user.email
    EmailMessage("Join Team Request Accepted!", "Please view your team page for more information", to=[email]).send()

    # Adding user to team
    profile = models.UserProfile.objects.get(id=user_id)
    profile.team_id = team_id
    profile.save()

    messages.success(request, "User successfully accepted into team!")

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
    notification = models.Notification(id="notification-" + str(random_with_N_digits(8)), title="Rejected from " + team.name, description="We're sorry", source_id=team_id, target_id=user_id, type="info")
    notification.save()

    # Sending email to user
    profile = models.UserProfile.objects.get(id=user_id)
    email = profile.user.email
    EmailMessage("Join Team Request Rejected", "Please view your team page for more information", to=[email]).send()

    messages.success(request, "Team invitations successfully rejected.")

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
    notification = models.Notification(id="notification-" + str(random_with_N_digits(8)), title=profile.user.username + " accepted invite!", description="Invitation accepted!", source_id=user_id, target_id=team_id, type="info")
    notification.save()

    # Sending email to each member of team
    for profile in models.UserProfile.objects.filter(team_id=team_id):
        email = profile.user.email
        EmailMessage("Team invitiation Accepted!", "Please view your team page for more information", to=[email]).send()

    messages.success(request, "Team invitation successfully accepted!")

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
    notification = models.Notification(id="notification-" + str(random_with_N_digits(8)), title=profile.user.username + " rejected team invitation.", description="Invitation rejected.", source_id=user_id, target_id=team_id, type="info")
    notification.save()

    # Sending email to each member of team
    for profile in models.UserProfile.objects.filter(team_id=team_id):
        email = profile.user.email
        EmailMessage("Team invitation rejected", "Please view your team page for more information", to=[email]).send()

    messages.success(request, "Team invite successfully rejected.")

    return HttpResponseRedirect("/")


# POST REQUEST
def delete_notification(request):
    notification_id = request.GET.get("id")

    models.Notification.objects.get(id=notification_id).delete()

    return JsonResponse({"value": "hi"})