from django.shortcuts import render
from django.db.models import Sum, Q
from .models import Заказы_покупателей, Контрагенты


def orders_view(request):
    filter_client = request.GET.get('filter_client', '')
    sort_field = request.GET.get('sort_field', 'Заказчик')
    sort_dir = request.GET.get('sort_dir', 'asc')
    search = request.GET.get('search', '').strip()

    if 'show_all' in request.GET:
        filter_client = ''
        search = ''

    orders_qs = Заказы_покупателей.objects.select_related('Заказчик_УИД').annotate(
        total_price=Sum('товары_в_заказах__Сумма')
    )

    if filter_client:
        orders_qs = orders_qs.filter(Заказчик_УИД=filter_client)

    if search:
        orders_qs = orders_qs.filter(
            Q(Заказчик_УИД__Наименование__icontains=search) |
            Q(Заказчик_УИД__Адрес__icontains=search) |
            Q(Заказчик_УИД__Телефон__icontains=search)
        )

    sort_dict = {
        'Заказчик': 'Заказчик_УИД__Наименование',
        'Дата заказа': 'Дата',
        'Сумма заказа': 'total_price',
    }
    field_to_sort = sort_dict.get(sort_field, 'Заказчик_УИД__Наименование')
    if sort_dir == 'desc':
        field_to_sort = '-' + field_to_sort
    orders_qs = orders_qs.order_by(field_to_sort)

    rows = []
    total_sum = 0

    for o in orders_qs:
        price = o.total_price or 0
        total_sum += price

        rows.append({
            'заказчик': o.Заказчик_УИД.Наименование if o.Заказчик_УИД else '',
            'город': o.Заказчик_УИД.Адрес if o.Заказчик_УИД else '',
            'телефон': o.Заказчик_УИД.Телефон if o.Заказчик_УИД else '',
            'дата': o.Дата.strftime('%d.%m.%Y') if o.Дата else '',
            'сумма': price
        })

    context = {
        'rows': rows,
        'clients': Контрагенты.objects.filter(Тип='Заказчик').order_by('Наименование'),
        'filter_client': filter_client,
        'sort_field': sort_field,
        'sort_dir': sort_dir,
        'search': search,
        'total_count': len(rows),
        'total_sum': f'{total_sum:.2f}'.replace('.', ','),
        'search_no_result': bool(search and not rows),
        'sort_fields': ['Заказчик', 'Дата заказа', 'Сумма заказа'],
    }
    return render(request, 'orders.html', context)
