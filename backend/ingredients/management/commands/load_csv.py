import csv
import os

from django.conf import settings
from django.core.management import BaseCommand
from django.db import IntegrityError
from ingredients.models import Ingredient, Unit
from tags.models import Tag

DATA_FORMAT = {
    'measurement_unit': 'measurement_unit_id',
    'ingredient_name': 'name',
    'name': 'name',
    'slug': 'slug'
}


class Command(BaseCommand):
    """Класс для обработки команд."""

    def handle(self, *args, **options):
        """
        Загружает данные в БД из `csv` файла.

        Для запуска команды выполнить:
        'python manage.py load_csv'.
        """

        try:
            with open(
                os.path.join(settings.CSV_DIR, 'ingredients.csv'),
                encoding='utf8'
            ) as datafile:
                data = csv.DictReader(datafile)
                list_ingredients = []
                for cursor in data:
                    args = dict(**cursor)
                    unit, flag = Unit.objects.get_or_create(
                        name=args['measurement_unit']
                    )
                    args['measurement_unit'] = unit
                    list_ingredients.append(Ingredient(**args))
                Ingredient.objects.bulk_create(
                    list_ingredients, ignore_conflicts=True)
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR('Файл ingredients.csv не найден.')
            )
        except (ValueError, IntegrityError) as error:
            self.stdout.write(
                self.style.ERROR(
                    f'Ошибка данных в файле ingredients.csv . {error}.'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Все данные успешно загружены.')
            )

        try:
            with open(
                os.path.join(settings.CSV_DIR, 'tags.csv'),
                encoding='utf8'
            ) as datafile:
                data = csv.DictReader(datafile)
                list_tags = []
                for cursor in data:
                    args = dict(**cursor)
                    list_tags.append(Tag(**args))
                Tag.objects.bulk_create(
                    list_tags, ignore_conflicts=True)
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR('Файл tags.csv не найден.')
            )
        except (ValueError, IntegrityError) as error:
            self.stdout.write(
                self.style.ERROR(f'Ошибка данных в файле tags.csv . {error}.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Все данные успешно загружены.')
            )
