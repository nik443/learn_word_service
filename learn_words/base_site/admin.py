from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import (MasterDictionaries,
                    UserDictionaries,
                    DatesLastAddedWordInUserDict)


MyUser = get_user_model()

admin.site.register(MyUser)
admin.site.register(MasterDictionaries)
admin.site.register(UserDictionaries)
admin.site.register(DatesLastAddedWordInUserDict)