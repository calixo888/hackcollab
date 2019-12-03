from django.shortcuts import render
from . import models, forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.utils.safestring import mark_safe
from random import randint
import json
import datetime
import os
import shutil

# Markdown/HTML libraries
import markdown2
import html2markdown

# Global variables
team_limit = 4

# Function to create random ID for users and teams
def random_with_N_digits(n):
    # Getting all IDs used
    ids = list(models.ID.objects.all())

    # Looping until unique ID is generated
    while True:
        # Generating ID
        range_start = 10**(n-1)
        range_end = (10**n)-1
        id = randint(range_start, range_end)

        # Breaking loop in ID is not used before
        if not id in ids:
            break

    # Saving ID to database
    id_model = models.ID(generated_id=id)
    id_model.save()

    # Returning ID
    return id

def index(request):
    return render(request, "hackathon/index.html")

def register(request):
    # Check if form was submitted
    if request.method == "POST":
        # Shortcut variable
        data = request.POST

        # Grabbing all form data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        birthday = data.get("birthday")
        title = data.get("title")
        gender = data.get("gender")
        email = data.get("email")
        phone_number = data.get("phone_number")
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

        # Checking if username is taken
        if not User.objects.filter(username=username).exists():
            # Checking if email is taken
            if not User.objects.filter(email=email).exists():
                # Modifying birthday to correct date format
                birthday = datetime.datetime.strptime(birthday, '%m/%d/%Y').strftime('%Y-%m-%d')

                # Creating and saving default User
                user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                user.set_password(password)
                user.save()

                # Creating and saving user profile - linked to User
                profile = models.UserProfile(user=user, id=random_with_N_digits(8), birthday=birthday, title=title, gender=gender, phone_number=phone_number, areas_of_expertise=areas_of_expertise, past_accomplishments=past_accomplishments, github_link=github_link, linkedin_link=linkedin_link, personal_website_link=personal_website_link, profile_picture=profile_picture, communication=communication, public_speaking=public_speaking, teamwork=teamwork, leadership=leadership)

                # Getting current hackathon from subdomain
                hackathon_name = request.get_host().split(".")[0]
                hackathon = models.Hackathon.objects.get(name=hackathon_name)

                # Creating hackathon identification
                hid = models.HackathonIdentification(hackathon_name=hackathon.name, model_id=profile.id)
                hid.save()

                # Grabbing profile picture
                if 'profile_picture' in request.FILES: # checking if they provided picture
                    profile.profile_picture = request.FILES['profile_picture']

                else:
                    filename = "default-" + username + ".png"
                    media_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/media/"
                    shutil.copyfile(media_dir + "default.png", media_dir + filename)
                    profile.profile_picture = filename

                profile.save()

                login(request, user)

                messages.success(request, "Account successfully created.")

                return HttpResponseRedirect("/")

            else:
                messages.success(request, "Your email is already taken. Please enter a different one.")

        else:
            messages.success(request, "Your username is already taken. Please enter a different one.")

    form = forms.UserForm()

    return render(request, "hackathon/register.html", context={"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)

                # Register user into hackathon if they aren't already
                # Getting current hackathon from subdomain
                hackathon_name = request.get_host().split(".")[0]

                # Getting HID
                hid = models.HackathonIdentification.objects.filter(hackathon_name=hackathon_name, model_id=user.profile.id)

                if not hid:
                    hid = models.HackathonIdentification(hackathon_name=hackathon_name, model_id=user.profile.id)
                    hid.save()

                return HttpResponseRedirect("/")
            else:
                messages.success(request, "Your account has be deactivated. Please re-register.")
        else:
            messages.success(request, "Invalid credentials. Please try again.")

    return render(request, "hackathon/login.html")

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
        title = data.get("title")
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
        "birthday": datetime.datetime.strptime(str(request.user.profile.birthday), '%Y-%m-%d').strftime('%m/%d/%Y'),
        "school": request.user.profile.school,
        "gender": request.user.profile.gender,
        "phone_number": request.user.profile.phone_number,
        "areas_of_expertise": request.user.profile.areas_of_expertise,
        "past_accomplishments": request.user.profile.past_accomplishments,
        "github_link": request.user.profile.github_link,
        "linkedin_link": request.user.profile.linkedin_link,
        "personal_website_link": request.user.profile.personal_website_link,
        "profile_picture": request.user.profile.profile_picture,
    })

    return render(request, "hackathon/update.html", context={
        "form": form,
        # Adding in soft skill values to manually add to form in HTML file
        "communication": request.user.profile.communication,
        "public_speaking": request.user.profile.public_speaking,
        "teamwork": request.user.profile.teamwork,
        "leadership": request.user.profile.leadership,
    })

@login_required(login_url="/login/")
def competitors(request):
    # Getting current hackathon from subdomain
    hackathon_name = request.get_host().split(".")[0]

    # Get all models within hackathon
    hids = models.HackathonIdentification.objects.filter(hackathon_name=hackathon_name)
    hackathon_competitors = []
    for hid in hids:
        if not hid.model_id.startswith("t") and not hid.model_id.startswith("n"):
            competitor = models.UserProfile.objects.get(id=hid.model_id)
            if competitor != request.user.profile:
                if not competitor.user.is_staff:
                    if not competitor.user.is_superuser:
                        hackathon_competitors.append(competitor)

    # Loads and displays all competitors within hackathon circle
    competitors = {}
    for competitor in hackathon_competitors:
        parameters = {}
        if competitor.team_id:
            team = models.Team.objects.get(id=competitor.team_id)
            parameters["team"] = team
        else:
            parameters["team"] = None

        if request.user.profile.team_id:
            if request.user.profile.team_id == competitor.team_id:
                parameters["invite"] = False
            else:
                parameters["invite"] = True
        else:
            parameters["invite"] = False

        team_members = models.UserProfile.objects.filter(team_id=request.user.profile.team_id)
        if len(team_members) >= team_limit:
            parameters["max"] = True
        else:
            parameters["max"] = False

        competitors[competitor] = parameters

    return render(request, "hackathon/competitors.html", context={"competitors": competitors})

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

        # Creating team identification
        tid = models.TeamIdentification(team_id=team.id, user_id=user.id)
        tid.save()

        # Getting current hackathon from subdomain
        hackathon_name = request.get_host().split(".")[0]
        hackathon = models.Hackathon.objects.get(name=hackathon_name)

        # Creating hackathon identification
        hid = models.HackathonIdentification(hackathon_name=hackathon.name, model_id=team.id)
        hid.save()

        messages.success(request, "Team successfully created.")

        return HttpResponseRedirect("/")

    return render(request, "hackathon/create_team.html")

@login_required(login_url="/login/")
def teams(request):
    # Getting current hackathon from subdomain
    hackathon_name = request.get_host().split(".")[0]

    # Get all models within hackathon
    hids = models.HackathonIdentification.objects.filter(hackathon_name=hackathon_name)
    hackathon_teams = []
    for hid in hids:
        if hid.model_id.startswith("t"):
            team = models.Team.objects.get(id=hid.model_id)
            hackathon_teams.append(team)

    # Loading and displaying all teams
    teams = {}

    for team in hackathon_teams:
        id = team.id
        teammates = []
        for user in models.UserProfile.objects.all():
            if user.team_id == id:
                teammates.append(user)

        teams[team] = teammates

    return render(request, "hackathon/teams.html", context={"teams": teams})

@login_required(login_url="/login/")
def notifications(request):
    # Getting current hackathon from subdomain
    hackathon_name = request.get_host().split(".")[0]

    # Get all models within hackathon
    hids = models.HackathonIdentification.objects.filter(hackathon_name=hackathon_name)
    hackathon_notifications = []
    for hid in hids:
        if hid.model_id.startswith("n"):
            notification = models.Notification.objects.get(id=hid.model_id)
            hackathon_notifications.append(notification)

    notifications = {}
    # Grabbing teams for each action notification
    for notification in hackathon_notifications:
        if notification.target_id == str(request.user.profile.id):
            if notification.type == "action" and notification.source_id:
                team = models.Team.objects.get(id=notification.source_id)
                notifications[notification] = team
            else:
                notifications[notification] = False

    return render(request, "hackathon/notifications.html", context={"notifications": notifications})

def contact_support(request):
    if request.method == "POST":
        # Grabbing information from contact us form
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Sending the email
        EmailMessage("HackCollab - " + request.get_host().split(".")[0] + " Contact Us", "From: " + name + "\n\n" + message + "\n\nEmail: " + email, to=["calix.huang1@gmail.com"]).send()

        # Redirecting to success page
        return HttpResponseRedirect("/success/")

    return render(request, "hackathon/contact_support.html")

def success(request):
    return render(request, "hackathon/success.html")

@login_required(login_url="/login/")
def view_profile(request, user_id):
    profile = models.UserProfile.objects.get(id=user_id)
    context = {"profile": profile}

    if profile.team_id:
        team = models.Team.objects.get(id=profile.team_id)
        context["team"] = team
    return render(request, "hackathon/profile.html", context=context)

@login_required(login_url="/login/")
def view_team(request, team_id):
    team = models.Team.objects.get(id=team_id)

    # Loading all members
    teammates = []
    for tid in models.TeamIdentification.objects.filter(team_id=team_id):
        profile = models.UserProfile.objects.get(id=tid.user_id)
        teammates.append(profile)

    return render(request, "hackathon/view_team.html", context={
        "team": team,
        "teammates": teammates,
        "leader": models.UserProfile.objects.get(id=team.leader),
    })

@login_required(login_url="/login/")
def team(request, team_id):
    team = models.Team.objects.get(id=team_id)

    if request.user.profile.team_id == team.id:
        team = models.Team.objects.get(id=team_id)

        # Getting current hackathon from subdomain
        hackathon_name = request.get_host().split(".")[0]

        # Get all models within hackathon
        hids = models.HackathonIdentification.objects.filter(hackathon_name=hackathon_name)
        hackathon_notifications = []
        for hid in hids:
            if hid.model_id.startswith("n"):
                notification = models.Notification.objects.get(id=hid.model_id)
                hackathon_notifications.append(notification)

        # Loading all notifications for the team
        notifications = {}
        for notification in hackathon_notifications:
            if notification.target_id == team_id:
                notifications[notification] = models.UserProfile.objects.get(id=notification.source_id)

        # Loading all members
        teammates = []
        for user in models.UserProfile.objects.all():
            if user.team_id == team_id:
                teammates.append(user)

        return render(request, "hackathon/team.html", context={
            "team": team,
            "leader": models.UserProfile.objects.get(id=team.leader),
            "teammates": teammates,
            "notifications": notifications,
            "submitted": models.TeamSubmission.objects.filter(hackathon_name=hackathon_name, team_id=team_id).exists(),
        })
    else:
        # Return error if user is not part of the team
        return HttpResponse("You are not on this team.")

@login_required(login_url="/login/")
def kickout(request):
    # Get user ID
    member_id = request.GET.get("member_id")

    # Get user profile_picture
    member = models.UserProfile.objects.get(id=member_id)

    # Send success message
    messages.success(request, member.user.username + " was kicked out.")

    # Instantiating titles and descriptions
    title = "You've been kicked out of your team."
    description = "We're sorry, but the team leader has kicked you out of the team. Please visit your notifications page for more details."

    # Send email to kicked out member
    EmailMessage(title, description, to=[member.user.email]).send()

    # Send notification to member
    notification = models.Notification(id="notification-" + str(random_with_N_digits(8)), title=title, description=description, source_id=member.team_id, target_id=member.id, type="info")
    notification.save()

    # Getting current hackathon from subdomain
    hackathon_name = request.get_host().split(".")[0]
    hackathon = models.Hackathon.objects.get(name=hackathon_name)

    # Creating hackathon identification
    hid = models.HackathonIdentification(hackathon_name=hackathon.name, model_id=notification.id)
    hid.save()

    # Delete team identification
    models.TeamIdentification.objects.get(team_id=request.user.profile.team_id, user_id=member.id).delete()

    # Kicking them out
    member.team_id = None
    member.save()

    return HttpResponseRedirect("/")

@login_required(login_url="/login/")
def join_team(request, team_id):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        # Source_id = user_id; target_id = team_id
        source_id = request.user.profile.id
        target_id = team_id

        notification = models.Notification(id="notification-" + str(random_with_N_digits(8)), title=title, description=description, source_id=source_id, target_id=target_id, type="action")
        notification.save()

        # Getting current hackathon from subdomain
        hackathon_name = request.get_host().split(".")[0]
        hackathon = models.Hackathon.objects.get(name=hackathon_name)

        # Creating hackathon identification
        hid = models.HackathonIdentification(hackathon_name=hackathon.name, model_id=notification.id)
        hid.save()

        # Sending email to each member of team
        for profile in models.UserProfile.objects.filter(team_id=team_id):
            email = profile.user.email
            EmailMessage("Join Team Request", profile.user.username + " has requested to join your team. Please visit your team pae to accept or reject it.", to=[email]).send()

        messages.success(request, "Join Team request successfully sent!")

        return HttpResponseRedirect("/")

    return render(request, "hackathon/join_team.html")

@login_required(login_url="/login/")
def leave_team(request, team_id):
    # Getting current user and setting team_id to null
    profile = models.UserProfile.objects.get(user=request.user)
    id = profile.id
    profile.team_id = None
    profile.save()

    # Delete team identification
    models.TeamIdentification.objects.get(team_id=team_id, user_id=id).delete()

    # Removing team if no one else is in it
    if not models.UserProfile.objects.filter(team_id=team_id):
        models.Team.objects.get(id=team_id).delete()
        models.HackathonIdentification.objects.get(model_id=team_id).delete()

    else:
        # Assign random member as leader
        random_id = models.TeamIdentification.objects.filter(team_id=team_id)[0]
        team = models.Team.objects.get(id=team_id)
        team.leader = random_id.user_id
        team.save()

    # Sending email to whole team
    for temp_profile in models.UserProfile.objects.filter(team_id=team_id):
        email = temp_profile.user.email
        EmailMessage(profile.user.username + " has the left the team", "Please view your team page for more information.", to=[email]).send()

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

        # Getting current hackathon from subdomain
        hackathon_name = request.get_host().split(".")[0]
        hackathon = models.Hackathon.objects.get(name=hackathon_name)

        # Creating hackathon identification
        hid = models.HackathonIdentification(hackathon_name=hackathon.name, model_id=notification.id)
        hid.save()

        # Sending email to user
        profile = models.UserProfile.objects.get(id=target_id)
        email = profile.user.email
        email_message = EmailMessage("Team invitation received", "You have been requested to join a team. Please view your notifications page to accept or reject it.", to=[email])
        email_message.send()

        messages.success(request, "Team invitation successfully sent!")

        return HttpResponseRedirect("/")

    return render(request, "hackathon/invite_to_team.html")

def hackathon_info(request):
    html_file = open(os.path.dirname(__file__) + "/info_files/" + request.get_host().split('.')[0] + "_info.txt", "r")
    html = html_file.read()

    return render(request, "hackathon/hackathon_info.html", context={"html": mark_safe(html)})

def submit(request):
    if request.method == "POST":
        # Getting submission information
        hackathon_name = request.get_host().split(".")[0]
        team_id = request.user.profile.team_id
        submission_name = request.POST.get("submission_name")
        submission_description = request.POST.get("submission_description")

        # Creating submission
        submission = models.TeamSubmission(hackathon_name=hackathon_name, team_id=team_id, submission_name=submission_name, submission_description=submission_description)
        submission.save()

        return HttpResponseRedirect("/")

    return render(request, "hackathon/submit.html")

def submissions(request):
    # Getting hackathon from subdomain
    hackathon_name = request.get_host().split(".")[0]

    # Loading and displaying all team submissions
    submissions = []
    counter = 1
    parameters = []
    for submission in models.TeamSubmission.objects.filter(hackathon_name=hackathon_name):
        parameters = []

        # Appending number
        parameters.append(counter)
        counter += 1

        # Appending team
        team = models.Team.objects.get(id=submission.team_id)
        parameters.append(team)

        # Appending submission
        parameters.append(submission)

    if parameters:
        submissions.append(parameters)

    return render(request, "hackathon/submissions.html", context={"submissions": submissions})

def awards(request):
    # Getting hackathon from subdomain
    hackathon_name = request.get_host().split(".")[0]

    # Loading and displaying all awards
    awards = {}
    for award in models.Award.objects.filter(hackathon_name=hackathon_name):
        if award.team_id:
            team = models.Team.objects.get(id=award.team_id)
            awards[award] = team
        else:
            awards[award] = None

    return render(request, "hackathon/awards.html", context={"awards": awards})

# STAFF VIEWS
@staff_member_required
@login_required(login_url="/login/")
def modify_hackathon_info(request):
    if request.method == "POST":
        new_info = request.POST.get("hackathon_info")

        html = markdown2.markdown(new_info)
        html_file = open(os.path.dirname(__file__) + "/info_files/" + request.get_host().split('.')[0] + "_info.txt", "w")
        html_file.write(html)

        return HttpResponseRedirect("/hackathon-info/")

    html_file = open(os.path.dirname(__file__) + "/info_files/" + request.get_host().split('.')[0] + "_info.txt", "r")
    markdown = html2markdown.convert(html_file.read())

    return render(request, "hackathon/modify_hackathon_info.html", context={"markdown": markdown})


@staff_member_required
@login_required(login_url="/login/")
def admin_view(request):
    # Getting current hackathon from subdomain
    hackathon_name = request.get_host().split(".")[0]

    if request.method == "POST":
        submit_type = request.POST.get("type")
        if submit_type == "update":
            id = request.POST.get("id")
            title = request.POST.get("title")
            description = request.POST.get("description")
            prize = request.POST.get("prize")

            # Updating model
            award = models.Award.objects.get(id=id)
            award.title = title
            award.description = description
            award.prize = prize
            award.save()

        elif submit_type == "add":
            title = request.POST.get("title")
            description = request.POST.get("description")
            prize = request.POST.get("prize")

            # Creating and storing award
            award = models.Award(hackathon_name=hackathon_name, title=title, description=description, prize=prize)
            award.save()

    # Get all models within hackathon
    hids = models.HackathonIdentification.objects.filter(hackathon_name=hackathon_name)
    hackathon_teams = []
    hackathon_competitors = []
    for hid in hids:
        # Getting all teams
        if hid.model_id.startswith("t"):
            team = models.Team.objects.get(id=hid.model_id)
            hackathon_teams.append(team)
        # Getting all competitors
        if not hid.model_id.startswith("t") and not hid.model_id.startswith("n"):
            competitor = models.UserProfile.objects.get(id=hid.model_id)
            if competitor != request.user.profile:
                if not competitor.user.is_staff:
                    if not competitor.user.is_superuser:
                        hackathon_competitors.append(competitor)

    # Loading and displaying all teams
    teams = {}

    for team in hackathon_teams:
        id = team.id
        teammates = []
        for user in models.UserProfile.objects.all():
            if user.team_id == id:
                teammates.append(user)

        teams[team] = teammates

    # Loading and displaying all team submissions
    submissions = []
    counter = 1
    parameters = []
    for submission in models.TeamSubmission.objects.filter(hackathon_name=hackathon_name):
        parameters = []

        # Appending number
        parameters.append(counter)
        counter += 1

        # Appending team
        for hid in models.HackathonIdentification.objects.filter(hackathon_name=hackathon_name):
            # Getting all teams
            if hid.model_id.startswith("t"):
                team = models.Team.objects.get(id=hid.model_id)
                parameters.append(team)
                break

        # Appending submission
        parameters.append(submission)

    if parameters:
        submissions.append(parameters)

    # Loading and displaying all awards
    awards = {}
    for award in models.Award.objects.filter(hackathon_name=hackathon_name):
        if award.team_id:
            team = models.Team.objects.get(id=award.team_id)
            awards[award] = team
        else:
            awards[award] = None

    return render(request, "hackathon/admin_view.html", context={
        "teams": teams,
        "competitors": hackathon_competitors,
        "submissions": submissions,
        "awards": awards,
    })

def select_team(request):
    # Getting current hackathon from subdomain
    hackathon_name = request.get_host().split(".")[0]

    # Getting award ID
    award_id = request.GET.get("award_id")

    # Get all models within hackathon
    hids = models.HackathonIdentification.objects.filter(hackathon_name=hackathon_name)
    hackathon_teams = []
    for hid in hids:
        if hid.model_id.startswith("t"):
            team = models.Team.objects.get(id=hid.model_id)
            hackathon_teams.append(team)

    # Loading and displaying all teams
    teams = {}

    for team in hackathon_teams:
        id = team.id
        teammates = []
        for user in models.UserProfile.objects.all():
            if user.team_id == id:
                teammates.append(user)

        teams[team] = teammates

    return render(request, "hackathon/select_team.html", context={"teams": teams, "award_id": award_id})


# POST REQUEST VIEWS
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
    models.HackathonIdentification.objects.get(model_id=notification_id).delete()

    # Creating notification for user
    notification = models.Notification(id="notification-" + str(random_with_N_digits(8)), title="Accepted into " + team.name, description="Congrats!", source_id=team_id, target_id=user_id, type="info")
    notification.save()

    # Getting current hackathon from subdomain
    hackathon_name = request.get_host().split(".")[0]
    hackathon = models.Hackathon.objects.get(name=hackathon_name)

    # Creating hackathon identification
    hid = models.HackathonIdentification(hackathon_name=hackathon.name, model_id=notification.id)
    hid.save()

    profile = models.UserProfile.objects.get(id=user_id)
    email = profile.user.email
    EmailMessage("Join Team Request Accepted!", "Your join team request has been accepted! Please view your team page for more information.", to=[email]).send()

    # Adding user to team
    profile = models.UserProfile.objects.get(id=user_id)
    profile.team_id = team_id
    profile.save()

    # Creating team identification
    tid = models.TeamIdentification(team_id=team_id, user_id=profile.id)
    tid.save()

    messages.success(request, "User successfully accepted into team!")

    return HttpResponseRedirect("/")

def reject_user(request):
    # Grabbing query parameters
    notification_id = request.GET.get("notification_id")
    user_id = request.GET.get("user_id")
    team_id = request.GET.get("team_id")

    team = models.Team.objects.get(id=team_id)

    # Deleting notification
    notification = models.Notification.objects.get(id=notification_id)
    notification.delete()
    models.HackathonIdentification.objects.get(model_id=notification_id).delete()

    # Creating notification for user
    notification = models.Notification(id="notification-" + str(random_with_N_digits(8)), title="Rejected from " + team.name, description="We're sorry", source_id=team_id, target_id=user_id, type="info")
    notification.save()

    # Getting current hackathon from subdomain
    hackathon_name = request.get_host().split(".")[0]
    hackathon = models.Hackathon.objects.get(name=hackathon_name)

    # Creating hackathon identification
    hid = models.HackathonIdentification(hackathon_name=hackathon.name, model_id=notification.id)
    hid.save()

    # Sending email to user
    profile = models.UserProfile.objects.get(id=user_id)
    email = profile.user.email
    EmailMessage("Join Team Request Rejected", "We're sorry, but your join team request has been rejected. Please view your team page for more information.", to=[email]).send()

    messages.success(request, "Team invitations successfully rejected.")

    return HttpResponseRedirect("/")

def accept_invite(request):
    # Grabbing query parameters
    notification_id = request.GET.get("notification_id")
    user_id = request.GET.get("user_id")
    team_id = request.GET.get("team_id")

    # Adding user to team
    profile = models.UserProfile.objects.get(id=user_id)
    profile.team_id = team_id
    profile.save()

    # Creating team identification
    tid = models.TeamIdentification(team_id=team_id, user_id=profile.id)
    tid.save()

    # Deleting notification
    notification = models.Notification.objects.get(id=notification_id)
    notification.delete()
    models.HackathonIdentification.objects.get(model_id=notification_id).delete()

    # Creating notification for team
    notification = models.Notification(id="notification-" + str(random_with_N_digits(8)), title=profile.user.username + " accepted invite!", description="Invitation accepted!", source_id=user_id, target_id=team_id, type="info")
    notification.save()

    # Getting current hackathon from subdomain
    hackathon_name = request.get_host().split(".")[0]
    hackathon = models.Hackathon.objects.get(name=hackathon_name)

    # Creating hackathon identification
    hid = models.HackathonIdentification(hackathon_name=hackathon.name, model_id=notification.id)
    hid.save()

    # Sending email to each member of team
    for profile in models.UserProfile.objects.filter(team_id=team_id):
        email = profile.user.email
        EmailMessage("Team invitiation Accepted!", "Your team invitation has been accepted! Please view your team page for more information.", to=[email]).send()

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
    models.HackathonIdentification.objects.get(model_id=notification_id).delete()

    profile = models.UserProfile.objects.get(id=user_id)

    # Creating notification for team
    notification = models.Notification(id="notification-" + str(random_with_N_digits(8)), title=profile.user.username + " rejected team invitation.", description="Invitation rejected.", source_id=user_id, target_id=team_id, type="info")
    notification.save()

    # Getting current hackathon from subdomain
    hackathon_name = request.get_host().split(".")[0]
    hackathon = models.Hackathon.objects.get(name=hackathon_name)

    # Creating hackathon identification
    hid = models.HackathonIdentification(hackathon_name=hackathon.name, model_id=notification.id)
    hid.save()

    # Sending email to each member of team
    for profile in models.UserProfile.objects.filter(team_id=team_id):
        email = profile.user.email
        EmailMessage("Team invitation rejected", "We're sorry, but your team invitiation has been rejected. Please view your team page for more information", to=[email]).send()

    messages.success(request, "Team invite successfully rejected.")

    return HttpResponseRedirect("/")

def delete_user(request):
    # Getting current hackathon from subdomain
    hackathon_name = request.get_host().split(".")[0]

    id = request.GET.get("id")

    profile = models.UserProfile.objects.get(id=id)
    profile.user.delete()
    models.HackathonIdentification.objects.get(hackathon_name=hackathon_name, model_id=id).delete()

    # Deleting team identification
    models.TeamIdentification.objects.get(user_id=profile.id).delete()

    EmailMessage("HackCollab Account Deleted", "You're HackCollab account has been deleted. Please contact the administrators for more information or re-register.", to=[profile.user.email]).send()

    username = profile.user.username

    profile.delete()

    messages.success(request, username + " successfully deleted.")

    return HttpResponseRedirect("/")

def delete_team(request):
    id = request.GET.get("id")

    team = models.Team.objects.get(id=id)
    name = team.name
    team.delete()
    models.HackathonIdentification.objects.get(model_id=id).delete()

    # Getting current hackathon from subdomain
    hackathon_name = request.get_host().split(".")[0]
    hackathon = models.Hackathon.objects.get(name=hackathon_name)

    # Removing team from all users
    for profile in models.UserProfile.objects.filter(team_id=id):
        # Delete team identification
        models.TeamIdentification.objects.get(team_id=id, user_id=profile.id).delete()

        profile.team_id = None
        profile.save()

        # Sending email notification
        EmailMessage("Team " + name + " deleted", "Team " + name + " was deleted by the hackathon organizers. Please visit your notifications page for more information", to=[profile.user.email])

        # Sending notification
        notification = models.Notification(id="notification-" + str(random_with_N_digits(8)), title="Team " + name + " deleted", description="Team " + name + " was deleted by the hackathon organizers.", source_id=None, target_id=profile.id, type="info")
        notification.save()

        # Creating hackathon identification
        hid = models.HackathonIdentification(hackathon_name=hackathon.name, model_id=notification.id)
        hid.save()

    messages.success(request, "Team " + name + " successfully deleted.")

    return HttpResponseRedirect("/")

def delete_notification(request):
    id = request.GET.get("id")

    models.Notification.objects.get(id=id).delete()
    models.HackathonIdentification.objects.get(model_id=id).delete()

    return JsonResponse({"value": "hi"})

def delete_submission(request):
    id = request.GET.get("id")

    models.TeamSubmission.objects.get(team_id=id).delete()

    return HttpResponseRedirect("/")

def delete_award(request):
    id = request.GET.get("id")

    models.Award.objects.get(id=id).delete()

    return HttpResponseRedirect("/admin-view/")

def assign_award(request):
    award_id = request.GET.get("award_id")
    team_id = request.GET.get("team_id")

    award = models.Award.objects.get(id=award_id)

    if team_id == "None":
        award.team_id = None
    else:
        award.team_id = team_id
    award.save()

    return HttpResponseRedirect("/admin-view/")
