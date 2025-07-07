# components/signals.py
# components/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

from builds.models import OrderItem
from .models import (
    CPU,
    GPU,
    Motherboard,
    RAM,
    Storage,
    PSU,
    Case,
    Cooler,
    Stock,
)  # noqa: F401


@receiver(post_save, sender=OrderItem)
def update_stock_on_order_item_create(sender, instance, created, **kwargs):
    """
    Обновляет складской запас при создании нового элемента заказа.
    """
    if created:
        component_type = instance.component_type
        component_id = instance.component_id

        if component_type and component_id:
            try:
                stock_item = Stock.objects.get(
                    component_type=component_type, component_id=component_id
                )
                # Убедимся, что количество не уходит в минус
                stock_item.quantity = max(0, stock_item.quantity - instance.quantity)
                stock_item.save()
            except Stock.DoesNotExist:
                # Обрабатываем случай, когда Stock не существует.
                # Это может быть уместно, если компоненты создаются без записи Stock.
                pass


@receiver(post_save, sender=CPU)
@receiver(post_save, sender=GPU)
@receiver(post_save, sender=Motherboard)
@receiver(post_save, sender=RAM)
@receiver(post_save, sender=Storage)
@receiver(post_save, sender=PSU)
@receiver(post_save, sender=Case)
@receiver(post_save, sender=Cooler)
def create_stock_on_component_create(sender, instance, created, **kwargs):
    """Создает запись в Stock при создании нового компонента."""
    if created:
        component_type = sender._meta.model_name  # Получаем тип компонента из модели
        # Инициализируем количество на складе каким-то значением по умолчанию (например, 10)
        Stock.objects.create(
            component_type=component_type, component_id=instance.pk, quantity=10
        )
