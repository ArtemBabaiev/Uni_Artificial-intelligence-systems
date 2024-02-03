import random
from termcolor import colored
import numpy as np
from heapq import heappop, heappush

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

wall = colored('#', 'red')+ '|'
visited = colored('.', 'yellow')+ '|'
empty = colored(' ', 'black')+ '|'
agent = colored('a', 'blue')+ '|'
dead = colored('x', 'black')+ '|'
exit = colored('►', 'green')+ '|'
fruit = colored('f', 'magenta')+ '|'

class AgentSearcher:
    def __init__(self, id, start_x, start_y):
        self.health = 10
        self.id = id
        self.x = start_x
        self.y = start_y
        self.path = []

class Fruit:
    def __init__(self, x, y) -> None:
        self.extra_health = 10
        self.x = x
        self.y = y

class Wall:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

class Exit:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.content :AgentSearcher | Fruit | Wall | Exit = None
        self.is_visited = False

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
            self.grid[wall_row][wall_col].content = Wall(wall_row, wall_col)

    def set_exit(self):
        exit_side = np.random.choice(['top', 'bottom', 'left', 'right'])
        exit_x = None
        exit_y = None
        if exit_side == 'top':
            exit_x = 0
            exit_y = np.random.randint(self.width)
        elif exit_side == 'bottom':
            exit_x = self.height - 1
            exit_y = np.random.randint(self.width)
        elif exit_side == 'left':
            exit_x = np.random.randint(self.height)
            exit_y = 0
        else:  # exit_side == 'right'
            exit_x = np.random.randint(self.height)
            exit_y = self.width - 1
        self.grid[exit_x][exit_y].content = Exit(exit_x, exit_y)
        return exit_x, exit_y
    
    def place_fruits(self, num_fruits):
        vacant_cells = [cell for row in self.grid for cell in row if cell.content is None]
        num_fruits = min(num_fruits, len(vacant_cells))

        for _ in range(num_fruits):
            cell = random.choice(vacant_cells)
            cell.content = Fruit(cell.x, cell.y)
            vacant_cells.remove(cell)

    def init_agents(self, num_agents):
        agents = []
        vacant_cells = [cell for cell in np.reshape(self.grid, self.width*self.height) if cell.content == None]

        for i in range(num_agents):
            cell = random.choice(vacant_cells)
            cell.is_visited = True
            agent = AgentSearcher(f"{i}", cell.x, cell.y)
            cell.content = agent
            agents.append(agent)
            vacant_cells.remove(cell)
        return agents
    
    def print_grid(self):
        for i in range(self.height):
            for j in range (self.width):
                cell = self.grid[i][j]
                if type(cell.content) is Wall:
                    print(wall,end='')
                elif type(cell.content) is Exit:
                    print(exit,end='')
                elif type(cell.content) is AgentSearcher and cell.content.health == 0:
                    print(dead,end='')
                elif type(cell.content) is AgentSearcher:
                    print(agent,end='')
                elif type(cell.content) is Fruit:
                    print(fruit,end='')
                elif cell.is_visited:
                    print(visited,end='')
                else:
                    print(empty,end='')
            print()
    
    def move_agent(self, agent, new_x, new_y):
        
        current_cell = self.grid[agent.x][agent.y]
        new_cell = self.grid[new_x][new_y]

        if type(new_cell.content) is Fruit:
            print(f"Agent {agent.id} got extra health")
            agent.health += new_cell.content.extra_health

        current_cell.content = None
        if type(new_cell.content) is not Exit:
            new_cell.content = agent

        agent.x = new_x
        agent.y = new_y
        new_cell.is_visited = True

    
    def run_simulation(self, max_steps):
        for step in range(max_steps):
            print(f"Step {step + 1}:")
            self.print_grid()

            input("Show next step")

            if step > 1:
                agents_with_paths = [agent for agent in self.agents if agent.path]
                agents_alive = [agent for agent in self.agents if agent.health > 0]
                if len(agents_with_paths) == 0 or len(agents_alive) == 0:
                    print("All agents that could reach the exit have reached. Simulation complete.")
                    break

            for agent in self.agents:
                if agent.health <= 0:
                    continue
                
                exit_reached, path = self.find_path(agent, target_exit=True)
                if path != None and len(path) > 0:
                    path.pop(0)
                agent.path = path

                if agent.health < len(path):
                    print(f"Agent {agent.id} doesnt have enough health to reach exit", end ='')
                    fruit_found, path_to_fruit = self.find_path(agent, target_exit=False)
                    if fruit_found:
                        print(f"| path to fruit found")
                        if path_to_fruit != None and len(path_to_fruit) > 0:
                            path_to_fruit.pop(0)
                        agent.path = path_to_fruit
                    else:
                        print(f"| path to fruit not found")

                agent.health -= 1  
                if agent.path != None and len(agent.path) > 0:
                    next_x, next_y = agent.path.pop(0)
                    self.move_agent(agent, next_x, next_y)

        print("Simulation ended.")


    def find_path(self, agent, target_exit=True):
        start_x, start_y = agent.x, agent.y
        target_x, target_y = (self.exit_x, self.exit_y) if target_exit else self.find_nearest_fruit(agent)

        open_set = [(0, (start_x, start_y))]
        came_from = {}

        g_score = {cell: float('inf') for row in self.grid for cell in row}
        g_score[(start_x, start_y)] = 0

        f_score = {cell: float('inf') for row in self.grid for cell in row}
        f_score[(start_x, start_y)] = self.heuristic(start_x, start_y, target_x, target_y)

        while open_set:
            current = min(open_set, key=lambda x: f_score[x[1]])
            current_x, current_y = current[1]

            if current_x == target_x and current_y == target_y:
                # Reconstruct the path
                path = [(target_x, target_y)]
                while (current_x, current_y) in came_from:
                    current_x, current_y = came_from[(current_x, current_y)]
                    path.append((current_x, current_y))
                path.reverse()
                return True, path

            open_set.remove(current)

            for neighbor_x, neighbor_y in self.get_neighbors(current_x, current_y):
                if (neighbor_x, neighbor_y) not in g_score:
                    g_score[(neighbor_x, neighbor_y)] = float('inf')

                tentative_g_score = g_score[(current_x, current_y)] + 1

                if tentative_g_score < g_score[(neighbor_x, neighbor_y)]:
                    came_from[(neighbor_x, neighbor_y)] = (current_x, current_y)
                    g_score[(neighbor_x, neighbor_y)] = tentative_g_score
                    f_score[(neighbor_x, neighbor_y)] = tentative_g_score + self.heuristic(
                        neighbor_x, neighbor_y, target_x, target_y
                    )

                    if (neighbor_x, neighbor_y) not in open_set:
                        open_set.append((f_score[(neighbor_x, neighbor_y)], (neighbor_x, neighbor_y)))

        return False, []

    def heuristic(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def get_neighbors(self, x, y):
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.height and 0 <= new_y < self.width and not isinstance(
                self.grid[new_x][new_y].content, Wall
            ):
                neighbors.append((new_x, new_y))
        return neighbors

    def find_nearest_fruit(self, agent):
        for row in self.grid:
            for cell in row:
                if isinstance(cell.content, Fruit):
                    return cell.x, cell.y
        return agent.x, agent.y 




if __name__ == "__main__":
    width = 20
    height = 20
    num_agents = 10
    max_steps = 50
    num_fruits = 15

    multi_agent_system = MultiAgentSystem(width, height, num_agents)
    multi_agent_system.place_fruits(num_fruits)
    multi_agent_system.run_simulation(max_steps)