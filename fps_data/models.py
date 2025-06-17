# fps_data\models.py
from django.db import models
class FPSData(models.Model):
    """
    Таблица соответствия FPS для компонентов и игр.
    Связывает конкретные компоненты (CPU и GPU) с FPS в определенной игре
    на разных настройках графики.
    """
    game = models.ForeignKey("games.Game", on_delete=models.CASCADE, verbose_name="Игра")
    cpu = models.ForeignKey("components.CPU", on_delete=models.CASCADE, verbose_name="Процессор")
    gpu = models.ForeignKey("components.GPU", on_delete=models.CASCADE, verbose_name="Видеокарта")
    min_fps = models.IntegerField(verbose_name="FPS (минимальные)")
    avg_fps = models.IntegerField(verbose_name="FPS (средние)")
    max_fps = models.IntegerField(verbose_name="FPS (максимальные)")
    settings = models.CharField(
        max_length=50,
        choices=[
            ('low', 'Низкие'),
            ('medium', 'Средние'),
            ('high', 'Высокие'),
            ('ultra', 'Ультра'),
        ],
        default='medium',
        verbose_name="Настройки графики"
    )

    def __str__(self):
        return f"{self.game} - {self.cpu} + {self.gpu} ({self.settings})"

    class Meta:
        verbose_name = "Данные FPS"
        verbose_name_plural = "Данные FPS"
