from PIL import Image, ImageDraw, ImageFont
import random

def generate_sudoku():
    grid = [[0] * 9 for _ in range(9)]

    def is_valid(num, row, col):
        for i in range(9):
            if grid[row][i] == num or grid[i][col] == num:
                return False

        start_row, start_col = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                if grid[i + start_row][j + start_col] == num:
                    return False
        return True

    def solve_sudoku():
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    for num in numbers:
                        if is_valid(num, row, col):
                            grid[row][col] = num
                            if solve_sudoku():
                                return True
                            grid[row][col] = 0
                    return False
        return True

    solve_sudoku()
    diff = input("Enter difficulty from 1 to 5: ")
    for row in range(9):
        for col in range(9):
            if random.random() < int(diff) * 0.2 - 0.1: 
                grid[row][col] = 0

    return grid

def create_sudoku_image(grid, filename="sudoku_grid.jpg"):
    # Create an image for the Sudoku grid
    cell_size = 50  # Size of each cell
    grid_size = cell_size * 9  # Size of the entire grid
    line_color = (0, 0, 0)  # Black grid lines
    bg_color = (255, 255, 255)  # White background

    # Create a new image with a white background
    img = Image.new("RGB", (grid_size, grid_size), bg_color)
    draw = ImageDraw.Draw(img)

    # Draw the grid lines
    for i in range(10):
        line_width = 3 if i % 3 == 0 else 1
        # Vertical lines
        draw.line([(i * cell_size, 0), (i * cell_size, grid_size)], fill=line_color, width=line_width)
        # Horizontal lines
        draw.line([(0, i * cell_size), (grid_size, i * cell_size)], fill=line_color, width=line_width)

    # Load a font
    try:
        font = ImageFont.truetype("arial.ttf", 35)
    except IOError:
        font = ImageFont.load_default()

    # Add the numbers to the grid at fixed positions
    for row in range(9):
        for col in range(9):
            if grid[row][col] != 0:
                num = str(grid[row][col])
                # Directly center the numbers in each cell
                x = col * cell_size + cell_size // 4
                y = row * cell_size + cell_size // 8
                draw.text((x, y), num, fill=line_color, font=font)

    # Save the image as a JPG file
    img.save(filename)
    print(f"Sudoku grid image saved as {filename}")

sudoku = generate_sudoku()

# Create and save the Sudoku image
create_sudoku_image(sudoku, "sudoku_grid.jpg")
