from django.contrib.auth.decorators import user_passes_test


def role_required(*role_names):
    def check_role(user):
        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        return user.groups.filter(name__in=role_names).exists()

    return user_passes_test(check_role, login_url="login")
