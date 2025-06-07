from django.contrib import admin


@admin.register('Message')
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user_id','username','email ', 'password', 'phone_number', 's_online', 'last_seen']
    
admin.register('Conversation')
admin.register('User')