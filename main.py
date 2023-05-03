# IMPORTS #
import math
from typing import Dict, List

# CLASE GRAFO #
# Toma un diccionario de vértices como entrada, donde cada vértice es una llave, y su valor es otro diccionario
# que representa vértices conectados

# Ejemplo de una entrada para la clase Grafo #
"""
Grafo(
    vertices={
        "A": {"B": 7, "D": 5},
        "B": {"A": 7, "C": 8, "D": 9, "E": 7},
        "C": {"B": 8, "E": 5},
        "D": {"A": 5, "B": 9, "E": 15, "F": 6},
        'E': {'B': 7, 'C': 5, 'D': 15, 'F': 8, 'G': 9},
        'F': {'D': 6, 'E': 8, 'G': 11},
        'G': {'E': 9, 'F': 11}
    }
)
"""
# Vertices es un diccionario con los vértices A -> G como llave, y el valor de cada uno es un diccionario
# que indica a cuáles vértices se encuentran conectados

class Grafo:
    def __init__(self, vertices: Dict[str, Dict[str, float]]):
        self.vertices = vertices

# CLASE CAMINO #
# Guarda información sobre el camino más corto. Tiene dos parámetros:
# Anterior: El vértice anterior en el camino
# Longitud: La longitud del camino hasta ese vértice
class Camino:
    def __init__(self, anterior: str, longitud: float):
        self.anterior = anterior
        self.longitud = longitud

# FUNCIÓN DIJKSTRA #
# Toma 3 argumentos:
# - Un objeto g de tipo Grafo
# - El vértice de origen 
# - El vértice de destino
# La función regresa una tupla que contiene la longitud del camino más corto desde 'origen' hasta 'destino'
# y una lista de vértices que representan el camino
def dijkstra(g: Grafo, origen: str, destino: str) -> tuple[float, List[str]]:
    # Inicializar la tabla de caminos
    caminos = {v: Camino(anterior="", longitud=math.inf) for v in g.vertices}
    visitados = {v: False for v in g.vertices}
    caminos[origen] = Camino(anterior="", longitud=0)

    # Encontrar el camino más corto
    actual = origen
    while True:
        # Marcar el vértice actual como visitado
        visitados[actual] = True

        # Actualizar las distancias de los vértices adyacentes
        for vecino, distancia in g.vertices[actual].items():
            if not visitados[vecino]:
                if caminos[actual].longitud + distancia < caminos[vecino].longitud:
                    caminos[vecino] = Camino(anterior=actual, longitud=caminos[actual].longitud + distancia)

        # Seleccionar el vértice no visitado más cercano al origen
        distancia_minima = math.inf
        for v, cam in caminos.items():
            if not visitados[v] and cam.longitud < distancia_minima:
                distancia_minima = cam.longitud
                actual = v

        # Si no hay vértices no visitados, hemos terminado
        if actual == destino or distancia_minima == math.inf:
            break

    # Construir el camino
    camino = [destino]
    v = destino
    while True:
        if v == origen:
            break
        camino.insert(0, caminos[v].anterior)
        v = caminos[v].anterior

    return caminos[destino].longitud, camino

# FUNCIÓN generarCodigoGraphviz # 
# La función recibe 4 argumentos:
# -	Una clase Grafo g
# -	Un vértice de origen como cadena de texto
# -	Un vértice de destino como cadena de texto
# -	Una lista de vértices ‘camino’ que representa el camino más corto entre los vértices dado
# La función regresa una cadena de texto que representa un código de Graphviz que puede ser usada
# para dibujar el grafo y resaltar el camino más corto.
def generarCodigoGraphviz(g: Grafo, origen: str, destino: str, camino: List[str]) -> str:
    b = ["digraph {"]
    
    # Dibujar los nodos
    for v in g.vertices:
        b.append(f'  {v} [label="{v}"]')

    # Dibujar las aristas
    for origen, destinos in g.vertices.items():
        for destino, longitud in destinos.items():
            b.append(f'  {origen} -> {destino}')

    # Dibujar la ruta más corta
    for i in range(len(camino) - 1):
        b.append(f'  {camino[i]} -> {camino[i+1]} [color=red, penwidth=2.0]')

    b.append("}")
    return "\n".join(b)


"""
if __name__ == "__main__":
    g = Grafo(vertices={
        "A": {"B": 7, "D": 5},
        "B": {"A": 7, "C": 8, "D": 9, "E": 7},
        "C": {"B": 8, "E": 5},
        "D": {"A": 5, "B": 9, "E": 15, "F": 6},
        'E': {'B': 7, 'C': 5, 'D': 15, 'F': 8, 'G': 9},
        'F': {'D': 6, 'E': 8, 'G': 11},
        'G': {'E': 9, 'F': 11}})
    origen = 'A'
    destino = 'G'

    longitud, camino = dijkstra(g, origen, destino)

    print(f"El camino más corto desde {origen} hasta {destino} es:")
    print(camino)

    print(f"Longitud del camino más corto: {longitud}")

    # Generar el código Graphviz para visualizar el grafo y la ruta más corta
    codigo = generarCodigoGraphviz(g, origen, destino, camino)
    print("Código Graphviz:")
    print(codigo)
"""