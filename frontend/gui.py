import PySimpleGUI as sg

sg.set_options(font=("Arial", 12),
               scaling=2,
               margins=(100, 100),
               element_padding=(10, 10))


# Custom LabelInputText function
def LabelInputText(prompt="", *args, **kwargs):
    return [
        sg.Text(prompt, size=(20, 1)),
        sg.InputText(*args, **kwargs, expand_x=True)
    ]


# Switch Window Function
def switch_window(window, new_window_func: callable):
    # hide
    if window:
        window.hide()
    new_window_func()
    # show
    if window:
        window.un_hide()
