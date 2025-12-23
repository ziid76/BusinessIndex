from .models import Menu

def menu_context(request):
    if request.user.is_authenticated:
        # 사용자가 권한을 가진 메뉴 목록을 가져옵니다.
        # 관리자(is_superuser)는 모든 메뉴를 볼 수 있도록 처리하거나, 
        # 특정 권한이 있는 메뉴만 보고 싶다면 filter만 사용합니다.
        if request.user.is_superuser:
            user_menus = Menu.objects.all()
        else:
            user_menus = request.user.permitted_menus.all()
        return {'user_menus': user_menus}
    return {'user_menus': []}
