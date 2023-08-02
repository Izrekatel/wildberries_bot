from django.db import models


class Base(models.Model):
    """Абстрактная модель. Добавляет ID и дату создания."""

    id = models.AutoField(primary_key=True)
    add_time = models.DateTimeField(
        verbose_name="Время добавления", auto_now_add=True, db_index=True
    )

    class Meta:
        abstract = True


class TelegramUser(Base):
    user_id = models.PositiveIntegerField(unique=True, editable=False)
    e_mail = models.EmailField(blank=True)

    class Meta:
        verbose_name = "Пользователь телеграм"
        verbose_name_plural = "Пользователи телеграм"

    def __str__(self):
        return f"Пользователь {self.user_id}"


class FrequencyRequestPosition(models.Model):
    frequency = models.PositiveIntegerField(unique=True)

    class Meta:
        verbose_name = "Частота, час"
        verbose_name_plural = "Частота, часы"

    def __str__(self):
        return f"Частота обновления: {self.frequency} час/часов."


class RequestPosition(Base):
    articul = models.IntegerField()
    text = models.CharField(max_length=255)
    telegram_user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        blank=False,
        related_name="subscribers",
        verbose_name="Подписчик",
    )
    frequency = models.ForeignKey(
        FrequencyRequestPosition,
        on_delete=models.PROTECT,
        blank=False,
        related_name="frequencies",
        verbose_name="Частота",
    )
    last_request = models.DateTimeField(
        verbose_name="Время последнего запроса",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Запрос позиции артикула"
        verbose_name_plural = "Запросы позиций артикулов"
        constraints = (
            models.UniqueConstraint(
                fields=("articul", "text", "telegram_user"),
                name="unique_articul_text_telegram_user",
            ),
        )

    def __str__(self):
        return f"Артикул: {self.articul}, текст: {self.text}"


class RequestStock(Base):
    articul = models.IntegerField()
    telegram_user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        blank=False,
        related_name="user",
        verbose_name="Пользователь",
    )

    class Meta:
        verbose_name = "Запрос остатков"
        verbose_name_plural = "Запросы остатков"

    def __str__(self):
        return f"Артикул: {self.articul}"


class RequestRate(Base):
    warehouse_id = models.IntegerField()
    telegram_user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        blank=False,
        related_name="telegram_user",
        verbose_name="Пользователь",
    )

    class Meta:
        verbose_name = "Коэффициент приемки"
        verbose_name_plural = "Коэффициенты приемки"

    def __str__(self):
        return f"Warehouse_id: {self.warehouse_id}"
