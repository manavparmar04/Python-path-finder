import pygame
import math 
from queue import PriorityQueue


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH)) # Setting the dimensions of the window 800x800
pygame.display.set_caption("Path finding algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


ALGORITHM_MODE = "A*"  # Can be "A*" or "DIJKSTRA"

'''
The purpose of using classes in this way is because each node/ spot has its own data + behavior,
without the use of a class we would need seperate arrays and functions for checking and changes. 
It also makes it easier to read. 

row, colm width, total_rows are to be permanently rememebered, x, y , color and neighbor are internal attributes 

H : Estimated distance from node n to the end node
G : Current shortest distance to get from start node to next/ current node
F : The addition of H + G


Controls:
- Left click to add start, end , barriers
- Right click to erase nodes
- C to clear
- D to change algorithms
- Space to start either algorithm

'''


class Spot: # Creating the visuals
    def __init__(self, row, col, width, total_rows):
        self.row = row   # row and col stores the Spots grid position 
        self.col = col   # ^
        self.width = width  # Saves the cell size so the spot knows how big it should be
        self.total_rows = total_rows # stores grid size so can be used to check boundaries
        self.x = row * width   # Converts grid coordinates to pixel coordinates 
        self.y = col * width   # ^
        self.color = WHITE  # Starting colour but also represents empty / unvisited
        self.neighbors = []  # used to store neighboring nodes used by A*
        

    # Methods below return t or f depending on the role of the spot
    def get_pos (self):
        return self.row, self.col
    
    def is_closed(self) : 
        return self.color == RED
    

    def is_open(self) :
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = WHITE
    
    # Setting the color of the spot based on the role

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK
    
    def make_start(self):
        self.color = ORANGE
    
    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self,win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


    def update_neighbors(self,grid):
        self.neighbors = []
        if self.row < self.total_rows -1 and not grid[self.row+1][self.col].is_barrier(): # Checking DOWN
            self.neighbors.append(grid[self.row+1][self.col])
        #self.row < self.total_rows-1 checks if we can go down, and will add bottom neighbor to list if it is not barrier 

        if self.row > 0 and not grid[self.row -1][self.col].is_barrier(): # checking UP
            self.neighbors.append(grid[self.row -1][self.col])
        #  self.row > 0 - making sure that row is not at row 0, and up spot is not a barrier, otherwise add top spot to list

        if self.col > 0 and not grid[self.row][self.col-1].is_barrier(): # checking LEFT
            self.neighbors.append(grid[self.row][self.col-1])            
        # self.col > 0 - making sure that value is not first in row, and is not barrier, otherwise add left spot to list

        if self.col < self.total_rows -1 and not grid[self.row][self.col +1].is_barrier(): # checking RIGHT
            self.neighbors.append(grid[self.row][self.col+1])
        # self.col < self.total_rows -1 - making sure col is not last value in row and is not a barrier, otherewise add right spot to the list

    
    
    def __lt__(self, other): # will be used to compare two spots togther 
        return False
    
#---------------------------------------------------------------------------------------------------------------------------------------------

def h(p1, p2): # heuristic function with point 1 and point 2
    x1, y1 = p1
    x2, y2 = p2

    return abs(x2-x1) + abs(y2-y1)

def path(came_from, current, draw): # current node starts at the end node and traveres back to the starting node - as long as node as a parent, we keep traversing back
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()



def a_star(draw, grid, start, end): 
    count = 0 # count is used as a tie breaker in case F score is the same
    open_set = PriorityQueue() # using heap to get minimum element in the queue
    open_set.put((0, count, start))  # 0 is current f score 
    came_from = {}  # keeping track of what spots we came from 
    g_score = {spot: float("inf") for row in grid for spot in row} # setting all f and g score inital value to infinity
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos()) # want to estimate the distance between start and end spot

    open_set_hash = {start} # used to keep track all the items in the priority queue and aren't in the priority queue

    while not open_set.empty(): # Keep lopping as long as there are still nodes to process
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2] # retreiving just the node (removing it from priority queue)
        open_set_hash.remove(current) # syncing with priority queue

        if current == end:
            path(came_from, current, draw)
            end.make_end()
            start.make_start()
            return True


        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 # Assuming all values of the edge are 1, whatever value of our current node is + 1 to move onto the next node.. eg start is 0, moving to next node would be 1.

            if temp_g_score < g_score[neighbor]: # if temp G score is less than current G score of neighbor, update it and store the value
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash: # checking to see if neighbor is in priority queue through hash
                    count += 1 # Increment count of number of values inside the hash
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open() # putting it into open set 
        draw()

        if current != start: # if the node we just considered is not the start node, make it red and close it off since it won't be added to open set again
            current.make_closed()

# it knows roughly which direction the goal is, so it explores fewer nodes
    return False # in case we do not find a path



def dijkstra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    distance = {spot: float("inf") for row in grid for spot in row}
    distance[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path(came_from, current, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_distance = distance[current] + 1

            if temp_distance < distance[neighbor]:
                came_from[neighbor] = current
                distance[neighbor] = temp_distance # uses just distance (which is equivalent to g_score) - it prioritizes nodes based ONLY on the actual distance traveled from the start
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((distance[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()
    # Dijkstra is "uninformed" - it explores equally in all directions like a spreading wave
    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows  # cell size 
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i,j,gap,rows)
            grid[i].append(spot)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) # drawing the grid lines, top to bottom
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), ( j * gap, width)) # drawing the vertical lines


def draw(win, grid, rows, width, algorithm_mode):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)

    # Draw algorithm mode text
    pygame.init()
    font = pygame.font.Font(None, 36)
    text = font.render(f"Algorithm: {algorithm_mode}", True, BLACK)
    text_rect = text.get_rect(center=(width // 2, 20))
    
    # Draw background for text
    bg_rect = text_rect.inflate(20, 10)
    pygame.draw.rect(win, WHITE, bg_rect)
    pygame.draw.rect(win, BLACK, bg_rect, 2)
    
    win.blit(text, text_rect)
    

    pygame.display.update() # take whatever we have drawn and update that on our display






def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col 

def print_grid(grid):
    for row in grid:
        for spot in row:
            if spot.is_start():
                print("S", end=" ")
            elif spot.is_end():
                print("E", end=" ")
            elif spot.is_barrier():
                print("#", end=" ")
            else:
                print(".", end=" ")
        print()




def main(win, width):
    global ALGORITHM_MODE
    ROWS = 50
    grid = make_grid(ROWS, width) # width value is set above
    
    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width, ALGORITHM_MODE)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue  # once we start, we dont want to add or change anything while the algorithm is running
            
            if pygame.mouse.get_pressed()[0]:  # checking if left mouse button was pressed
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width) # getting us the specific spot that was clicked on 
                spot = grid[row][col]

                if not start and spot != end :
                    start = spot
                    start.make_start()
                
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                
                elif spot != end and spot != start: # making sure we dont place over start and end 
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[1]:
                print_grid(grid)

            
            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width) # getting us the specific spot that was clicked on 
                spot = grid[row][col]
                spot.reset()

                if spot == start:   # resetting values, it will create another start/end spot through if conditions above
                    start = None
                elif spot == end:
                    end = None


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:   # where we run the algorithm 
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    if ALGORITHM_MODE == "A*":
                        a_star(lambda: draw(win, grid, ROWS, width, ALGORITHM_MODE), grid, start, end)
                    else:
                        dijkstra(lambda: draw(win, grid, ROWS, width, ALGORITHM_MODE), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_d:
                    if ALGORITHM_MODE == "A*":
                        ALGORITHM_MODE = "DIJKSTRA"
                    else:
                        ALGORITHM_MODE = "A*"

    
    pygame.quit()

main(WIN, WIDTH)

