from django.shortcuts import render

# Create your views here.
def infer(request):
    return render(request, 'infer.html')