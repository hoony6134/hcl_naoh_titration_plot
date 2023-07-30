# IMPORT
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


# 입력값
a = 100 # a의 부피 (mL)
mol_a = 10 # a의 몰농도 (mol/L)
mol_t = 5 # t의 몰농도 (mol/L)


# 데이터 생성
N = 40 # 데이터 개수
t = a*mol_a/mol_t # 당량점

x1 = np.linspace(0, t - 1e-6, N//2) # 0부터 t까지 N//2개의 데이터 생성 (당량점 이전)
x2 = np.linspace(t + 1e-6, 2*t, N//2) # t부터 2t까지 N//2개의 데이터 생성 (당량점 이후)
anzahl_mol_von_starker_analyt = a*10**(-3)*mol_a # a의 몰수 (mol)
anzahl_mol_von_starker_titrant = t*10**(-3)*mol_t # t의 몰수 (mol)

y1 = (-1)*np.log10((anzahl_mol_von_starker_analyt - x1*10**(-3)*mol_t)/(x1*10**(-3) + a*10**(-3))) # 당량점 이전의 데이터 생성
y2 = 14 - (-1)*np.log10((x2*10**(-3)*mol_t - anzahl_mol_von_starker_analyt)/(x2*10**(-3) + a*10**(-3))) # 당량점 이후의 데이터 생성

x = np.concatenate((x1, x2)) # x1과 x2를 합쳐서 x로 만듦
y = np.concatenate((y1, y2)) # y1과 y2를 합쳐서 y로 만듦

# 곡선 그리기
def calc(x, A, B, C, D, E):
    return A/(1 + B**(x - C)) + D + E*x

parameters, covariance = curve_fit(f = calc, xdata = x, ydata = y, bounds = ([0, 0, 0.9*t, -10, -10], [14, 1, 1.1*t, 10, 10]))

for parameter, name in zip(parameters, ['A', 'B', 'C', 'D', 'E']):
    print(f'{name} = {parameter:14.10f}')

x_fitted = np.linspace(x[0], x[-1], 1000)
y_fitted = calc(x_fitted, *parameters)


# 그래프 보여주기
# plt의 기본 폰트는 한글을 지원하지 않으므로, 영어로 작성함
plt.style.use('seaborn-v0_8-darkgrid')
fig, ax = plt.subplots()

ax.plot(x, y, label = 'data', marker = 'o', linestyle = '')
ax.plot(x_fitted, y_fitted, label = 'fitted curve')

ax.set_xlabel('Volume of titrant in ml')
ax.set_ylabel('pH')
ax.set_title('Titration curve of {} M Acid and {} M Base ({} data)'.format(mol_a, mol_t,N))
ax.legend(frameon = True)

plt.show()