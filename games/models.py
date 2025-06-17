# games\models.py
from django.db import models
class Game(models.Model):
    """Игра."""
    title = models.CharField(max_length=255, verbose_name="Название")
    genre = models.CharField(max_length=255, verbose_name="Жанр")
    min_cpu = models.ForeignKey("components.CPU", on_delete=models.SET_NULL, null=True, blank=True, related_name='min_games', verbose_name="Мин. CPU")
    min_gpu = models.ForeignKey("components.GPU", on_delete=models.SET_NULL, null=True, blank=True, related_name='min_games', verbose_name="Мин. GPU")
    min_ram = models.IntegerField(verbose_name="Мин. RAM (ГБ)", default=4) # Пример, лучше связать с моделью RAM
    recommended_cpu = models.ForeignKey("components.CPU", on_delete=models.SET_NULL, null=True, blank=True, related_name='recommended_games', verbose_name="Реком. CPU")
    recommended_gpu = models.ForeignKey("components.GPU", on_delete=models.SET_NULL, null=True, blank=True, related_name='recommended_games', verbose_name="Реком. GPU")
    recommended_ram = models.IntegerField(verbose_name="Реком. RAM (ГБ)", default=8) # Пример, лучше связать с моделью RAM

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"