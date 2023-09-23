import csv  # Para trabajar con archivos CSV
from colorama import Fore, Style  # Para el formato de color en la terminal
import matplotlib.pyplot as plt  # Para visualizar el laberinto y las rutas

# Definir la clase MazeSolver para resolver el laberinto
class MazeSolver:
    def __init__(self):
        self.paths = []  # Lista para almacenar las rutas encontradas

    # Método para encontrar la entrada y salida del laberinto
    def find_start_end(self, maze):
        rows = len(maze)
        cols = len(maze[0])
        start = None
        end = None

        for x in range(cols):
            if maze[0][x] == 0:
                start = (x, 0)  # Encuentra la entrada en la primera fila
            if maze[rows - 1][x] == 0:
                end = (x, rows - 1)  # Encuentra la salida en la última fila

        for y in range(1, rows - 1):
            if maze[y][0] == 0:
                start = (0, y)  # Encuentra la entrada en la primera columna
            if maze[y][cols - 1] == 0:
                end = (cols - 1, y)  # Encuentra la salida en la última columna

        return start, end

    # Método recursivo para resolver el laberinto
    def solve(self, maze, startX, startY, endX, endY, path=[]):
        rows = len(maze)
        cols = len(maze[0])

        # Verificar si estamos fuera de los límites o en una celda bloqueada
        if (
            startX < 0 or startX >= cols or
            startY < 0 or startY >= rows or
            maze[startY][startX] == 1
        ):
            return

        path.append((startX, startY))  # Agregar la posición actual a la ruta

        if startX == endX and startY == endY:
            self.paths.append(list(path))  # Agregar la ruta encontrada a la lista de rutas
            path.pop()  # Eliminar la posición actual antes de retroceder
            return

        maze[startY][startX] = 1  # Marcar la celda como visitada

        # Explorar las cuatro direcciones posibles
        self.solve(maze, startX + 1, startY, endX, endY, path)
        self.solve(maze, startX - 1, startY, endX, endY, path)
        self.solve(maze, startX, startY + 1, endX, endY, path)
        self.solve(maze, startX, startY - 1, endX, endY, path)

        maze[startY][startX] = 0  # Desmarcar la celda antes de retroceder
        path.pop()  # Retroceder eliminando la posición actual

    # Método para mostrar el laberinto en color
    def display_maze(self, maze, path=[], show_crosses=False):
        cmap = plt.get_cmap('Blues')
        cmap.set_bad(color='red')
        plt.imshow(maze, cmap=cmap)  # Mostrar el laberinto con colores

        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if (x, y) in path and show_crosses:
                    plt.plot(x, y, marker='o', markersize=5, color='green')  # Marcar las rutas con círculos verdes

        plt.show()  # Mostrar el gráfico del laberinto

# Función para cargar el laberinto desde un archivo CSV
def cargar_laberinto(matriz):
    laberinto = []
    with open(matriz, 'r') as archivo:
        lector_csv = csv.reader(archivo)
        for fila in lector_csv:
            laberinto.append(list(map(int, fila)))  # Leer el laberinto desde el archivo CSV
    return laberinto

# Nombre del archivo CSV que contiene el laberinto
matriz = 'matriz.csv'
laberinto = cargar_laberinto(matriz)  # Cargar el laberinto desde el archivo CSV

solver = MazeSolver()  # Crear una instancia de MazeSolver
start, end = solver.find_start_end(laberinto)  # Encontrar la entrada y salida del laberinto
startX, startY = start  # Obtener las coordenadas de inicio
endX, endY = end  # Obtener las coordenadas de fin

# Mostrar el laberinto original en la terminal
print("Laberinto Original:")
for row in laberinto:
    print(' '.join(map(str, row)))

solver.display_maze(laberinto)  # Mostrar el laberinto original

solver.solve(laberinto, startX, startY, endX, endY)  # Resolver el laberinto

# Mostrar todas las rutas encontradas en color
for idx, path in enumerate(solver.paths):
    print(f'\nRuta {idx + 1}:')
    solver.display_maze(laberinto, path, show_crosses=True)  # Mostrar las rutas encontradas en verde