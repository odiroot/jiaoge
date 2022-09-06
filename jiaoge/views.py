from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required(login_url="/code-claim")
def landing(request):
    return render(request, "landing.html")
