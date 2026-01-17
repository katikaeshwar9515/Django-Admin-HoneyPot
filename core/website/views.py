from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView,FormView,CreateView,TemplateView
from .forms import PhotoForm
from .models import Photo
from honeypot.models import LoginAttempt, BlackList, HoneyPotHit
# Create your views here.


class LandingView(TemplateView):
    template_name = "website/landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["features"] = [
            {
                "title": "Decoy Admin",
                "desc": "Fake /admin/ absorbs brute-force attempts and records behavior.",
                "icon": "shield-lock",
            },
            {
                "title": "Hidden Entry",
                "desc": "Real admin lives at /secret-admin-entrance/ for authorized staff only.",
                "icon": "key",
            },
            {
                "title": "Lockouts & Logging",
                "desc": "Repeated failures trigger lockouts and provide intel for defense.",
                "icon": "activity",
            },
        ]
        context["steps"] = [
            "Visit the landing page and understand the honeypot flow.",
            "Probe /admin/ and see lockouts in action.",
            "Use /secret-admin-entrance/ for the real admin login.",
        ]
        context["stats"] = {
            "honeypot_hits": HoneyPotHit.objects.count(),
            "login_attempts": LoginAttempt.objects.count(),
            "blocked_ips": BlackList.objects.count(),
        }
        return context


class UploadView(CreateView):
    template_name = 'website/index.html'
    form_class = PhotoForm
    success_url = reverse_lazy("website:upload")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["gallery"] = Photo.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        
        if 'file' not in request.FILES or not form.is_valid():
            return HttpResponseRedirect(reverse_lazy("website:index"))
        
        if form.is_valid():
            for file in files:
                Photo.objects.create(file=file)
            return HttpResponseRedirect(self.request.path_info)
        else:
            return self.form_invalid(form)
    

class AboutView(TemplateView):
    template_name = "website/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team_members"] = [
            {
                "name": "Eshwar Katika",
                "role": "Team Leader",
                "details": "22E11A6228",
            },
            {
                "name": "K Indu",
                "role": "",
                "details": "22E11A6230",
            },
            {
                "name": "Sahasra Ch",
                "role": "",
                "details": "22E11A6211",
            },
            {
                "name": "Santosh K",
                "role": "",
                "details": "22E11A6229",
            },
        ]
        return context
    
