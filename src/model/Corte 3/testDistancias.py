import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Cargar los datos de distancia desde el archivo CSV
distance_data_path = r'C:\Users\juans\OneDrive\Desktop\8vo Semestre\Intro Sistemas Inteligentes\Proyecto1_Sistemas_Inteligentes\data\Corte 3\distancias_ciudades_colombia.csv'
distance_df = pd.read_csv(distance_data_path)

# Obtener las ciudades y formar la matriz de distancias
cities = sorted(set(distance_df['Origen']).union(set(distance_df['Destino'])))
city_index = {city: idx for idx, city in enumerate(cities)}
n_cities = len(cities)

# Inicializar la matriz de distancias
distance_matrix = np.full((n_cities, n_cities), np.inf)
for _, row in distance_df.iterrows():
    origin, destination, distance = row['Origen'], row['Destino'], row['Distancia (km)']
    i, j = city_index[origin], city_index[destination]
    distance_matrix[i, j] = distance
np.fill_diagonal(distance_matrix, 0)

# Parámetros del algoritmo de luciérnagas
num_iterations = 20000
num_fireflies = 50
beta = 1
gamma = 0.01
initial_alpha = 0.1

# Inicializar las luciérnagas con rutas que comienzan y terminan en Bogotá
bogota_index = city_index['Bogotá']
fireflies = [
    [bogota_index] + random.sample([i for i in range(n_cities) if i != bogota_index], n_cities - 1) + [bogota_index]
    for _ in range(num_fireflies)
]

distances = []
for firefly in fireflies:
    distance = sum(distance_matrix[firefly[k], firefly[k + 1]] for k in range(len(firefly) - 1))
    distances.append(distance)

# Variables para rastrear la mejor ruta
best_route = None
best_distance = float('inf')

for iteration in range(num_iterations):
    alpha = initial_alpha * (1 - iteration / num_iterations)  # Reducir aleatoriedad gradualmente
    for i in range(num_fireflies):
        for j in range(num_fireflies):
            if distances[j] < distances[i]:  # Si la luciérnaga j es "más brillante"
                # Crear una nueva ruta intercambiando dos ciudades (excluyendo Bogotá)
                new_route = fireflies[i][1:-1]
                swap_idx1, swap_idx2 = random.sample(range(len(new_route)), 2)
                new_route[swap_idx1], new_route[swap_idx2] = new_route[swap_idx2], new_route[swap_idx1]
                new_route = [bogota_index] + new_route + [bogota_index]

                # Calcular la nueva distancia
                new_distance = sum(distance_matrix[new_route[k], new_route[k + 1]] for k in range(len(new_route) - 1))

                # Aceptar la nueva ruta si mejora la distancia
                if new_distance < distances[i]:
                    fireflies[i] = new_route
                    distances[i] = new_distance

    # Seguimiento de la mejor ruta en esta iteración
    min_distance_idx = distances.index(min(distances))
    if distances[min_distance_idx] < best_distance:
        best_distance = distances[min_distance_idx]
        best_route = fireflies[min_distance_idx][:]

    # Incorporar la mejor ruta en la población ocasionalmente
    if iteration % 10 == 0 and best_route is not None:
        # Reemplazar algunas luciérnagas con la mejor ruta perturbada
        num_to_replace = int(num_fireflies * 0.1)  # Reemplazar el 10% de las luciérnagas
        indices_to_replace = random.sample(range(num_fireflies), num_to_replace)
        for idx in indices_to_replace:
            # Perturbar ligeramente la mejor ruta
            perturbed_route = best_route[1:-1][:]
            if len(perturbed_route) > 1:
                swap_idx1, swap_idx2 = random.sample(range(len(perturbed_route)), 2)
                perturbed_route[swap_idx1], perturbed_route[swap_idx2] = perturbed_route[swap_idx2], perturbed_route[swap_idx1]
            fireflies[idx] = [bogota_index] + perturbed_route + [bogota_index]
            distances[idx] = sum(distance_matrix[fireflies[idx][k], fireflies[idx][k + 1]] for k in range(len(fireflies[idx]) - 1))

    # Imprimir el progreso
    print(f"Iteración {iteration + 1}: Mejor distancia hasta ahora = {best_distance}")

# Traducir la mejor ruta de índices a nombres de ciudades
best_route_cities = [cities[i] for i in best_route]

# Imprimir la mejor distancia y la mejor ruta
print("Mejor distancia encontrada:", best_distance)
print("Mejor ruta:", " -> ".join(best_route_cities))

# Configuración de animación (sin cambios)
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

# Crear la figura y el eje
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_title("Optimización TSP con el Algoritmo de Luciérnagas")
ax.set_xlabel("Longitud")
ax.set_ylabel("Latitud")

# Dibujar las posiciones de las ciudades
ax.scatter(city_positions[:, 1], city_positions[:, 0], color='blue', s=30, label="Ciudades")
for i, city in enumerate(cities):
    if city in city_coords:
        ax.text(city_positions[i, 1], city_positions[i, 0], city, fontsize=8, ha='right')

# Crear líneas para cada luciérnaga y la mejor ruta
lines = [ax.plot([], [], lw=0.5, alpha=0.4, color="gray")[0] for _ in range(num_fireflies)]
best_line, = ax.plot([], [], color='red', lw=1.5, label="Mejor Ruta")

# Función de actualización para la animación
def update(frame):
    # Actualizar la posición de cada luciérnaga
    for i, route in enumerate(fireflies):
        route_positions = np.array([city_coords[cities[city]] for city in route if cities[city] in city_coords])
        lines[i].set_data(route_positions[:, 1], route_positions[:, 0])
    
    # Actualizar la mejor ruta
    best_route_positions = np.array([city_coords[cities[city]] for city in best_route if cities[city] in city_coords])
    best_line.set_data(best_route_positions[:, 1], best_route_positions[:, 0])

# Animación
anim = FuncAnimation(fig, update, frames=num_iterations, repeat=False, interval=100)

# Mostrar la animación
plt.legend()
plt.show()
