from tkinter import Tk
from initialize_database import initialize_database
from ui.ui import UI


def main():
    initialize_database()
    window = Tk()
    window.title("Scorekeeper")

    ui = UI(window)
    ui.start()

    window.mainloop()


if __name__ == "__main__":
    main()
