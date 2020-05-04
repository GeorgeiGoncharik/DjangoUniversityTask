from django.shortcuts import render
from .models import ServiceType, Service

# Create your views here.
def services_list(request):
    service_list = []
    service_types_list = ServiceType.objects.all()

    for s_type in service_types_list:
        services = Service.objects.filter(service_type=s_type)
        service_list.append(services)

    dictionary = dict(zip(service_types_list, service_list))
    return render(
        request,
        'services/services_list.html',
        {'service_types_list': dictionary}
    )
