import tkinter as tk
from tkinter import ttk, Toplevel
import sentencias 
from mochila_clas import AlgoritmoGenetico
root = tk.Tk()
plantas = sentencias.obtener_nombres_de_plantas()
tipos_cultivos = sentencias.obtener_tipos_de_cultivos()
riesgos = sentencias.obtener_riesgos()

# config the root window
root.geometry('600x800')
root.resizable(False, False)
root.title('Dropdown Checkboxes')

# set the default font size
default_font = ('Arial', 18)
root.option_add('*Font', default_font)

# list of options for each set
options = [
    plantas,
    tipos_cultivos,
    plantas,
    riesgos
]

# list of names for each set
names = [
    'Selecciona las planta que deseas sembrar',
    'Tipos de Cultivos que te gustaria sembrar',
    'Plantas de Nuevas que te gustarian sembrar',
    'Riesgos que conoscas en tu zona '
]

# variable to track the opened toplevel window
opened_toplevel = None

def show_options(name, selected_options, options):
    """Create a toplevel window with checkboxes for each option"""
    global opened_toplevel
    if opened_toplevel is not None:
        return

    top = Toplevel(root)
    top.title(f"{name}")

    # set the default font size for the toplevel window
    top.option_add('*Font', default_font)

    # set the opened toplevel window
    opened_toplevel = top

    # create a checkbox for each option
    for option in options:
        selected_options[option] = tk.BooleanVar()
        ttk.Checkbutton(top, text=option, variable=selected_options[option]).pack(anchor='w')

    def on_ok_click():
        """Close the toplevel window"""
        top.destroy()
        # clear the opened toplevel window
        global opened_toplevel
        opened_toplevel = None

    ttk.Button(top, text="OK", command=on_ok_click).pack()

selected = {}

# create four button for four sets of selection
for i in range(4):
    name = names[i]
    label = ttk.Label(text=f"{name}:")
    label.pack(fill=tk.X, padx=5, pady=5)

    selected[name] = {}
    ttk.Button(root, text=f"Select Option for {name}", command=lambda name=name, options=options[i]: show_options(name, selected[name], options)).pack(fill=tk.X, padx=5, pady=5)

# create a combobox for single selection
single_selection1 = tk.StringVar()
label = ttk.Label(text="Selecciona el suelo con el que cuentas")
label.pack(fill=tk.X, padx=5, pady=5)
single_options1 = sentencias.obtener_suelos()
combobox1 = ttk.Combobox(root, textvariable=single_selection1, values=single_options1, state='readonly')
combobox1.pack(fill=tk.X, padx=5, pady=5)

# create another combobox for single selection
single_selection2 = tk.StringVar()
label = ttk.Label(text="Selecciona el clima con el que cuentas")
label.pack(fill=tk.X, padx=5, pady=5)
single_options2 = sentencias.obtener_climas()
combobox2 = ttk.Combobox(root, textvariable=single_selection2, values=single_options2, state='readonly')
combobox2.pack(fill=tk.X, padx=5, pady=5)

# create a third combobox for single selection
single_selection3 = tk.StringVar()
label = ttk.Label(text="Selecciona el mes de siembra:")
label.pack(fill=tk.X, padx=5, pady=5)
single_options3 = sentencias.obtener_meses()
combobox3 = ttk.Combobox(root, textvariable=single_selection3, values=single_options3, state='readonly')
combobox3.pack(fill=tk.X, padx=5, pady=5)

# handle button click event
def on_button_click():
    """ handle button click event """
    selected_options = []
    for name, options in selected.items():
        selected_options.append([option for option, var in options.items() if var.get()])
        
    # retrieve values from settings
    datos_algoritmos = []
    for i in range(6):
        datos_algoritmos.append(settings_inputs[i].get())
    
    print(selected_options)
    print(datos_algoritmos)
    suelo = single_selection1.get()
    cultivos_usuario = selected_options[0]
    cantidad_de_cultivos = 2
    cultivo_deseado = selected_options[2]
    tipo_cultivo_usuario = selected_options[1]
    clima_usuario = single_selection2.get()
    mes_de_siembra = single_selection3.get()
    riesgos_conocidos = selected_options[3]

    algoritmo_genetico = AlgoritmoGenetico(suelo, cultivos_usuario, cantidad_de_cultivos, cultivo_deseado,
                                           tipo_cultivo_usuario, clima_usuario, mes_de_siembra, riesgos_conocidos,datos_algoritmos)
    algoritmo_genetico.main()


# add a button to trigger the selection
button = ttk.Button(root, text="OK", command=on_button_click)
button.pack(fill=tk.X, padx=5, pady=5)

# create a settings toplevel
settings_inputs = [tk.StringVar() for _ in range(6)]  # create six StringVars for settings
def show_settings():
    """Create a toplevel window with input fields for each setting"""
    global opened_toplevel
    if opened_toplevel is not None:
        return

    top = Toplevel(root)
    top.title("Configurations")

    # set the default font size for the toplevel window
    top.option_add('*Font', default_font)

    # set the opened toplevel window
    opened_toplevel = top
    titulo_labels = ["cantidad poblacion inicial","poblacion Maxima","posibilidad de cruza","probabilidad de mutacion del individuo","probabilidad de mutacion del gen","cantidad de iteraciones"]
    # create an entry for each setting
    for i in range(6):
        label = ttk.Label(top, text=f"{titulo_labels[i]}:")
        label.pack(fill=tk.X, padx=5, pady=5)
        entry = ttk.Entry(top, textvariable=settings_inputs[i])
        entry.pack(fill=tk.X, padx=5, pady=5)

    def on_ok_click():
        """Close the toplevel window"""
        top.destroy()
        # clear the opened toplevel window
        global opened_toplevel
        opened_toplevel = None

    ttk.Button(top, text="OK", command=on_ok_click).pack()

# add a button to open settings
button = ttk.Button(root, text="Configurations", command=show_settings)
button.pack(fill=tk.X, padx=5, pady=5)

# create a list with your default values
default_values = [2,32,50,33,60,80]

# preload some values to settings
for i, var in enumerate(settings_inputs):
    var.set(default_values[i])

root.mainloop()
