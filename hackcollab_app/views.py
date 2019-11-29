from django.shortcuts import render
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect

def handler404(request, *args, **argv):
    return render(request, "errors/404.html")

def handler500(request, *args, **argv):
    return render(request, "errors/500.html")

def index(request):
    if request.method == "POST":
        # Grabbing information from contact us form
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Sending the email
        EmailMessage("HackCollab - General Contact Us", "From: " + name + "\n\n" + message + "\n\nEmail: " + email, to=["calix.huang1@gmail.com"]).send()

        # Redirecting to success page
        return HttpResponseRedirect("/success/")

    return render(request, "hackcollab_app/index.html")

def success(request):
    return render(request, "hackcollab_app/success.html" )

def privacy_policy(request):
    return render(request, "hackcollab_app/privacy_policy.html")

def terms_and_conditions(request):
    return render(request, "hackcollab_app/terms_and_conditions.html")
