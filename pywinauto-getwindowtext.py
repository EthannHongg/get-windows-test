from pywinauto import Desktop

# Connect to all top-level windows
desktop = Desktop(backend="uia")  # 'uia' is the more modern UI Automation backend

# Iterate over all top-level windows
windows = desktop.windows()

for window in windows:
    print(f"Window Title: {window.window_text()}")
    try:
        # Access all child controls of the window
        child_elements = window.descendants()

        for child in child_elements:
            control_type = child.element_info.control_type
            text = child.window_text()

            # Print control type and associated text if available
            if text:
                print(f"   {control_type}: {text}")

    except Exception as e:
        print(f"   Could not access elements of this window: {str(e)}")

