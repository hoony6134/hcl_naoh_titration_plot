import matplotlib.pyplot as plt
import math
global initial_hcl_conc
global initial_hcl_volume
global initial_naoh_conc
global equilibrium_naoh_volume

initial_hcl_conc, initial_hcl_volume, initial_naoh_conc = map(float, input("초기 HCl 농도, 부피, NaOH 농도를 순서대로 입력하세요 (단위: mL 또는 M):").split())
equilibrium_naoh_volume = initial_hcl_volume * initial_hcl_conc / initial_naoh_conc  # nMV = nMV 식 이용하여 당량점에서의 NaOH 부피 계산

global initial_hcl_ph
initial_hcl_ph = -math.log10(initial_hcl_conc)  # 초기 HCl 용액의 pH 계산

# titration 함수 정의
def titration(initial_hcl_conc, initial_hcl_volume, initial_naoh_conc, equilibrium_naoh_volume):
    # x, y 리스트 초기화
    y = []
    x = []

    volume_naoh_added = 0.0
    step_size = 0.01
    naoh_remaining = 0
    total_volume = initial_hcl_volume

    while volume_naoh_added <= 2 * equilibrium_naoh_volume:
        # pH 계산
        if volume_naoh_added <= equilibrium_naoh_volume-step_size:
            hcl_remaining = initial_hcl_conc * initial_hcl_volume - initial_naoh_conc * volume_naoh_added # NaOH 용액이 당량점 이전에는 HCl 용액의 용질을 모두 소모하므로 HCl 몰수에서 첨가함 NaOH 몰수를 빼줌
            ph = initial_hcl_ph -math.log10(hcl_remaining)
        else:
            naoh_remaining += step_size # 당량점 이후에는 NaOH만 남으므로 NaOH 몰수를 더해줌
            total_volume += step_size
            ph = 14 - initial_hcl_ph + math.log10(naoh_remaining / total_volume)
        y.append(ph)
        x.append(volume_naoh_added)

        volume_naoh_added += step_size

    # matplotlib의 경우 한글 폰트가 기본으로 지원되지 않으므로 영어로 레이블 등 작성함
    plt.plot(x[:int(2 * equilibrium_naoh_volume / step_size) + 1], y[:int(2 * equilibrium_naoh_volume / step_size) + 1], color='b')
    plt.xlabel('Volume of Added {}M NaOH (mL)'.format(initial_naoh_conc))
    plt.ylabel('pH')
    plt.yticks([0,7,14])
    plt.title('Titration Curve of HCl with NaOH')
    plt.show()

titration(initial_hcl_conc, initial_hcl_volume, initial_naoh_conc, equilibrium_naoh_volume)