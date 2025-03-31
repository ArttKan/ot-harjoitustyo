import tkinter as tk
from tkinter import messagebox
from entities.event import Event
from services.score_service import ScoreService

Scorekeeper = ScoreService()


def handle_add_event():
    event_type = event_type_entry.get()
    event_content = event_content_entry.get()

    if not event_type or not event_content:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        event_content = int(event_content)  # Convert score to integer
    except ValueError:
        messagebox.showerror("Error", "Score must be a number.")
        return

    Scorekeeper.add_event(event_type, event_content)
    messagebox.showinfo("Success", f"Event '{event_type}' added successfully!")
    event_type_entry.delete(0, tk.END)
    event_content_entry.delete(0, tk.END)

    update_event_list()


def update_event_list():
    event_listbox.delete(0, tk.END)  # Clear the Listbox
    events = Scorekeeper.get_events()  # Retrieve the list of events
    for event in events:
        event_listbox.insert(tk.END, f"{event.type} - Score: {event.content}")


root = tk.Tk()
root.title("Scorekeeper")


tk.Label(root, text="Event Type:").grid(row=0, column=0, padx=10, pady=10)
event_type_entry = tk.Entry(root)
event_type_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Event content:").grid(row=1, column=0, padx=10, pady=10)
event_content_entry = tk.Entry(root)
event_content_entry.grid(row=1, column=1, padx=10, pady=10)

add_event_button = tk.Button(root, text="Add Event", command=handle_add_event)
add_event_button.grid(row=2, column=0, columnspan=2, pady=20)

tk.Label(root, text="Added Events:").grid(
    row=3, column=0, columnspan=2, pady=10)
event_listbox = tk.Listbox(root, width=40, height=10)
event_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

update_event_list()

root.mainloop()
