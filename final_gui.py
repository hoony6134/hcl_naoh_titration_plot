import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

global a
global mol_a
global mol_t
global N

def calc(x, A, B, C, D, E):
    return A / (1 + B**(x - C)) + D + E * x

def draw_and_show_plot():
    global mol_a
    global mol_t
    global a
    global N
    # GUI에서 입력받은 값 가져오기
    a = float(entry_a.get())
    mol_a = float(entry_mol_a.get())
    mol_t = float(entry_mol_t.get())

    # 데이터 생성
    t = a * mol_a / mol_t
    N = 80  # 데이터 개수: 80개 (40개: 당량점 이전, 40개: 당량점 이후) / 데이터 개수를 늘리면 더 정확한 곡선을 그릴 수 있음

    x1 = np.linspace(0, t - 1e-6, N // 2) # 0부터 t까지 N//2개의 데이터 생성 (당량점 이전)
    x2 = np.linspace(t + 1e-6, 2 * t, N // 2) # t부터 2t까지 N//2개의 데이터 생성 (당량점 이후)
    acid_mol_remaining = a * 10**(-3) * mol_a # 남은 산의 몰수
    base_mol_remaining = t * 10**(-3) * mol_t # 남은 염기의 몰수

    y1 = (-1) * np.log10((acid_mol_remaining - x1 * 10**(-3) * mol_t) / (x1 * 10**(-3) + a * 10**(-3))) # 당량점 이전의 pH 계산해서 numpy array에 추가
    y2 = 14 - (-1) * np.log10((x2 * 10**(-3) * mol_t - acid_mol_remaining) / (x2 * 10**(-3) + a * 10**(-3))) # 당량점 이후의 pH 계산해서 numpy array에 추가

    x = np.concatenate((x1, x2)) # x1과 x2를 합쳐서 numpy array로 만듦 (당량점 이전의 데이터와 당량점 이후의 데이터를 합침)
    y = np.concatenate((y1, y2)) # y1과 y2를 합쳐서 numpy array로 만듦 (당량점 이전의 데이터와 당량점 이후의 데이터를 합침)

    # 데이터에 맞는 곡선을 scipy.optimize.curve_fit() 함수를 이용해 그려주기
    parameters, covariance = curve_fit(f=calc, xdata=x, ydata=y, bounds=([0, 0, 0.9 * t, -10, -10], [14, 1, 1.1 * t, 10, 10]))
    x_fitted = np.linspace(x[0], x[-1], 1000)
    y_fitted = calc(x_fitted, *parameters)

    # 그래프 그리기 (기존에 그려진 그래프가 있다면 지우고 다시 그림)
    plt.clf()
    plt.style.use('bmh') # 그래프 스타일 설정
    fig, ax = plt.subplots()

    ax.plot(x, y, label='data', marker='o', linestyle='')
    ax.plot(x_fitted, y_fitted, label='fitted curve')

    ax.set_xlabel('Volume of titrant in ml')
    ax.set_ylabel('pH')
    ax.set_title('Titration curve of {} M Acid and {} M Base ({} data)'.format(mol_a, mol_t, N))
    ax.legend(frameon=True)

    # Save the figure for showing in a separate window
    plt.savefig('plot.png')  # Save the plot to a file

    # Display the plot in a new window
    show_plot()

def show_plot():
    global a
    global mol_a
    global mol_t
    global N
    # 그래프를 보여주는 새로운 창 생성
    if not hasattr(show_plot, "plot_window") or not show_plot.plot_window.winfo_exists(): # 중복 생성 방지
        show_plot.plot_window = tk.Toplevel(root)
        show_plot.plot_window.title('{} M 강산과 {} M 강염기의 중화적정 곡선 (데이터 수: {})'.format(mol_a, mol_t, N))

        # 중화적정 곡선 이미지 저장하고 보여줌
        plot_image = tk.PhotoImage(file='plot.png')
        plot_label = tk.Label(show_plot.plot_window, image=plot_image)
        plot_label.image = plot_image
        plot_label.pack()

# Tkinter GUI 창 보여주기
root = tk.Tk()
root.title("강산-강염기 중화적정 곡선 그리기")

# Create main frame
main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

# Create input fields and labels
label_a = tk.Label(main_frame, text="산의 부피 (mL)")
label_a.grid(row=0, column=0)
entry_a = tk.Entry(main_frame)
entry_a.grid(row=0, column=1)

label_mol_a = tk.Label(main_frame, text="산의 몰농도 (M)")
label_mol_a.grid(row=1, column=0)
entry_mol_a = tk.Entry(main_frame)
entry_mol_a.grid(row=1, column=1)

label_mol_t = tk.Label(main_frame, text="염기의 몰농도 (M)")
label_mol_t.grid(row=2, column=0)
entry_mol_t = tk.Entry(main_frame)
entry_mol_t.grid(row=2, column=1)

# Create and bind the draw button
button_draw = tk.Button(main_frame, text="중화적정 곡선 그리기", command=draw_and_show_plot)
button_draw.grid(row=4, columnspan=2)

# Run the tkinter main loop
root.mainloop()
