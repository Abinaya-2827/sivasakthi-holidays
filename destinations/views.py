from django.shortcuts import render, get_object_or_404
from .models import Destination

def destination_list(request):
    query = request.GET.get("q", "").strip()

    destinations = Destination.objects.all()

    if query:
        destinations = destinations.filter(name__icontains=query)

    return render(request, "destination_list.html", {
        "destinations": destinations,
        "query": query,
    })


def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug)

    return render(request, "destination_detail.html", {
        "destination": destination,
    })