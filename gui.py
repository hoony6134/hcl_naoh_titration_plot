import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

# titration function
def titration_plot():
    initial_hcl_conc = float(hcl_conc_entry.get())
    initial_hcl_volume = float(hcl_volume_entry.get())
    initial_naoh_conc = float(naoh_conc_entry.get())
    equilibrium_naoh_volume = initial_hcl_volume * initial_hcl_conc / initial_naoh_conc

    initial_hcl_ph = -math.log10(initial_hcl_conc)

    # x, y lists initialization
    y = []
    x = []

    volume_naoh_added = 0.0
    step_size = 0.01
    naoh_remaining = 0
    total_volume = initial_hcl_volume

    while volume_naoh_added <= 2 * equilibrium_naoh_volume:
        if volume_naoh_added <= equilibrium_naoh_volume - step_size:
            hcl_remaining = initial_hcl_conc * initial_hcl_volume - initial_naoh_conc * volume_naoh_added
            ph = initial_hcl_ph - math.log10(hcl_remaining)
        else:
            naoh_remaining += step_size
            total_volume += step_size
            ph = 14 - initial_hcl_ph + math.log10(naoh_remaining / total_volume)
        y.append(ph)
        x.append(volume_naoh_added)

        volume_naoh_added += step_size

    # Create a figure and plot the data
    fig, ax = plt.subplots()
    ax.plot(x[:int(2 * equilibrium_naoh_volume / step_size) + 1], y[:int(2 * equilibrium_naoh_volume / step_size) + 1], color='b')
    ax.set_xlabel('Volume of Added {}M NaOH (mL)'.format(initial_naoh_conc))
    ax.set_ylabel('pH')
    ax.set_yticks([0, 7, 14])
    ax.set_title('Titration Curve of HCl with NaOH')

    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=5, pady=10)

# Create main application window
root = tk.Tk()
root.title('Titration Curve Plot')

# Labels and Entry widgets for initial values
hcl_conc_label = ttk.Label(root, text='초기 HCl 농도 (M):')
hcl_conc_label.grid(row=0, column=0, padx=5, pady=5)

hcl_conc_entry = ttk.Entry(root)
hcl_conc_entry.grid(row=0, column=1, padx=5, pady=5)

hcl_volume_label = ttk.Label(root, text='초기 HCl 부피 (mL):')
hcl_volume_label.grid(row=1, column=0, padx=5, pady=5)

hcl_volume_entry = ttk.Entry(root)
hcl_volume_entry.grid(row=1, column=1, padx=5, pady=5)

naoh_conc_label = ttk.Label(root, text='초기 NaOH 농도 (M):')
naoh_conc_label.grid(row=2, column=0, padx=5, pady=5)

naoh_conc_entry = ttk.Entry(root)
naoh_conc_entry.grid(row=2, column=1, padx=5, pady=5)

# Plot button
plot_button = ttk.Button(root, text='적정 곡선 그리기', command=titration_plot)
plot_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

# Run the main loop
root.mainloop()
