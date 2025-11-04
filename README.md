# Flappy_Bird_IA_MachineLearning

Este proyecto forma parte de mi aprendizaje en el campo de la **Inteligencia Artificial** y el **Machine Learning**, dentro de mi formación en un **Ciclo de Especialización en Inteligencia Artificial y Big Data**.  

He desarrollado una versión del clásico *Flappy Bird* donde una **IA aprende a jugar por sí sola** utilizando el algoritmo **NEAT (NeuroEvolution of Augmenting Topologies)**.  
El objetivo del agente es mejorar con cada generación, aprendiendo a **esquivar los tubos y mantenerse en vuelo** el mayor tiempo posible.

---

## Características principales
- Juego programado en **Python** utilizando **Pygame**.  
- Entrenamiento de la IA con **NEAT-Python**.  
- Configuración flexible mediante el archivo `config-feedforward.txt`.  
- Visualización en tiempo real del progreso del entrenamiento.  
- Ejecución tanto de forma local como mediante **Docker** (opcional).

---

## Estructura del proyecto
Flappy_Bird_IA_MachineLearning

├── flappy-ai.py # Código principal del juego y la IA

├── config-feedforward.txt # Configuración de la red neuronal (NEAT)

├── Dockerfile # (Opcional) Imagen para ejecutar con Docker

├── docker-compose.yml # (Opcional) Configuración de Docker Compose

└── README.md # Descripción del proyecto


---

## Requisitos
Si decides ejecutar el proyecto sin Docker, asegúrate de tener instalado:

```bash
Python 3.8+
Pygame
neat-python

```
---
Ejecución local
```
python flappy-ai.py
```
Ejecución Docker
```
docker-compose up
