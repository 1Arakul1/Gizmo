# games/views.py
from django.core.cache import cache  # noqa: F401
from django.shortcuts import (
    get_object_or_404,
    render,
)

from components.models import CPU, GPU
from fps_data.models import FPSData
from .models import Game


def game_list(request):
    games = Game.objects.all()
    return render(request, 'games/game_list.html', {'games': games})


def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'games/game_detail.html', {'game': game})


def predict_fps(request):
    if request.method == 'POST':
        cpu_id = request.POST.get('cpu')
        gpu_id = request.POST.get('gpu')
        game_id = request.POST.get('game')
        settings = request.POST.get('settings')

        # Проверка, что значения не пустые
        if not all([cpu_id, gpu_id, game_id, settings]):
            cpus = CPU.objects.all()
            gpus = GPU.objects.all()
            games = Game.objects.all()
            context = {
                'cpus': cpus,
                'gpus': gpus,
                'games': games,
                'error_message': "Пожалуйста, заполните все поля.",
            }
            return render(request, 'games/fps_form.html', context)

        try:
            cpu = get_object_or_404(CPU, pk=cpu_id)
            gpu = get_object_or_404(GPU, pk=gpu_id)
            game = get_object_or_404(Game, pk=game_id)

            # Ищем FPS в базе данных для данной комбинации компонентов
            fps_data = FPSData.objects.get(
                game=game, cpu=cpu, gpu=gpu, settings=settings
            )
            predicted_fps = f"{fps_data.min_fps} - {fps_data.max_fps} FPS"

        except FPSData.DoesNotExist:
            predicted_fps = "Нет данных для этой конфигурации."  # Вывод FPS
            context = {
                'error_message': "Нет данных для этой конфигурации.",
                'cpus': CPU.objects.all(),
                'gpus': GPU.objects.all(),
                'games': Game.objects.all(),
            }  # Отправляем сообщение об ошибке

        except ValueError as e:
            context = {
                'error_message': "Некорректные данные: {}. ".format(e),
                'cpus': CPU.objects.all(),
                'gpus': GPU.objects.all(),
                'games': Game.objects.all(),
            }
            return render(request, 'games/fps_form.html', context)

        context = {
            'game': game,
            'cpu': cpu,
            'gpu': gpu,
            'predicted_fps': predicted_fps,
            'settings': settings,
        }
        return render(request, 'games/fps_result.html', context)

    else:  # Отобразить форму выбора компонентов
        cpu_id = request.GET.get('cpu')
        gpu_id = request.GET.get('gpu')

        if cpu_id and gpu_id:
            # Если CPU и GPU заданы - передать их в контекст
            cpu = get_object_or_404(CPU, pk=cpu_id)
            gpu = get_object_or_404(GPU, pk=gpu_id)
            gpus = GPU.objects.all()
            games = Game.objects.all()
            context = {'cpu': cpu, 'gpu': gpu, 'gpus': gpus, 'games': games}  # Передаём в шаблон
            return render(request, 'games/fps_form.html', context)

        cpus = CPU.objects.all()
        gpus = GPU.objects.all()
        games = Game.objects.all()
        context = {'cpus': cpus, 'gpus': gpus, 'games': games}
        return render(request, 'games/fps_form.html', context)
