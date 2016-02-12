from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.shortcuts import render



class IndexView(TemplateView):
    template_name = 'index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)

def about(request):
     return render(request, "about.html", {})

def contact(request):
    title = 'Contact Us!'
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form_email = form.cleaned_data.get('email')
        form_message = form.cleaned_data.get('message')
        form_full_name = form.cleaned_data.get('full_name')
        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, 'yourotheremail@email.com']
        contact_message = """
        %s: %s via %s
        """%(full_name, message, email)
        send_mail(subject, contact_message, from_email, to_email, fail_silently=False)

    context = {
        "form": form,
        "title": title,
    }
    return render(request, "forms.html", context)
    
