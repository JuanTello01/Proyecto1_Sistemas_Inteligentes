"""
Este script implementa el Algoritmo de Luciérnagas para resolver el Problema del Viajante (TSP) en Colombia.

El algoritmo optimiza una ruta que visita varias ciudades de Colombia, minimizando la distancia total recorrida, utilizando un enfoque inspirado en el comportamiento de las luciérnagas.

A continuación se detalla cada fragmento del código:

1. Importación de librerías necesarias:

Se importan las librerías necesarias para la manipulación de datos (`pandas`, `numpy`), generación de números aleatorios (`random`), visualización de datos (`matplotlib`), y animación (`FuncAnimation`).

2. Carga de datos de distancia desde un archivo CSV:

Se define la ruta del archivo CSV que contiene las distancias entre las ciudades y se carga en un DataFrame de pandas.

3. Procesamiento de datos de ciudades y creación de la matriz de distancias:

Se obtienen los nombres de las ciudades únicas y se asigna un índice a cada una para su manejo en matrices.

Se crea una matriz de distancias donde cada elemento `(i, j)` representa la distancia desde la ciudad `i` hasta la ciudad `j`. Las distancias iniciales se establecen en infinito y luego se llenan con los datos del DataFrame. Se establecen ceros en la diagonal principal, ya que la distancia de una ciudad a sí misma es cero.

4. Definición de parámetros del algoritmo de luciérnagas:

Se establecen los parámetros del algoritmo: número de iteraciones, número de luciérnagas, coeficientes beta y gamma, y el valor inicial de alpha (aleatoriedad).

5. Inicialización de las luciérnagas con rutas aleatorias:

Se generan rutas aleatorias para cada luciérnaga, comenzando y terminando en Bogotá. Se utiliza `random.sample` para crear permutaciones aleatorias de las ciudades.

6. Cálculo de las distancias iniciales de las luciérnagas:

Se calcula la distancia total recorrida en la ruta de cada luciérnaga y se almacena en una lista.

7. Variables para rastrear la mejor ruta encontrada:

Se inicializan las variables que almacenarán la mejor ruta y la menor distancia encontrada durante las iteraciones.

8. Bucle principal del algoritmo de luciérnagas:

En cada iteración, se reduce gradualmente la aleatoriedad `alpha`. Luego, para cada par de luciérnagas, si una luciérnaga es más brillante (tiene una ruta más corta), la otra luciérnaga se mueve hacia ella.

9. Movimiento de las luciérnagas hacia las más brillantes:

Se crea una nueva ruta para la luciérnaga `i` intercambiando dos ciudades en su ruta actual (excluyendo Bogotá).

10. Cálculo de la nueva distancia y actualización si mejora:

Se calcula la distancia de la nueva ruta y, si es mejor que la anterior, se actualiza la ruta y la distancia de la luciérnaga `i`.

11. Actualización de la mejor ruta global:

Se verifica si en esta iteración se ha encontrado una ruta mejor que la mejor conocida hasta ahora y se actualiza si es necesario.

12. Incorporación ocasional de la mejor ruta en la población:

Cada 10 iteraciones, se reemplaza el 10% de las luciérnagas por versiones ligeramente perturbadas de la mejor ruta encontrada, para explorar el entorno de esa solución.

13. Impresión del progreso:

Se imprime en consola el número de iteración y la mejor distancia encontrada hasta ese punto.

14. Conversión de la mejor ruta de índices a nombres de ciudades:

Se traduce la mejor ruta encontrada de índices numéricos a nombres de ciudades para su interpretación.

15. Impresión de la mejor distancia y ruta:

Se muestran en pantalla la mejor distancia total recorrida y la secuencia de ciudades de la mejor ruta.

16. Configuración de la visualización y animación:

Se configuran los elementos para la visualización de las rutas en un mapa, incluyendo las posiciones de las ciudades y sus etiquetas.

17. Preparación de las líneas para animar las rutas de las luciérnagas:

Se crean objetos de línea para cada luciérnaga y para la mejor ruta, que serán actualizados en cada cuadro de la animación.

18. Función de actualización para la animación:

Esta función actualiza las posiciones de las líneas en la animación, mostrando el movimiento de las luciérnagas y resaltando la mejor ruta encontrada.

19. Creación y visualización de la animación:

Se crea la animación utilizando `FuncAnimation` y se muestra la figura con la leyenda correspondiente.

En resumen, este código implementa una metaheurística basada en el comportamiento de las luciérnagas para resolver el TSP, visualizando el proceso de optimización y mostrando la mejor ruta encontrada entre las ciudades de Colombia.
"""



import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

distance_data_path = r'C:\Users\juans\OneDrive\Desktop\8vo Semestre\Intro Sistemas Inteligentes\Proyecto1_Sistemas_Inteligentes\data\Corte 3\distancias_ciudades_colombia.csv'
distance_df = pd.read_csv(distance_data_path)

cities = sorted(set(distance_df['Origen']).union(set(distance_df['Destino'])))
city_index = {city: idx for idx, city in enumerate(cities)}
n_cities = len(cities)

distance_matrix = np.full((n_cities, n_cities), np.inf)
for _, row in distance_df.iterrows():
    origin, destination, distance = row['Origen'], row['Destino'], row['Distancia (km)']
    i, j = city_index[origin], city_index[destination]
    distance_matrix[i, j] = distance
np.fill_diagonal(distance_matrix, 0)

num_iterations = 5000
num_fireflies = 50
beta = 1
gamma = 0.01
initial_alpha = 0.1

bogota_index = city_index['Bogotá']
fireflies = [
    [bogota_index] + random.sample([i for i in range(n_cities) if i != bogota_index], n_cities - 1) + [bogota_index]
    for _ in range(num_fireflies)
]

distances = []
for firefly in fireflies:
    distance = sum(distance_matrix[firefly[k], firefly[k + 1]] for k in range(len(firefly) - 1))
    distances.append(distance)

best_route = None
best_distance = float('inf')
best_distances = []


for iteration in range(num_iterations):
    alpha = initial_alpha * (1 - iteration / num_iterations) 
    for i in range(num_fireflies):
        for j in range(num_fireflies):
            if distances[j] < distances[i]: 
                new_route = fireflies[i][1:-1]
                swap_idx1, swap_idx2 = random.sample(range(len(new_route)), 2)
                new_route[swap_idx1], new_route[swap_idx2] = new_route[swap_idx2], new_route[swap_idx1]
                new_route = [bogota_index] + new_route + [bogota_index]


                new_distance = sum(distance_matrix[new_route[k], new_route[k + 1]] for k in range(len(new_route) - 1))

                if new_distance < distances[i]:
                    fireflies[i] = new_route
                    distances[i] = new_distance
                

    min_distance_idx = distances.index(min(distances))
    if distances[min_distance_idx] < best_distance:
        best_distance = distances[min_distance_idx]
        best_route = fireflies[min_distance_idx][:]

    if iteration % 10 == 0 and best_route is not None:
        num_to_replace = int(num_fireflies * 0.1) 
        indices_to_replace = random.sample(range(num_fireflies), num_to_replace)
        for idx in indices_to_replace:
            perturbed_route = best_route[1:-1][:]
            if len(perturbed_route) > 1:
                swap_idx1, swap_idx2 = random.sample(range(len(perturbed_route)), 2)
                perturbed_route[swap_idx1], perturbed_route[swap_idx2] = perturbed_route[swap_idx2], perturbed_route[swap_idx1]
            fireflies[idx] = [bogota_index] + perturbed_route + [bogota_index]
            distances[idx] = sum(distance_matrix[fireflies[idx][k], fireflies[idx][k + 1]] for k in range(len(fireflies[idx]) - 1))
    best_distances.append(best_distance)
    # Imprimir el progreso
    print(f"Iteración {iteration + 1}: Mejor distancia hasta ahora = {best_distance}")

best_route_cities = [cities[i] for i in best_route]

print("Mejor distancia encontrada:", best_distance)
print("Mejor ruta:", " -> ".join(best_route_cities))

city_coords = {
    'Leticia': (-4.2150, -69.9406), 'Medellín': (6.2442, -75.5812), 'Arauca': (7.0844, -70.7591),
    'Barranquilla': (10.9685, -74.7813), 'Cartagena de Indias': (10.3910, -75.4794), 'Tunja': (5.5353, -73.3678),
    'Manizales': (5.0703, -75.5138), 'Florencia': (1.6144, -75.6062), 'Yopal': (5.3378, -72.3959),
    'Popayán': (2.4448, -76.6147), 'Valledupar': (10.4631, -73.2532), 'Quibdó': (5.6947, -76.6611),
    'Montería': (8.7479, -75.8814), 'Bogotá': (4.7110, -74.0721), 'Inírida': (3.8653, -67.9235),
    'San José del Guaviare': (2.5667, -72.6389), 'Neiva': (2.9273, -75.2819), 'Riohacha': (11.5444, -72.9073),
    'Santa Marta': (11.2408, -74.1990), 'Villavicencio': (4.1420, -73.6266), 'San Juan de Pasto': (1.2136, -77.2811),
    'Cúcuta': (7.8898, -72.4966), 'Mocoa': (1.1522, -76.6498), 'Armenia': (4.5339, -75.6811),
    'Pereira': (4.8087, -75.6906), 'San Andrés': (12.5847, -81.7004), 'Bucaramanga': (7.1193, -73.1227),
    'Sincelejo': (9.3047, -75.3978), 'Ibagué': (4.4389, -75.2322), 'Cali': (3.4516, -76.5319),
    'Mitú': (1.1983, -70.1730), 'Puerto Carreño': (6.1894, -67.4856)
}
city_positions = np.array([city_coords[city] for city in cities if city in city_coords])

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_title("Optimización TSP con el Algoritmo de Luciérnagas")
ax.set_xlabel("Longitud")
ax.set_ylabel("Latitud")

ax.scatter(city_positions[:, 1], city_positions[:, 0], color='blue', s=30, label="Ciudades")
for i, city in enumerate(cities):
    if city in city_coords:
        ax.text(city_positions[i, 1], city_positions[i, 0], city, fontsize=8, ha='right')

lines = [ax.plot([], [], lw=0.5, alpha=0.4, color="gray")[0] for _ in range(num_fireflies)]
best_line, = ax.plot([], [], color='red', lw=1.5, label="Mejor Ruta")

def update(frame):
    for i, route in enumerate(fireflies):
        route_positions = np.array([city_coords[cities[city]] for city in route if cities[city] in city_coords])
        lines[i].set_data(route_positions[:, 1], route_positions[:, 0])
    
    best_route_positions = np.array([city_coords[cities[city]] for city in best_route if cities[city] in city_coords])
    best_line.set_data(best_route_positions[:, 1], best_route_positions[:, 0])

anim = FuncAnimation(fig, update, frames=num_iterations, repeat=False, interval=100)

plt.legend()
plt.show()


plt.figure(figsize=(10, 6))
plt.plot(range(1, num_iterations + 1), best_distances, label='Mejor distancia')
plt.title('Convergencia del Algoritmo de Luciérnagas')
plt.xlabel('Iteraciones')
plt.ylabel('Mejor distancia encontrada')
plt.legend()
plt.grid(True)
plt.show()

plt.savefig('convergencia_algoritmo_luciernagas.png')

