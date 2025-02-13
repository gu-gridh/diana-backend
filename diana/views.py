from django.shortcuts import render, redirect
from diana.forms import ContactForm
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Send an email
            send_mail(
                f'From {name}, Subject: {subject}',
                f'Message: {message}\n',
                email,  # From email
                [settings.EMAIL_HOST_USER],  # To email
                fail_silently=False,
            )
            return redirect('success')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def success(request):
  return HttpResponse('Success!') 