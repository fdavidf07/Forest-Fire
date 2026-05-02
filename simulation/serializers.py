from rest_framework import serializers
from .models import Simulation

class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = ['id', 'size', 'p', 'f', 'grid', 'steps_count', 'tree_density', 'fire_size_history']
        read_only_fields = ['id', 'grid', 'steps_count', 'tree_density', 'fire_size_history']

    def validate_size(self, value):
        # Validación obligatoria según el enunciado
        if value < 20 or value > 200:
            raise serializers.ValidationError("El tamaño debe estar entre 20 y 200.")
        return value