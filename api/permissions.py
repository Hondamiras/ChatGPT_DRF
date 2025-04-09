from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешаем всем читать (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            # Если это безопасный метод (т.е. GET, HEAD, OPTIONS), то разрешаем доступ
            # (т.е. разрешаем всем читать)
            return True

        # А менять можно только если ты владелец
        return obj.owner == request.user
        #владелец объекта == текущий пользователь

        # (аналогия):
        #🔓 Чтение — как читать чей-то пост в Инстаграме
        #🔒 Изменение — можно только если ты автор поста

# ✍️ Представим:
# Ты — пользователь Ali.

# Категорию "Электроника" создал Ali, а "Игрушки" создал Bob.

# Теперь:

# Действие	Разрешено Али?	Разрешено Бобу?
# Смотреть "Электроника"	✅ Да	✅ Да
# Удалить "Электроника"	✅ Да	❌ Нет
# Обновить "Игрушки"	❌ Нет	✅ Да
