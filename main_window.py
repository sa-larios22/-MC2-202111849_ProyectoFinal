import tkinter as tk
from tkinter import messagebox
from main import Grafo, dijkstra, generarCodigoGraphviz

class GraphApp:
    def __init__(self, master):
        self.master = master
        master.configure(bg="light blue")

        # Botón para limpiar el canvas
        self.clear_button = tk.Button(master, text="Limpiar", command=self.clear_canvas)
        self.clear_button.pack(side=tk.TOP)

        # Botón de cómo se usa
        self.how_to_button = tk.Button(master, text="¿Cómo se usa?", command=self.how_to)
        self.how_to_button.pack(side=tk.TOP)

        # Botón información
        self.info_button = tk.Button(master, text="Información", command=self.info)
        self.info_button.pack(side=tk.TOP)

        # Canvas para dibujar el grafo
        self.canvas = tk.Canvas(master, width=500, height=500, bg="white", border=2, relief=tk.SUNKEN)
        self.canvas.pack()

        # Diccionario de vértices
        self.vertices = {}
        self.graph = {}
        self.edges = []

        # Entrada para el vértice a agregar
        self.label = tk.Label(master, text="Vértice:", background="light blue").pack(side=tk.LEFT)
        self.vertex_entry = tk.Entry(master)
        self.vertex_entry.pack(side=tk.LEFT)

        # Campos de entrada para los vértices de inicio y final
        self.label1 = tk.Label(master, text="Vértice de Inicio", background="light blue").pack(side=tk.LEFT)
        self.start_vertex_entry = tk.Entry(master)
        self.start_vertex_entry.pack(side=tk.LEFT)

        self.label2 = tk.Label(master, text="Vértice Final", background="light blue").pack(side=tk.LEFT)
        self.end_vertex_entry = tk.Entry(master)
        self.end_vertex_entry.pack(side=tk.LEFT)

        # Bindear click izquierdo para agregar vértices
        self.canvas.bind("<Button-1>", self.add_vertex)

        # Bindear click derecho para conectar vértices
        self.canvas.bind("<Button-3>", self.connect_vertices)

        self.selected_vertex = None

        # Botón para encontrar el camino más corto y generar el código Graphviz
        self.find_path_button = tk.Button(master, text="Encontrar camino más corto", command=self.find_shortest_path)
        self.find_path_button.pack(side=tk.RIGHT)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.vertices = {}
        self.graph = {}
        self.edges = []

    def how_to(self):
        tk.messagebox.showinfo("¿Cómo se usa?", """1. Agregue el nombre del vértice en el primer cuadro de texto
2. Seleccione en cualquier área del canvas para agregar el vértice
3. Haga click derecho en el canvas para conectar dos vértices.
4. Ingrese el vértice de inicio y final.
5. Haga click en el botón Encontrar camino más corto
6. Se mostrará una ventana de información que contiene la ruta más corta
7. Se generará un código Graphviz en el que se visualiza y resalta la ruta más corta""")

    def info(self):
        tk.messagebox.showinfo("Información", """Sergio Andrés Larios Fajardo
Carné: 202111849
Matemática para Computación 2
Sección: N""")

    def find_shortest_path(self):
        start_vertex = self.start_vertex_entry.get()
        end_vertex = self.end_vertex_entry.get()

        if start_vertex == "" or end_vertex == "":
            tk.messagebox.showerror("Error", "Ingrese un vértice de inicio y final.")
            return

        if start_vertex and end_vertex and start_vertex in self.graph and end_vertex in self.graph:
            try:
                # Create a Grafo instance with the current graph
                grafo = Grafo(self.graph)

                # Run the dijkstra function to find the shortest path
                path_length, shortest_path = dijkstra(grafo, start_vertex, end_vertex)

                # Mensaje de la ruta más corta
                tk.messagebox.showinfo("Ruta más corta", f"La ruta más corta desde {start_vertex} hasta {end_vertex} es:\n{shortest_path}\nLongitud de la ruta: {path_length}")
            
                # Generar código Graphviz
                code_graphviz = generarCodigoGraphviz(grafo, start_vertex, end_vertex, shortest_path)
                #print(code_graphviz)
                try:
                    filepath = "graphviz\grafo.dot"
                    file = open(filepath, "w")
                    file.write(code_graphviz)
                    file.close()
                    tk.messagebox.showinfo("Archivo generado", f"El archivo .dot se ha generado correctamente en la ruta {filepath}")
                except Exception as e:
                    tk.messagebox.showerror("Error", "Error al generar el archivo .dot\n" + str(e))
            except Exception as e:
                tk.messagebox.showerror("Error", "Error al determinar el camino\n" + str(e))
        else:
            tk.messagebox.showerror("Error", "Ingrese un vértice de inicio y final.")

    def add_vertex(self, event):
        x, y = event.x, event.y
        vertex_name = self.vertex_entry.get()
        if vertex_name == "":
            tk.messagebox.showerror("Error", "Por favor, ingrese un nombre de vértice.")
            return

        if vertex_name not in self.graph:
            try:
                vertex_id = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue")
                self.vertices[vertex_id] = (x, y)
                self.graph[vertex_name] = {}
                self.vertex_entry.delete(0, tk.END)
            except Exception as e:
                tk.messagebox.showerror("Error al agregar el vértice", e)
        else:
            tk.messagebox.showinfo("Error", "El nombre del vértice ya está en uso \nPor favor, elija otro nombre.")

    def connect_vertices(self, event):
        x, y = event.x, event.y
        clicked_vertex = self.find_closest_vertex(x, y)

        if clicked_vertex is not None:
            if self.selected_vertex is None:
                self.selected_vertex = clicked_vertex
                self.canvas.itemconfig(clicked_vertex, fill="red")
            else:
                if clicked_vertex != self.selected_vertex:
                    self.edges.append((self.selected_vertex, clicked_vertex))
                    x1, y1 = self.vertices[self.selected_vertex]
                    x2, y2 = self.vertices[clicked_vertex]
                    self.canvas.create_line(x1, y1, x2, y2)

                    start_vertex = list(self.graph.keys())[list(self.vertices.keys()).index(self.selected_vertex)]
                    end_vertex = list(self.graph.keys())[list(self.vertices.keys()).index(clicked_vertex)]

                    self.graph[start_vertex][end_vertex] = 0  # Replace 0 with the desired edge weight

                self.canvas.itemconfig(self.selected_vertex, fill="blue")
                self.selected_vertex = None

    def find_closest_vertex(self, x, y):
        closest_vertex = None
        min_distance = float("inf")

        for vertex_id, coords in self.vertices.items():
            vx, vy = coords
            distance = ((x - vx) ** 2 + (y - vy) ** 2) ** 0.5

            if distance < 10 and distance < min_distance:
                closest_vertex = vertex_id
                min_distance = distance

        return closest_vertex

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Proyecto MC2 - Grafos - Sergio Larios")
    app = GraphApp(root)
    root.mainloop()