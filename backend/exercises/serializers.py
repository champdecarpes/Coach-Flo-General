from rest_framework import serializers
from .models import Exercise, TrackingFields


class TrackingFieldsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели TrackingFields.
    Преобразует все поля модели в JSON и обратно, включая TimeField и DecimalField.
    """

    class Meta:
        model = TrackingFields
        fields = '__all__'


class ExerciseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Exercise.
    Обрабатывает все поля, включая вложенную модель TrackingFields через OneToOneField.
    """
    tracking_fields = TrackingFieldsSerializer()

    class Meta:
        model = Exercise
        fields = '__all__'

    def validate_monitored_fields(self, value):
        """
        Валидация поля monitored_fields, чтобы убедиться, что оно содержит не более 3 элементов.
        """
        if value and len(value) > 3:
            raise serializers.ValidationError("Можно мониторить не более 3 полей.")
        return value

    def create(self, validated_data):
        """
        Создание нового экземпляра Exercise с вложенной моделью TrackingFields.
        Извлекает данные tracking_fields, создает связанный объект и сохраняет Exercise.
        """

        # Может вызвать ошибку, если tracking_fields будет пустым
        tracking_data = validated_data.pop('tracking_fields')
        tracking_instance = TrackingFields.objects.create(**tracking_data)
        exercise_instance = Exercise.objects.create(tracking_fields=tracking_instance, **validated_data)
        return exercise_instance

    def update(self, instance, validated_data):
        """
        Обновление существующего экземпляра Exercise и связанной модели TrackingFields.
        Обновляет данные tracking_fields и сохраняет изменения в обеих моделях.
        """
        tracking_data = validated_data.pop('tracking_fields')
        tracking_instance = instance.tracking_fields
        for attr, value in tracking_data.items():
            setattr(tracking_instance, attr, value)
        tracking_instance.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
