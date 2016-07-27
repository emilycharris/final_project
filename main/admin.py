from django.contrib import admin
from main.models import Rating, Profile, Program, Queue, QueueProgram, GroupQueue

# Register your models here.

admin.site.register(Rating)
admin.site.register(Profile)
admin.site.register(Program)

class QueueProgramInline(admin.StackedInline):
    model = QueueProgram

admin.site.register(QueueProgram)


class QueueAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    inlines = (QueueProgramInline,)

    def get_inline_instances(self, request, obj=None):
        return [inline(self.model, self.admin_site) for inline in self.inlines]

admin.site.register(Queue, QueueAdmin)

class GroupQueueAdmin(admin.ModelAdmin):
        list_display = ['id']


admin.site.register(GroupQueue, GroupQueueAdmin)
