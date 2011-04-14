from django.contrib import admin

from datetime import datetime

from models import BroadcastFormat, MusicFocus, ShowInformation, ShowTopic, Host, Note, ProgramSlot, Show, TimeSlot

class BroadcastFormatAdmin(admin.ModelAdmin):
    list_display = ('format',)
    prepopulated_fields = {'slug': ('format',)}

class MusicFocusAdmin(admin.ModelAdmin):
    list_display = ('focus', 'abbrev')
    prepopulated_fields = {'slug': ('focus',)}

class ShowInformationAdmin(admin.ModelAdmin):
    list_display = ('information', 'abbrev')
    prepopulated_fields = {'slug': ('information',)}

class ShowTopicAdmin(admin.ModelAdmin):
    list_display = ('topic', 'abbrev')
    prepopulated_fields = {'slug': ('topic',)}

class NoteAdmin(admin.ModelAdmin):
    date_hierarchy = 'start'
    list_display = ('title', 'show', 'start', 'status')
    list_filter = ('status',)
    ordering = ('timeslot',)

    def queryset(self, request):
        qs = super(NoteAdmin, self).queryset(request)

        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(owner=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'timeslot':
            if request.user.is_superuser:
                kwargs['queryset'] = TimeSlot.objects.filter(start__gt=datetime.now)
            else:
                shows = request.user.shows.all()
                kwargs['queryset'] = TimeSlot.objects.filter(show__in=shows, start__gt=datetime.now)

        return super(NoteAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

class TimeSlotInline(admin.TabularInline):
    model = TimeSlot

class ProgramSlotAdmin(admin.ModelAdmin):
    date_hierarchy = 'dstart'
    inlines = (TimeSlotInline,)
    list_display = ('show', 'byweekday', 'rrule', 'tstart', 'tend', 'dstart', 'until', 'timeslot_count')
    list_filter = ('byweekday', 'rrule', 'is_repetition')
    ordering = ('byweekday', 'dstart')
    search_fields = ('show__name',)

class ProgramSlotInline(admin.TabularInline):
    model = ProgramSlot

class ShowAdmin(admin.ModelAdmin):
    filter_horizontal = ('hosts', 'owners', 'musicfocus', 'showinformation', 'showtopic')
    inlines = (ProgramSlotInline,)
    list_display = ('name', 'short_description', 'broadcastformat', 'has_active_programslots')
    list_filter = ('broadcastformat', 'showinformation', 'showtopic', 'musicfocus',)
    ordering = ('slug',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'short_description', 'description')

admin.site.register(BroadcastFormat, BroadcastFormatAdmin)
admin.site.register(MusicFocus, MusicFocusAdmin)
admin.site.register(ShowInformation, ShowInformationAdmin)
admin.site.register(ShowTopic, ShowTopicAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(ProgramSlot, ProgramSlotAdmin)
admin.site.register(Show, ShowAdmin)

admin.site.register(Host)