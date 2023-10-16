from django.contrib.auth.decorators import user_passes_test


def admin_only(function):
    """
    Декоратор, который разрешает доступ только для администраторов
    """
    return user_passes_test(lambda u: u.is_superuser)(function)
