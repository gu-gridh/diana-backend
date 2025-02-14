from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
import json

@csrf_exempt
def contact(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')

            if not all([name, email, subject, message]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            send_mail(
                f'From {name}, Subject: {subject}',
                f'Message: {message}\n',
                email,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            return JsonResponse({'message': 'Email sent successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
