import time

def print_at_coords(x, y, char):
    """Prints a character at the specified (x, y) coordinates."""
    # ANSI escape code to move cursor: \033[<Y>;<X>H
    # Y is row, X is column. Terminals are typically 1-indexed.
    # So, add 1 to x and y for common 0-indexed programming coordinates.
    print(f"\033[{y + 1};{x + 1}H{char}", end="")

def clear_screen():
    """Clears the entire terminal screen."""
    print("\033[2J", end="") # Clear screen

def hide_cursor():
    """Hides the terminal cursor."""
    print("\033[?25l", end="")

def show_cursor():
    """Shows the terminal cursor."""
    print("\033[?25h", end="")

# Your dictionary of Unicode characters and their coordinates
char_data = {
    "smile": {"char": "😊", "x": 10, "y": 5},
    "star": {"char": "⭐", "x": 20, "y": 8},
    "heart": {"char": "❤️", "x": 5, "y": 12},
    "snowflake": {"char": "❄️", "x": 30, "y": 3},
    "tree": {"char": "🌳", "x": 15, "y": 10}
}

if __name__ == "__main__":
    clear_screen()
    hide_cursor()

    try:
        for key, data in char_data.items():
            print_at_coords(data["x"], data["y"], data["char"])
            # You might want a small delay to see each character appear
            # time.sleep(0.1)

        # Move cursor to the bottom left after printing everything
        print_at_coords(0, 20, "") # Move cursor to a clean line

        input("Press Enter to clear screen and exit...")

    finally:
        clear_screen()
        show_cursor()