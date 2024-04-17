from django.http import JsonResponse


def home(request):
    return JsonResponse({'page': 'blog'})
