import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from PIL import Image, ImageTk

from .puzzle import (
    generate_scrambled_state,
    apply_move
)

from .solver import SEARCH_TYPES, solve


class PuzzleGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("15-PUZZLE")
        self.root.geometry("800x800")
        self.root.resizable(False, False)

        self.tile_size = 100
        self.board_size = 400

        self.initial_state = generate_scrambled_state(25)
        self.state = self.initial_state

        self.solution_path = []
        self.animation_index = 0

        self.image_tiles = {}

        self.tile_widgets = {}
        self.blank_widget = None

        self.animation_speed = 300

        self.slide_steps = 8

        self.solving = False

        self.create_widgets()
        self.load_image()
        self.update_board()

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="15-PUZZLE",
            font=("Arial", 24, "bold")
        )

        title.pack(pady=10)

        self.board = tk.Frame(
            self.root,
            width=self.board_size,
            height=self.board_size,
            bg="white",
            bd=2,
            relief="solid"
        )

        self.board.pack(pady=10)

        self.board.pack_propagate(False)

        controls = tk.Frame(self.root)
        controls.pack(pady=10)

        self.solve_button = tk.Button(
            controls,
            text="Solve",
            command=self.solve_puzzle
        )

        self.solve_button.grid(
            row=0,
            column=2,
            padx=5
        )

        self.new_button = tk.Button(
            controls,
            text="New Puzzle",
            command=self.new_puzzle
        )

        self.new_button.grid(
            row=0,
            column=3,
            padx=5
        )

        self.reset_button = tk.Button(
            controls,
            text="Reset Puzzle",
            command=self.reset_puzzle
        )

        self.reset_button.grid(
            row=0,
            column=4,
            padx=5
        )

        selectors = tk.Frame(self.root)
        selectors.pack(pady=5)

        tk.Label(
            selectors,
            text="Search type:"
        ).pack(
            side="left",
            padx=5
        )

        self.search_type = ttk.Combobox(
            selectors,
            values=list(SEARCH_TYPES),
            state="readonly",
            width=12
        )

        self.search_type.current(0)

        self.search_type.pack(
            side="left",
            padx=5
        )

        self.search_type.bind(
            "<<ComboboxSelected>>",
            self.update_algorithms
        )

        tk.Label(
            selectors,
            text="Algorithm:"
        ).pack(
            side="left",
            padx=5
        )

        self.algorithm = ttk.Combobox(
            selectors,
            state="readonly",
            width=10
        )

        self.algorithm.pack(
            side="left",
            padx=5
        )

        self.update_algorithms()

        speed_frame = tk.Frame(self.root)
        speed_frame.pack(pady=5)

        tk.Label(
            speed_frame,
            text="Animation Speed:"
        ).pack(
            side="left",
            padx=5
        )

        self.speed_scale = tk.Scale(
            speed_frame,
            from_=50,
            to=1000,
            orient="horizontal",
            length=250,
            resolution=50,
            command=self.update_speed
        )

        self.speed_scale.set(300)

        self.speed_scale.pack(
            side="left"
        )

        self.status = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 11)
        )

        self.status.pack(pady=5)

    def update_speed(self, value):

        self.animation_speed = int(
            float(value)
        )

    def update_algorithms(self, event=None):

        algorithms = SEARCH_TYPES[
            self.search_type.get()
        ]

        self.algorithm.config(
            values=algorithms
        )

        self.algorithm.set(
            algorithms[0]
        )

    def load_image(self):

        image_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "resources",
            "puzzle.jpg"
        )

        try:

            image = Image.open(
                image_path
            )

            image = image.resize(
                (
                    self.board_size,
                    self.board_size
                )
            )

            for number in range(1, 16):

                index = number - 1

                row = index // 4
                col = index % 4

                left = col * self.tile_size
                top = row * self.tile_size

                right = left + self.tile_size
                bottom = top + self.tile_size

                tile = image.crop(
                    (
                        left,
                        top,
                        right,
                        bottom
                    )
                )

                self.image_tiles[number] = ImageTk.PhotoImage(
                    tile
                )

        except Exception as e:

            messagebox.showerror(
                "Image Error",
                f"Could not load puzzle image:\n{e}"
            )

    def index_to_xy(self, index):

        row = index // 4
        col = index % 4

        return col * self.tile_size, row * self.tile_size

    def update_board(self):

        for widget in self.board.winfo_children():

            widget.destroy()

        self.tile_widgets = {}
        self.blank_widget = None

        for index, number in enumerate(self.state):

            x, y = self.index_to_xy(index)

            if number == 0:

                tile = tk.Frame(
                    self.board,
                    width=self.tile_size,
                    height=self.tile_size,
                    bg="white",
                    bd=1,
                    relief="solid"
                )

                tile.place(
                    x=x,
                    y=y,
                    width=self.tile_size,
                    height=self.tile_size
                )

                self.blank_widget = tile

            else:

                label = tk.Label(
                    self.board,
                    image=self.image_tiles[number],
                    bd=1,
                    relief="solid"
                )

                label.place(
                    x=x,
                    y=y,
                    width=self.tile_size,
                    height=self.tile_size
                )

                self.tile_widgets[number] = label

    def solve_puzzle(self):

        algorithm = self.algorithm.get()

        if not algorithm:

            messagebox.showwarning(
                "Warning",
                "Select an algorithm."
            )

            return

        if self.solving:

            return

        self.initial_state = self.state

        self.solution_path = []
        self.animation_index = 0

        self.solving = True

        self.solve_button.config(
            state="disabled"
        )

        self.new_button.config(
            state="disabled"
        )

        self.reset_button.config(
            state="disabled"
        )

        self.search_type.config(
            state="disabled"
        )

        self.algorithm.config(
            state="disabled"
        )

        self.speed_scale.config(
            state="disabled"
        )

        self.status.config(
            text=f"Solving with {algorithm}..."
        )

        thread = threading.Thread(
            target=self.run_solver,
            args=(algorithm,),
            daemon=True
        )

        thread.start()

    def run_solver(self, algorithm):

        try:

            result = solve(
                self.initial_state,
                algorithm
            )

            self.root.after(
                0,
                self.solver_finished,
                result
            )

        except Exception as e:

            self.root.after(
                0,
                self.solver_error,
                e
            )

    def solver_finished(self, result):

        self.solving = False

        if result["found"]:

            self.solution_path = result["path"]

            self.animation_index = 0

            self.status.config(
                text=(
                    f"{result['algorithm']} | "
                    f"Moves: {result['moves']} | "
                    f"Nodes: {result['nodes_expanded']} | "
                    f"Time: {result['time']:.4f}s"
                )
            )

            self.animate_solution()

        else:

            self.state = self.initial_state

            self.update_board()

            self.status.config(
                text=(
                    f"{result['algorithm']} did not find "
                    f"a solution. "
                    f"Nodes: {result['nodes_expanded']}"
                )
            )

            self.enable_controls()

    def solver_error(self, error):

        self.solving = False

        self.enable_controls()

        messagebox.showerror(
            "Solver Error",
            str(error)
        )

        self.status.config(
            text="Solver error."
        )

    def animate_solution(self):

        if self.animation_index >= len(
            self.solution_path
        ):

            self.solving = False

            self.enable_controls()

            self.status.config(
                text="Puzzle solved!"

            )

            return

        move = self.solution_path[
            self.animation_index
        ]

        self.animation_index += 1

        self.slide_tile(move, self.animate_solution)

    def slide_tile(self, move, on_complete):

        empty_index = self.state.index(0)

        if move == "UP":
            source_index = empty_index - 4
        elif move == "DOWN":
            source_index = empty_index + 4
        elif move == "LEFT":
            source_index = empty_index - 1
        else:
            source_index = empty_index + 1

        tile_number = self.state[source_index]
        widget = self.tile_widgets[tile_number]

        start_x, start_y = self.index_to_xy(source_index)
        end_x, end_y = self.index_to_xy(empty_index)

        self.blank_widget.place(
            x=start_x,
            y=start_y
        )

        widget.lift()

        step_delay = max(
            1,
            self.animation_speed // self.slide_steps
        )

        def step(count=0):

            if count >= self.slide_steps:

                self.state = apply_move(
                    self.state,
                    move
                )

                widget.place(
                    x=end_x,
                    y=end_y
                )

                on_complete()

                return

            progress = (count + 1) / self.slide_steps

            widget.place(
                x=int(start_x + (end_x - start_x) * progress),
                y=int(start_y + (end_y - start_y) * progress)
            )

            self.root.after(
                step_delay,
                step,
                count + 1
            )

        step()

    def reset_puzzle(self):

        if self.solving:

            return

        self.state = self.initial_state

        self.solution_path = []

        self.animation_index = 0

        self.update_board()

        self.status.config(
            text="Puzzle reset."
        )

    def new_puzzle(self):

        if self.solving:

            return

        self.initial_state = generate_scrambled_state(25)

        self.state = self.initial_state

        self.solution_path = []

        self.animation_index = 0

        self.update_board()

        self.status.config(
            text="New puzzle generated."
        )

    def enable_controls(self):

        self.solve_button.config(
            state="normal"
        )

        self.new_button.config(
            state="normal"
        )

        self.reset_button.config(
            state="normal"
        )

        self.search_type.config(
            state="readonly"
        )

        self.algorithm.config(
            state="readonly"
        )

        self.speed_scale.config(
            state="normal"
        )

    def run(self):

        self.root.mainloop()


def main():

    root = tk.Tk()

    app = PuzzleGUI(root)

    app.run()


if __name__ == "__main__":
    main()
