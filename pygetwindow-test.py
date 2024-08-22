import pygetwindow as gw
import time
import sys
import threading
from screeninfo import get_monitors
from shapely.geometry import box
from shapely.ops import unary_union

# TODO: some background windows may have extreme bounds like (-32000, -32000) that are not actually on screen

# Calculate the displayed part of a window
def get_displayed_bounds(window, existing_regions):
    # Get the window bounds as a shapely box
    window_box = box(window.left, window.top, window.right, window.bottom)

    # Subtract overlapping regions
    visible_region = window_box
    for region in existing_regions:
        visible_region = visible_region.difference(region)
    
    return visible_region

def start_monitoring(interval, iterations):
    total_time = 0
    total_windows = 0

    for i in range(iterations):
        start_time = time.time()
        all_windows = gw.getAllWindows()
        end_time = time.time()

        elapsed_time = end_time - start_time
        total_time += elapsed_time
        total_windows += len(all_windows)

        displayed_windows = []
        existing_regions = []

        for window in all_windows:
            for monitor in get_monitors():
                window_region = get_displayed_bounds(window, existing_regions)

                if not window_region.is_empty:
                    # Add the new visible region to the list of existing regions
                    existing_regions.append(window_region)
                    displayed_windows.append((window.title, window_region.bounds))

        print(f"Iteration {i+1}/{iterations}")
        for title, bounds in displayed_windows:
            # the title may not display the app name
            # example: “Kanye West - Flashing Lights” rather than “Spotify - Kanye West - Flashing Lights”
            if title.strip() and bounds[2] - bounds[0] > 0 and bounds[3] - bounds[1] > 0:
                print(f"Window Title: {title}, Displayed Bounds: {bounds}")

        time.sleep(interval)

    avg_runtime = total_time / iterations
    avg_runtime_per_window = avg_runtime / total_windows if total_windows else 0

    print(f"\nAverage runtime of getAllWindows: {avg_runtime:.4f} seconds")
    print(f"Average runtime per window: {avg_runtime_per_window:.6f} seconds")

def command_handler():
    while True:
        command = input("Enter a command: ")

        if command.startswith("start"):
            try:
                _, interval, iterations = command.split()
                interval = float(interval)
                iterations = int(iterations)
                start_monitoring(interval, iterations)
            except ValueError:
                print("Invalid command format. Use: start <interval> <# of iterations>")
        elif command == "exit":
            print("Exiting program.")
            break
        else:
            print("Unknown command. Available commands: start, exit")

if __name__ == "__main__":
    command_thread = threading.Thread(target=command_handler)
    command_thread.start()
    command_thread.join()
