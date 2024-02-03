import random
from colorama import Fore, Back, Style
from colorama import init
from termcolor import colored
import numpy as np
from heapq import heappop, heappush

# ідея, стоврити агент їжї та тривалість життя для агентів
# якщо залишок життя < відстанні до виходу агент повинен знайти їжу та прямувати до неї

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

wall = colored('#', 'red')+ '|'
visited = colored('.', 'yellow')+ '|'
empty = colored(' ', 'black')+ '|'
agent = colored('a', 'blue')+ '|'
exit = colored('►', 'green')+ '|'
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_wall = False
        self.is_visited = False
        self.is_exit = False
        self.is_occupied = False
    
    def __lt__(self, other):
        # For A* algorithm
        return False

class AgentSearcher:
    def __init__(self, id, start_x, start_y):
        self.id = id
        self.x = start_x
        self.y = start_y
        self.move_history = []
        self.path = []
    
    def move(self, coordinates):
        x, y = coordinates
        self.move_history.append((self.x, self.y))
        self.x = x
        self.y = y


class MultiAgentSystem:
    def __init__(self, width, height, num_agents):
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
        self.set_walls()
        self.exit_x, self.exit_y = self.set_exit()
        self.agents = self.init_agents(num_agents)
        
    def set_walls(self):
        num_walls = int(0.33 * self.height * self.width)
        for _ in range(num_walls):
            wall_row, wall_col = np.random.randint(self.height), np.random.randint(self.width)
            self.grid[wall_row][wall_col].is_wall = True

    def set_exit(self):
        exit_side = np.random.choice(['top', 'bottom', 'left', 'right'])
        exit_x = None
        exit_y = None
        if exit_side == 'top':
            exit_x = 0
            exit_y = np.random.randint(width)
        elif exit_side == 'bottom':
            exit_x = height - 1
            exit_y = np.random.randint(width)
        elif exit_side == 'left':
            exit_x = np.random.randint(height)
            exit_y = 0
        else:  # exit_side == 'right'
            exit_x = np.random.randint(height)
            exit_y = width - 1
        self.grid[exit_x][exit_y].is_exit = True
        self.grid[exit_x][exit_y].is_wall = False
        return exit_x, exit_y

    def init_agents(self, num_agents):
        agents = []
        vacant_cells = [cell for cell in np.reshape(self.grid, self.width*self.height) if  not cell.is_exit and not cell.is_wall]

        for i in range(num_agents):
            cell = random.choice(vacant_cells)
            cell.is_occupied = True
            agent = AgentSearcher(f"{i}", cell.x, cell.y)
            agents.append(agent)
            vacant_cells.remove(cell)
        return agents

    def print_grid(self):
        for i in range(self.height):
            for j in range (self.width):
                cell = self.grid[i][j]
                if cell.is_wall:
                    print(wall,end='')
                elif cell.is_exit:
                    print(exit,end='')
                elif cell.is_occupied:
                    print(agent,end='')
                elif cell.is_visited:
                    print(visited,end='')
                else:
                    print(empty,end='')
            print()
    # def print_grid(self):
    #     for i in range(self.height):
    #         for j in range (self.width):
    #             cell = self.grid[i][j]
    #             if cell.is_wall:
    #                 print('W',end='')
    #             if cell.is_exit:
    #                 print("E",end='')
    #             if cell.is_occupied:
    #                 print("A",end='')
    #             if cell.is_visited:
    #                 print("V",end='')
    #             if not cell.is_exit and not cell.is_occupied and not cell.is_visited and not cell.is_wall:
    #                 print(" ",end='')
    #             print("|\t", end="")
    #         print()
    
    def get_neighbors(self, x, y):
        neighbors = []
        if x > 0 and not self.grid[x - 1][y].is_wall and not self.grid[x - 1][y].is_occupied:
            neighbors.append((x - 1, y))
        if x < self.width - 1 and not self.grid[x + 1][y].is_wall and not self.grid[x + 1][y].is_occupied:
            neighbors.append((x + 1, y))
        if y > 0 and not self.grid[x][y - 1].is_wall and not self.grid[x][y - 1].is_occupied:
            neighbors.append((x, y - 1))
        if y < self.height - 1 and not self.grid[x][y + 1].is_wall and not self.grid[x][y + 1].is_occupied:
            neighbors.append((x, y + 1))
        return neighbors

    def heuristic(self, x, y):
        return abs(x - self.exit_x) + abs(y - self.exit_y)

    def a_star(self, start_x, start_y, goal_x, goal_y):
        frontier = [(0, (start_x, start_y))]
        came_from = {(start_x, start_y): None}
        cost_so_far = {(start_x, start_y): 0}

        while frontier:
            current_cost, current = heappop(frontier)

            if current == (goal_x, goal_y):
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            for next_x, next_y in self.get_neighbors(*current):
                new_cost = cost_so_far[current] + 1
                if (next_x, next_y) not in cost_so_far or new_cost < cost_so_far[(next_x, next_y)]:
                    cost_so_far[(next_x, next_y)] = new_cost
                    priority = new_cost + self.heuristic(next_x, next_y)
                    heappush(frontier, (priority, (next_x, next_y)))
                    came_from[(next_x, next_y)] = current

        return None

    def run_simulation(self, max_steps):
        for step in range(max_steps):
            agents_at_exit = [agent for agent in self.agents if (agent.x, agent.y) == (self.exit_x, self.exit_y)]
            agents_with_paths = [agent for agent in self.agents if agent.path]

            if step > 0 and len(agents_with_paths) == 0:
                print("All agents that could reach the exit have reached. Simulation complete.")
                break

            for agent in self.agents:
                new_path = self.a_star(agent.x, agent.y, self.exit_x, self.exit_y)
                if new_path != None:
                    new_path.pop(0)
                    agent.path = new_path

                if agent.path:
                    next_x, next_y = agent.path.pop(0)
                    current_cell = self.grid[agent.x][agent.y]
                    current_cell.is_visited = True
                    current_cell.is_occupied = False
                    agent.move((next_x, next_y))
                    new_cell = self.grid[agent.x][agent.y]
                    new_cell.is_occupied = True
                    new_cell.is_visited = True

            self.print_grid()
            input("Show next step")





if __name__ == "__main__":
    width = 20
    height = 20
    num_agents = 10
    max_steps = 50

    multi_agent_system = MultiAgentSystem(width, height, num_agents)
    #multi_agent_system.print_grid()
    multi_agent_system.run_simulation(max_steps)