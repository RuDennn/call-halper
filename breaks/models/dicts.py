from core.models.mixins import BaseDictModelMixin


class ReplacementStatus(BaseDictModelMixin):
    class Meta:
        verbose_name = 'Статус смены'
        verbose_name_plural = 'Статусы смен'


class BreakStatus(BaseDictModelMixin):
    class Meta:
        verbose_name = 'Статус обеда'
        verbose_name_plural = 'Статусы обедов'

