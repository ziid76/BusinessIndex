from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Indicator, DailyPerformance, CategoryGroup, Menu
from datetime import date
from django.http import JsonResponse
import json

@login_required
def index(request):
    # Get user's permitted menus
    if request.user.is_superuser:
        user_menus = Menu.objects.all().order_by('order')
    else:
        user_menus = request.user.permitted_menus.all().order_by('order')
    
    if user_menus.exists():
        first_menu = user_menus.first()
        return redirect('daily_performance', group_code=first_menu.code)
    
    # If no menus and is staff, maybe go to user management? 
    # But user specifically asked for auth.html
    return render(request, 'dashboard/auth.html')

@login_required
def user_management(request):
    if not request.user.is_staff:
        return redirect('index')
        
    from django.contrib.auth.models import User
    users = User.objects.all().prefetch_related('permitted_menus')
    all_menus = Menu.objects.all()
    
    return render(request, 'dashboard/user_list.html', {
        'users': users,
        'all_menus': all_menus
    })

@login_required
def update_user_permissions(request):
    if request.method == 'POST' and request.user.is_staff:
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            menu_ids = data.get('menu_ids', [])
            
            from django.contrib.auth.models import User
            target_user = User.objects.get(id=user_id)
            
            # Clear existing and set new permissions
            # ManyToMany relationship through Menu.authorized_users can be managed from either side.
            # Here we update from the Menu side or use the related name 'permitted_menus'
            target_user.permitted_menus.set(Menu.objects.filter(id__in=menu_ids))
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def daily_performance(request, group_code):
    target_date_str = request.GET.get('date', date.today().isoformat())
    try:
        target_date = date.fromisoformat(target_date_str)
    except ValueError:
        target_date = date.today()

    # 파라미터로 받은 그룹 코드와 일치하는 CategoryGroup 리스트(QuerySet) 생성
    groups = CategoryGroup.objects.filter(code=group_code)
    print(groups)
    # 해당 CategoryGroup에 포함된 Category를 거쳐 Indicator 필터링
    indicators = Indicator.objects.filter(
        is_active=True, 
        category__group__in=groups
    ).select_related('category', 'category__group').order_by('category__group__order', 'category__order', 'order')
    
    print(indicators)
    # Get existing performances for the date
    performances = DailyPerformance.objects.filter(date=target_date)
    performance_map = {p.indicator_id: p.value for p in performances}
    
    grouped_data = []
    current_group = None
    current_cat = None
    
    for ind in indicators:
        g_name = ind.category.group.name
        g_code = ind.category.group.code
        c_name = ind.category.name

        # 새로운 그룹(대분류) 시작 여부
        is_new_group = not current_group or current_group['name'] != g_name
        if is_new_group:
            current_group = {
                'code': g_code,
                'name': g_name,
                'categories': [],
                'rowspan': 0
            }
            print(current_group)
            grouped_data.append(current_group)
            current_cat = None
            
        # 새로운 카테고리(소분류) 시작 여부
        is_new_cat = not current_cat or current_cat['name'] != c_name
        if is_new_cat:
            current_cat = {
                'name': c_name,
                'items': [],
                'rowspan': 0
            }
            current_group['categories'].append(current_cat)
            
        # 개별 항목 추가
        item = {
            'id': ind.id,
            'name': ind.name,
            'unit': ind.unit,
            'value': performance_map.get(ind.id, 0),
            'is_first_in_group': is_new_group and (not current_cat['items']),
            'is_first_in_cat': is_new_cat
        }
        current_cat['items'].append(item)
        current_cat['rowspan'] += 1
        current_group['rowspan'] += 1
        
    return render(request, 'dashboard/daily_performance.html', {
        'target_date': target_date.isoformat(),
        'grouped_data': grouped_data,
        'current_group_code': group_code
    })

@login_required
def save_performance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            target_date = data.get('date')
            values = data.get('values', {}) # {indicator_id: value}
            
            for ind_id, val in values.items():
                DailyPerformance.objects.update_or_create(
                    indicator_id=ind_id,
                    date=target_date,
                    defaults={'value': val}
                )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
