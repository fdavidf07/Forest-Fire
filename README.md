# 🔥 Forest Fire Simulator (Modelo Drossel-Schwabl)

Este proyecto es un simulador de incendios forestales basado en el autómata celular de **Drossel y Schwabl**. Permite visualizar cómo se propaga el fuego en un bosque dinámico, integrando datos meteorológicos reales para ajustar el comportamiento de la simulación.

## 🚀 Características principales

*   **Motor de Simulación**: Implementado en Python con **NumPy** para un procesamiento eficiente de matrices.
*   **API REST**: Desarrollada con **Django REST Framework** para gestionar el estado de la simulación y las estadísticas.
*   **Visualización en tiempo real**: Cliente web dinámico usando **HTML5 Canvas** y JavaScript moderno.
*   **Datos Reales (Open-Meteo)**: Integración con la API de Open-Meteo para sugerir parámetros de crecimiento de árboles ($p$) y caída de rayos ($f$) basados en el clima de cualquier ciudad.
*   **Análisis Estadístico**: Registro del historial de tamaños de incendios para verificar la **Ley de Potencia**.

## 🛠️ Tecnologías utilizadas

*   **Backend**: Python 3.11+, Django, Django REST Framework.
*   **Frontend**: JavaScript (Vanilla), HTML5, CSS3.
*   **Gestión de Dependencias**: [uv](https://github.com/astral-sh/uv) (rápido y con bloqueo de versiones mediante `uv.lock`).
*   **Lógica Matemática**: NumPy para el cálculo de clústeres y estados de la rejilla.

## 📦 Instalación y uso

Este proyecto utiliza `uv` para una gestión de dependencias ultra rápida.

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/forest-fire.git](https://github.com/tu-usuario/forest-fire.git)
   cd forest-fire
