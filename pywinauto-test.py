from pywinauto import Desktop, Application
from pywinauto.application import WindowSpecification
import time
import threading

def get_all_windows_info():
    windows_info = []
    # Enumerate all top-level windows
    for window in Desktop(backend="uia").windows():
        try:
            # Retrieve window details
            title = window.window_text()
            rect = window.rectangle()
            bounds = (rect.left, rect.top, rect.right, rect.bottom)
            process_id = window.process_id()
            
            # Attach to the application to retrieve app name or path
            app = Application(backend="uia").connect(process=process_id)
            exe_path = app.backend

            window_data = {
                'title': title,
                'bounds': bounds,
                'app_path': exe_path,
                'texts': [],
                'child_elements': []
            }
            
            # Attempt to retrieve text from the window (if possible)
            try:
                texts = window.texts()
                window_data['texts'] = texts
            except Exception as e:
                window_data['texts'] = [f"Text extraction failed: {str(e)}"]

            try:
                # Access all child controls of the window
                child_elements = window.descendants()

                for child in child_elements:
                    control_type = child.element_info.control_type
                    text = child.window_text()

                    # Print control type and associated text if available
                    if text:
                        window_data['child_elements'].append((control_type, text))

            except Exception as e:
                print(f"Could not access elements of this window: {str(e)}")


            windows_info.append(window_data)
        except Exception as e:
            print(f"Failed to process window: {str(e)}")
    
    return windows_info

def print_windows_info(windows_info):
    for window_info in windows_info:
        print(f"Window Title: {window_info['title']}")
        print(f"Bounds: {window_info['bounds']}")
        print(f"Application Path: {window_info['app_path']}")
        print("Texts:")
        for text in window_info['texts']:
            print(f"  {text}")
        print("=" * 50)

def start_monitoring(interval, iterations):
    total_time = 0

    for i in range(iterations):
        print(f"\n--- Iteration {i+1} ---")
        start_time = time.time()
        
        windows_info = get_all_windows_info()
        print_windows_info(windows_info)
        
        end_time = time.time()
        iteration_time = end_time - start_time
        total_time += iteration_time
        
        print(f"Iteration {i+1} runtime: {iteration_time:.4f} seconds")
        time.sleep(interval)
    
    average_runtime = total_time / iterations
    print(f"\nAverage runtime per iteration: {average_runtime:.4f} seconds")

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
