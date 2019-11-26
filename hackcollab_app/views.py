from django.shortcuts import render

def index(request):
    return render(request, "hackcollab_app/index.html")
