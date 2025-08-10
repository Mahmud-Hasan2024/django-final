from django.shortcuts import redirect

# Create your views here.

def api_root_view(request):
    return redirect('api-root')