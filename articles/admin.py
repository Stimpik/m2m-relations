from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        acc = 0
        for form in self.forms:
            main = form.cleaned_data
            if main.get('is_main'):
                acc += 1
        if acc == 0:
            raise ValidationError('Выберите основную тематику!')
        elif acc > 1:
            raise ValidationError('Основная тематика должна быть одна!')

        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 2


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
