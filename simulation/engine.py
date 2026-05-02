import numpy as np

class ForestFireEngine:
    EMPTY, TREE, FIRE = 0, 1, 2

    def __init__(self, size, p, f, grid=None):
        self.size = size
        self.p = p
        self.f = f
        self.grid = np.array(grid) if grid is not None else np.zeros((size, size), dtype=int)

    def step(self):
        new_grid = self.grid.copy()
        fire_sizes = []
        
        # Primero identificamos los incendios actuales antes de que se apaguen
        # Esto nos permite medir su tamaño
        current_fire_clusters = self._get_fire_clusters()
        
        for r in range(self.size):
            for c in range(self.size):
                state = self.grid[r, c]
                if state == self.EMPTY:
                    if np.random.random() < self.p:
                        new_grid[r, c] = self.TREE
                elif state == self.TREE:
                    # Regla: vecino en llamas o rayo
                    neighbors = self.grid[max(0,r-1):r+2, max(0,c-1):c+2]
                    if self.FIRE in neighbors or np.random.random() < self.f:
                        new_grid[r, c] = self.FIRE
                elif state == self.FIRE:
                    new_grid[r, c] = self.EMPTY
        
        self.grid = new_grid
        return self.grid.tolist(), current_fire_clusters

    def _get_fire_clusters(self):
        """
        Detecta grupos de celdas en llamas conectadas para calcular tamaños.
        """
        visited = np.zeros((self.size, self.size), dtype=bool)
        sizes = []
        
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r, c] == self.FIRE and not visited[r, c]:
                    # Iniciar búsqueda de un nuevo incendio (clúster)
                    size = 0
                    stack = [(r, c)]
                    visited[r, c] = True
                    while stack:
                        curr_r, curr_c = stack.pop()
                        size += 1
                        # Revisar vecinos 4-conectados (N, S, E, O)
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nr, nc = curr_r + dr, curr_c + dc
                            if 0 <= nr < self.size and 0 <= nc < self.size:
                                if self.grid[nr, nc] == self.FIRE and not visited[nr, nc]:
                                    visited[nr, nc] = True
                                    stack.append((nr, nc))
                    sizes.append(size)
        return sizes