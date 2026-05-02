# Reflexiones sobre el Proyecto: Simulador de Incendios

### 1. ¿Por qué hemos usado un método POST y no un GET para el endpoint de `/step/`?
Aunque estemos "pidiendo" que la simulación avance y nos devuelva datos, en realidad estamos modificando el estado del servidor. Si usáramos un `GET`, se supone que solo estamos consultando información sin cambiar nada. Pero aquí, cada vez que llamamos a `/step/`, la base de datos se actualiza: el bosque cambia, el contador de pasos sube y el historial de incendios crece. Por eso se usa `POST`, porque la operación no es "idempotente" (si la llamas varias veces, el resultado en el servidor cambia cada vez).

### 2. ¿Qué ventajas e inconvenientes tiene guardar el estado de la simulación en el servidor en lugar de en el navegador?
**Ventajas:**
*   **Persistencia real:** Puedo cerrar el navegador, irme a tomar un café, volver y la simulación sigue donde estaba. No se pierde nada al refrescar la página.
*   **Control total:** Al estar en el servidor, los cálculos pesados (como el motor de incendios con Numpy) no dependen de si el móvil o el ordenador del usuario son lentos.

**Inconvenientes:**
*   **Carga del servidor:** Si 100 personas se ponen a simular a la vez bosques de 200x200, el servidor va a sufrir bastante procesando tantas matrices.
*   **Latencia:** Cada paso tiene que ir y volver por internet. Si la conexión va mal, la simulación se nota "a tirones" comparado con si se hiciera directamente en el navegador.

### 3. ¿Qué ocurre con la simulación al variar los parámetros $p$ y $f$? ¿Se observa algún comportamiento especial?
He estado probando y se nota mazo la diferencia. Si subes mucho la $p$ (la probabilidad de que crezcan árboles), el bosque se llena súper rápido. Cuando cae un rayo ($f$) o empieza un fuego, se propaga de golpe por todo el mapa porque hay árboles por todos lados; es lo que llaman el estado crítico. Si la $p$ es muy baja, el fuego se apaga pronto porque no tiene "gasolina" (árboles) cerca para saltar. Es curioso ver cómo al ajustar los valores de Open-Meteo, el sistema se comporta de forma mucho más realista.

### 4. ¿Dónde has implementado la validación del parámetro `size` (entre 20 y 200) y por qué?
La he puesto en el **Serializer** de Django REST Framework (en `serializers.py`). Me parece el mejor sitio porque es la primera barrera de seguridad. Si el usuario intenta crear una simulación de tamaño 1 o de 5000, el Serializer lo corta antes de que el código intente siquiera crear el objeto o mover el motor. Así nos ahorramos errores raros en la base de datos o que el servidor explote por falta de memoria.

### 5. ¿Qué ventaja aporta usar `uv` frente a un simple `pip freeze > requirements.txt`?
Después de usarlo en este proyecto, `uv` me parece mucho más moderno. La principal ventaja es el archivo `uv.lock`. Con un `requirements.txt` normal, a veces las versiones de las librerías que dependen de otras librerías (las transitivas) cambian y te rompen el proyecto. Con `uv`, el archivo lock asegura que todo el mundo (o yo mismo si cambio de PC) tenga **exactamente** los mismos bits instalados. Además, es increíblemente más rápido instalando cosas que el `pip` de toda la vida.