import matplotlib.pyplot as plt
import math

def titration(initial_hcl_conc, initial_hcl_volume, initial_naoh_conc):
    equilibrium_naoh_volume = initial_hcl_volume * initial_hcl_conc / initial_naoh_conc
    initial_hcl_ph = -math.log10(initial_hcl_conc)

    # x, y lists initialization
    y = []
    x = []

    volume_naoh_added = 0.0
    step_size = 0.0001  # Smaller step size for better accuracy
    total_volume = initial_hcl_volume

    while volume_naoh_added <= initial_hcl_volume + equilibrium_naoh_volume:
        # pH calculation
        if volume_naoh_added <= equilibrium_naoh_volume:
            hcl_remaining = initial_hcl_conc * initial_hcl_volume - initial_naoh_conc * volume_naoh_added
            ph = -math.log10(hcl_remaining)
        else:
            naoh_added_in_excess = volume_naoh_added - equilibrium_naoh_volume
            excess_naoh_moles = initial_naoh_conc * naoh_added_in_excess
            h3o_conc = excess_naoh_moles / (total_volume + naoh_added_in_excess)
            ph = -math.log10(h3o_conc)

        y.append(ph)
        x.append(volume_naoh_added)

        volume_naoh_added += step_size

    # Plotting the titration curve
    plt.plot(x, y, color='b')
    plt.xlabel('Volume of Added {}M NaOH (mL)'.format(initial_naoh_conc))
    plt.ylabel('pH')
    plt.title('Titration Curve of HCl with NaOH')
    plt.show()

def main():
    try:
        initial_hcl_conc, initial_hcl_volume, initial_naoh_conc = map(float,
                                                                     input("초기 HCl 농도, 부피, NaOH 농도를 순서대로 입력하세요 (단위: mL 또는 M):").split())
        titration(initial_hcl_conc, initial_hcl_volume, initial_naoh_conc)
    except ValueError:
        print("Invalid input. Please enter valid numeric values.")

if __name__ == "__main__":
    main()
