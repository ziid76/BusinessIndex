from django.contrib import admin
from .models import CategoryGroup, Category, Indicator, DailyPerformance, Menu

@admin.register(CategoryGroup)
class CategoryGroupAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'order')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'order')
    list_filter = ('group',)

@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'unit', 'code', 'is_active', 'order')
    list_filter = ('category', 'is_active')

@admin.register(DailyPerformance)
class DailyPerformanceAdmin(admin.ModelAdmin):
    list_display = ('date', 'indicator', 'value')
    list_filter = ('date', 'indicator__category')

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'order')
    filter_horizontal = ('authorized_users',)
