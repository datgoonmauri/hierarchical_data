from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from file.models import FileSystem


admin.site.register(FileSystem, DraggableMPTTAdmin)
