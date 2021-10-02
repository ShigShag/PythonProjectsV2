from sys import argv, exit
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def create_random_grid(size):
    return np.random.choice([1, 0], pow(size, 2), p=[0.2, 0.8]).reshape(size, size)

def refresh(frame_data, grid, image, size):
    # Copy grid to prevent collisions while changing values
    copy_grid = grid.copy()

    # Loop every row and entry
    for y in range(0, size):
        for x in range(0, size):
            # Calculate sum of adjacent cells
            sum = (grid[y, (x - 1) % size] + grid[y, (x + 1) % size] # left and right cells
                  + grid[(y - 1) % size, (x - 1) % size] + grid[(y - 1) % size, x] + grid[(y - 1) % size, (x + 1) % size] # top cells
                  + grid[(y + 1) % size, (x - 1) % size] + grid[(y + 1) % size, x] + grid[(y + 1) % size, (x + 1) % size]) # bottom cells

            if grid[y, x] == 0 and sum == 3:
                copy_grid[y, x] = 1
                continue

            if grid[y, x] == 1:
                if sum <= 1 or sum >= 4:
                    copy_grid[y, x] = 0

    # set image
    image.set_data(copy_grid)

    # update main grid
    grid[:] = copy_grid[:]

    return image

def main():
    n = 100

    if len(argv) >= 2:
        n = int(argv[1])

    if len(argv) == 3:
        interval = int(argv[2])



    grid = create_random_grid(n)
    fig, axs = plt.subplots()
    image = axs.imshow(grid)

    vid = animation.FuncAnimation(fig, refresh, fargs=(grid, image, n), frames=10, interval=interval, save_count=50)

    plt.show()

if __name__ == '__main__':
    exit(main())