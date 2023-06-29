
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from av_system.models import Voo
from django.db.models import Case, Count, FloatField, Sum, When
User = get_user_model()


class Command(BaseCommand):
    help = 'Pre-creates a single Funcionario in the database.'
    def handle(self, *args, **options):
        voo_queryset = Voo.objects.filter(id_socio=1)
        print(voo_queryset[0].parecer)
        average_parecer = voo_queryset.aggregate(
            total_parecer=Sum(
                Case(
                    When(parecer__in="A", then=4),
                    When(parecer__in="B", then=3),
                    When(parecer__in="C", then=2),
                    When(parecer__in="D", then=1),
                    default=0,
                    output_field=FloatField()
                )
            ),
            count_parecer=Count(
                Case(
                    When(parecer__in=Voo.NOTA_CONCEITO_mapping.keys(), then=1),
                    default=0
                )
            )
        )

        count = average_parecer['count_parecer']
        total = average_parecer['total_parecer']
        average = total / count if count > 0 else 0

        print(average)

# Usage