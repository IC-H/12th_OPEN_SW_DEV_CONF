from django.http import JsonResponse

def search(request):
    params = request.POST.get('keyWrods');
    data = {
        'keyWrods' : params
    }
    return JsonResponse(data)
