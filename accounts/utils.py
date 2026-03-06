from django.contrib.auth.models import Group


def assign_user_to_group(user, group_name):
    group, created = Group.objects.get_or_create(name=group_name)
    user.groups.clear()
    user.groups.add(group)
