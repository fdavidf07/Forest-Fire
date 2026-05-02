from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Simulation
from .serializers import SimulationSerializer
from .engine import ForestFireEngine
from .weather import get_suggested_params
import numpy as np

# --- VISTA PARA EL FRONTEND (RA9) ---

def index(request):
    """
    Punto de entrada para la SPA. Simplemente carga el HTML base 
    donde vive el Canvas y toda la lógica de JS.
    """
    return render(request, 'index.html')


# --- ENDPOINTS DE LA API (RA7) ---

class SimulationListCreateView(APIView):
    """
    Se encarga de la creación inicial de la simulación.
    """
    def post(self, request):
        # Pasamos los datos por el serializer para validar que 'size' 
        # y los parámetros p/f tengan sentido antes de tocar la BD.
        serializer = SimulationSerializer(data=request.data)
        
        if serializer.is_valid():
            size = serializer.validated_data['size']
            p = serializer.validated_data['p']
            f = serializer.validated_data['f']
            
            # Instanciamos el motor para generar la rejilla inicial aleatoria.
            # Separamos la lógica matemática (engine.py) de la vista.
            engine = ForestFireEngine(size, p, f)
            
            # Guardamos el estado inicial. La rejilla se guarda como lista JSON
            # para que el frontend la pueda pintar directamente.
            simulation = Simulation.objects.create(
                size=size,
                p=p,
                f=f,
                grid=engine.grid.tolist(),
                tree_density=np.count_nonzero(engine.grid == 1) / (size**2)
            )
            return Response(SimulationSerializer(simulation).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SimulationDetailView(APIView):
    """
    CRUD básico para una simulación específica.
    """
    def get(self, request, id):
        try:
            sim = Simulation.objects.get(id=id)
            return Response(SimulationSerializer(sim).data)
        except Simulation.DoesNotExist:
            return Response({"error": "No encuentro esa simulación"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        """
        Permite ajustar p y f sobre la marcha (en caliente) sin 
        tener que reiniciar toda la simulación.
        """
        try:
            sim = Simulation.objects.get(id=id)
            if 'p' in request.data: sim.p = request.data['p']
            if 'f' in request.data: sim.f = request.data['f']
            sim.save()
            return Response(SimulationSerializer(sim).data)
        except Simulation.DoesNotExist:
            return Response({"error": "No se puede actualizar lo que no existe"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        # Limpieza de recursos en la base de datos.
        Simulation.objects.filter(id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SimulationStepView(APIView):
    """
    Este es el corazón del avance temporal. Usamos POST porque 
    cada llamada cambia el estado interno (no es una simple consulta).
    """
    def post(self, request, id):
        try:
            sim = Simulation.objects.get(id=id)
            steps = int(request.data.get('steps', 1))
            
            # Rehidratamos el motor con los datos que teníamos guardados.
            # Así el motor no pierde la "memoria" del bosque actual.
            engine = ForestFireEngine(sim.size, sim.p, sim.f, grid=sim.grid)
            
            # Sacamos el diccionario del historial para ir acumulando los tamaños.
            history = sim.fire_size_history 
            
            for _ in range(steps):
                # Avanzamos un paso y el motor nos dice qué incendios ha detectado.
                grid, fire_clusters = engine.step()
                
                # Actualizamos las estadísticas del histograma.
                # Esto es vital para comprobar la Ley de Potencia más tarde.
                for size in fire_clusters:
                    s_key = str(size)
                    history[s_key] = history.get(s_key, 0) + 1
            
            # Sincronizamos los cambios de vuelta a la base de datos.
            sim.grid = engine.grid.tolist()
            sim.fire_size_history = history 
            sim.steps_count += steps
            sim.tree_density = np.count_nonzero(engine.grid == 1) / (sim.size**2)
            sim.save()
            
            return Response(SimulationSerializer(sim).data)
        except Simulation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class WeatherView(APIView):
    """
    Puente con la API de Open-Meteo. 
    Sirve para que el usuario no tenga que inventarse p y f.
    """
    def get(self, request):
        city = request.query_params.get('city')
        if not city:
            return Response({"error": "Falta el nombre de la ciudad"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Llamamos al módulo externo que procesa la lógica del clima.
        params = get_suggested_params(city)
        if not params:
            return Response({"error": "Ciudad no encontrada o servicio caído"}, status=status.HTTP_404_NOT_FOUND)
            
        return Response(params)