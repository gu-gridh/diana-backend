
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import viewsets
from .forms import ContactForm  # Import ContactForm
from rest_framework.response import Response
from rest_framework import status

class ContactFormViewSet(viewsets.ViewSet):
    def create(self, request):
        form = ContactForm(request.data)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            send_mail(
                f'From {name}, Subject: {subject}',
                f'Message: {message}\n',
                email,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
        return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
