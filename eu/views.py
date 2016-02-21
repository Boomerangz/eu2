from django.shortcuts import redirect

__author__ = 'igor'



def home(request):
    if request.user.is_anonymous():
        return redirect("/login/")
    else:
        return redirect("/advertiser/campaigns/")
