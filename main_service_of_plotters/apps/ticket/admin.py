from django.contrib import admin

from .models import Ticket, PopularProblem

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(PopularProblem)
class PopularProblemAdmin(admin.ModelAdmin):
    pass
