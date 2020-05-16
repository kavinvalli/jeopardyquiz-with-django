from django.contrib import admin
from.models import Level, Category, Question, Team

class LevelAdmin(admin.ModelAdmin):
    list_display = ('level_name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name','level')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text','level','category','marks_alloted','status')


class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name','team_points')

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('tournament_name',)


admin.site.register(Level, LevelAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Team, TeamAdmin)

