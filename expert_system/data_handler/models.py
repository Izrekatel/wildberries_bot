from django.db import models


class Base(models.Model):
    """Абстрактная модель. Добавляет ID и дату создания."""

    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
    )
    add_time = models.DateTimeField(
        verbose_name="Время добавления",
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        abstract = True


class TelegramUser(Base):
    user_id = models.PositiveIntegerField(
        unique=True,
        editable=False,
    )
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
    user_id = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        blank=False,
        to_field="user_id",
        related_name="subscribers",
        verbose_name="Подписчик",
    )
    frequency = models.ForeignKey(
        FrequencyRequestPosition,
        on_delete=models.PROTECT,
        blank=False,
        to_field="frequency",
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
                fields=("articul", "text", "user_id"),
                name="unique_articul_text_user_id",
            ),
        )

    def __str__(self):
        return f"Артикул: {self.articul}, текст: {self.text}"


class RequestStock(Base):
    articul = models.IntegerField()
    user_id = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        to_field="user_id",
        blank=False,
        related_name="user_stock",
        verbose_name="Пользователь",
    )

    class Meta:
        verbose_name = "Запрос остатков"
        verbose_name_plural = "Запросы остатков"
        constraints = (
            models.UniqueConstraint(
                fields=("articul", "user_id"),
                name="unique_articul_user_id",
            ),
        )

    def __str__(self):
        return f"Артикул: {self.articul}"


class RequestRate(Base):
    warehouse_id = models.IntegerField()
    user_id = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        blank=False,
        to_field="user_id",
        related_name="user_rate",
        verbose_name="Пользователь",
    )

    class Meta:
        verbose_name = "Коэффициент приемки"
        verbose_name_plural = "Коэффициенты приемки"
        constraints = (
            models.UniqueConstraint(
                fields=("warehouse_id", "user_id"),
                name="unique_warehouse_id_user_id",
            ),
        )

    def __str__(self):
        return f"Warehouse_id: {self.warehouse_id}"


class City(models.Model):
    city = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return f"Город: {self.city}, локация: {self.location}."


class Warehouse(models.Model):
    number = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"

    def __str__(self):
        return f"Номер склада: {self.number}, название: {self.name}."
