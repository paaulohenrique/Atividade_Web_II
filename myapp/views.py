from django.shortcuts import render
from .models import Client, Order
from django.db.models import Sum

def clients(request):
    # Mostrar apenas clientes ativos
    clients = Client.objects.filter(is_deleted=False)

    # Mostrar apenas pedidos ativos
    orders = Order.objects.filter(is_deleted=False).select_related('client', 'product')

    # Total gasto por cliente ativo
    totals = Order.objects.filter(is_deleted=False).values('client__id', 'client__name').annotate(
        total_spent=Sum('total_price')
    )

    context = {
        'clients': clients,
        'orders': orders,
        'totals': totals
    }
    return render(request, 'myapp/clients.html', context)
