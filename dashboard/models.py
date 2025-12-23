from django.db import models
from django.contrib.auth.models import User

class Menu(models.Model):

    code = models.CharField(max_length=2, unique=True, verbose_name="메뉴코드", default="00")
    name = models.CharField(max_length=100, verbose_name="메뉴 명")
    authorized_users = models.ManyToManyField(User, related_name='permitted_menus', blank=True, verbose_name="권한 부여 사용자")
    order = models.IntegerField(default=0, verbose_name="정렬 순서")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "메뉴 마스터"

    def __str__(self):
        return f"{self.name} ({self.code})"

class CategoryGroup(models.Model):
    code = models.CharField(max_length=2, verbose_name="사업영역 코드 (2자리)", default="00")
    name = models.CharField(max_length=100, verbose_name="구분 (대분류)")
    order = models.IntegerField(default=0, verbose_name="정렬 순서")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "구분 마스터"

    def __str__(self):
        return f"[{self.code}] {self.name}"



class Category(models.Model):
    group = models.ForeignKey(CategoryGroup, on_delete=models.CASCADE, related_name='categories', verbose_name="구분")
    name = models.CharField(max_length=100, verbose_name="분류 (소분류)")
    order = models.IntegerField(default=0, verbose_name="정렬 순서")

    class Meta:
        ordering = ['group', 'order', 'name']
        verbose_name = "분류 마스터"

    def __str__(self):
        return f"[{self.group.name}] {self.name}"

class Indicator(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='indicators', verbose_name="분류")
    name = models.CharField(max_length=100, verbose_name="항목")
    unit = models.CharField(max_length=50, verbose_name="단위")
    code = models.CharField(max_length=4, unique=True, verbose_name="지표코드", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="사용 여부")
    order = models.IntegerField(default=0, verbose_name="정렬 순서")

    class Meta:
        ordering = ['category', 'order', 'name']
        verbose_name = "지표 항목 마스터"

    def __str__(self):
        return f"[{self.category.name}] {self.name}"

class DailyPerformance(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name='performances', verbose_name="지표 항목")
    date = models.DateField(verbose_name="실적 일자")
    value = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="일실적")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('indicator', 'date')
        ordering = ['-date', 'indicator']
        verbose_name = "일일 지표 실적"

    def __str__(self):
        return f"{self.date} - {self.indicator.name}: {self.value}"
