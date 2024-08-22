from pywinauto import Application

app = Application().connect(title="Your Window Title")
dlg = app.window(title="Your Window Title")
text = dlg.child_window(title="Text Element Title", control_type="Text").window_text()

print(text)
