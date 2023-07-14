from django.db import models


class Base(models.Model):
    """Абстрактная модель. Добавляет дату создания."""
    id = models.AutoField(primary_key=True)
    add_time = models.DateTimeField(
        verbose_name='Время добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True


class TelegramUser(Base):
    user_id = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"Пользователь {self.user_id}"


class RequestPosition(Base):
    articul = models.IntegerField()
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"Артикул: {self.articul}, текст: {self.text}"


class RequestStock(Base):
    articul = models.IntegerField()

    def __str__(self):
        return f"Артикул: {self.articul}"


class RequestRate(Base):
    warehouse_id = models.IntegerField()

    def __str__(self):
        return f"Warehouse_id: {self.warehouse_id}"
