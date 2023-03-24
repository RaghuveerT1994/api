from django.db import models

from django.contrib.auth.models import Group, User

Group.add_to_class('description', models.CharField(max_length=180,null=True, blank=True))
Group.add_to_class('extras', models.JSONField(default=dict, blank=True, null=True))
Group.add_to_class('is_deleted', models.BooleanField(default=False, null=True, blank=True))
Group.add_to_class('isActive', models.BooleanField(default=False, null=True, blank=True))


User.add_to_class('extras', models.JSONField(default=dict, blank=True, null=True))
User.add_to_class('is_deleted', models.BooleanField(default=False, null=True, blank=True))