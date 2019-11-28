from django.shortcuts import render

def index(request):
    return render(request, "hackcollab_app/index.html")

def handler404(request, *args, **argv):
    return render(request, "errors/404.html")

def handler500(request, *args, **argv):
    return render(request, "errors/500.html")

def privacy_policy(request):
    return render(request, "hackcollab_app/privacy_policy.html")

def terms_and_conditions(request):
    return render(request, "hackcollab_app/terms_and_conditions.html")
