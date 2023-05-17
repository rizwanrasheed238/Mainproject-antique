
# Create your views here.

from django.shortcuts import render, redirect
 
 
def chatPage(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chatPage.html", context)

