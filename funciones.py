from tablas import *


def calcular(caudal, cotaSup, cotaInf, longitud, tuberiaPVC):
    # Primera parte -------------------------------------------------------------------------------------------

    #  Datos de entrada----------------------

    # caudal = 75. # L/s
    # cotaSup = 2015.52  # m
    # cotaInf = 2015.  # m
    # longitud = 250  # m
    # tuberiaPVC = True  # False para concreto

    pesoEspAgua = 9810.0  # N/m3

    # Cálculos-----------------------------------

    pendiente = (cotaSup - cotaInf) * 100 / longitud
    # Aquí toca decidir si es de PVC o de concreto y seguir
    if tuberiaPVC:  # PVC
        n = 0.009
        tuberias = tuberiasS8
        limiteSanitario = 170
    else:  # Concreto
        n = 0.013
        tuberias = tuberiasConc
        limiteSanitario = 140

    Dinicialm = 1.548 * (n * caudal / 1000 / (pendiente / 100) ** 0.5) ** 0.375  # Diámetro inicial en m
    Dinicialmm = round(Dinicialm * 1000, 1)  # Diámetro inicial en mm
    # Filtrar el menor de los que son superiores al Dinicial:
    Dinterno = np.min(tuberias[:, 1][tuberias[:, 1] >= Dinicialmm])  # mm
    # Encontrar la fila donde está el Dinterno en la matriz de tuberías
    filaDnominal = np.where(tuberias == Dinterno)[0][0]
    Dnominal = tuberias[filaDnominal, 0]

    # Salidas-------------------------------------------------

    # print('Material: ', 'PVC' if tuberiaPVC else 'Concreto')
    # print(f'Diámetro inicial: {Dinicialmm} mm\nDiámetro interno: {Dinterno} mm\nDiámetro nominal: {Dnominal}')
    # print('Para alcantarillado sanitario', 'sí' if Dinterno > limiteSanitario else 'no', 'cumple D interno')
    # print('Para alcantarillado pluvial/combinado', 'sí' if Dinterno > 260 else 'no', 'cumple D interno')

    # Segunda parte -----------------------------------------------------------------------------------------------------

    # Condiciones a tubo lleno
    Qo = 0.312 * ((Dinterno / 1000) ** (8 / 3)) * ((pendiente / 100) ** (1 / 2)) / n * 1000  # L/s
    Ao = np.pi * ((Dinterno / 1000) ** 2) / 4  # m2
    Vo = Qo / 1000 / Ao  # m/s
    Ro = Dinterno / 4000  # m
    # print(f'\nCondiciones a tubo lleno:\nQo: {round(Qo, 2)} L/s, '
    #       f'Ao: {round(Ao, 3)} m2, Vo: {round(Vo, 3)} m/s, Ro: {round(Ro, 5)} m')

    # Relaciones hidráulicas
    QQo = round(caudal / Qo, 2)
    # Encontrar la columna donde está el Q/Qo en la matriz de relaciones hidráulicas
    columnaQQo = np.where(relHid == QQo)[1][0]
    VVo = relHid[1][columnaQQo]
    dDo = relHid[2][columnaQQo]
    RRo = relHid[3][columnaQQo]
    # print(f'\nRelaciones hidráulicas:\nQ/Qo: {QQo},  V/Vo: {VVo}, D/Do: {dDo}, R/Ro: {RRo}')
    # print('Para alcantarillado sanitario', 'sí' if dDo <= 0.85 else 'no', 'cumple D/Do')
    # print('Para alcantarillado pluvial/combinado', 'sí' if dDo < 0.93 else 'no', 'cumple D/Do')

    # Condiciones reales
    V = VVo * Vo  # m/s
    d = dDo * Dinterno  # mm
    Rh = RRo * Ro  # m
    # print(f'\nCondiciones reales:\nV: {round(V, 3)} m/s, d: {round(d, 3)} mm, Rh: {round(Rh, 3)}m')
    # print('Para alcantarillado sanitario/pluvial/combinado',
    #       'sí cumple velocidad' if V <= 5.0 else 'no cumple. Disminuir velocidad')

    # Fuerza tractiva
    ft = pesoEspAgua * Rh * pendiente / 100  # Pa
    # print(f'\nFuerza tractiva: {round(ft, 2)} Pa')
    # print('Para alcantarillado sanitario', 'sí' if ft >= 1.0 else 'no', 'cumple fuerza tractiva')
    # print('Para alcantarillado pluvial/combinado', 'sí' if ft >= 2.0 else 'no', 'cumple fuerza tractiva')

    texto = 'Material: ' + ('PVC' if tuberiaPVC else 'Concreto') \
            + '\nDiámetro inicial: ' + str(Dinicialmm) + ' mm' \
            + '\nDiámetro interno: ' + str(Dinterno) + ' mm' \
            + '\nDiámetro nominal: ' + str(Dnominal) \
            + '\nPara alcantarillado sanitario ' + ('sí' if Dinterno > limiteSanitario else 'no') + ' cumple D interno' \
            + '\nPara alcantarillado pluvial/combinado ' + ('sí' if Dinterno > 260 else 'no') + ' cumple D interno' \
            + '\n\nCondiciones a tubo lleno:' \
            + '\nQo: ' + str(round(Qo, 2)) + 'L/s, Ao: ' + str(round(Ao, 3)) \
            + ' m2, Vo: ' + str(round(Vo, 3)) + ' m/s, Ro: ' + str(round(Ro, 5)) + ' m' \
            + '\n\nRelaciones hidráulicas:' \
            + '\nQ/Qo: ' + str(QQo) + ', V/Vo: ' + str(VVo) + ', D/Do: ' + str(dDo) + ', R/Ro: ' + str(RRo) \
            + '\nPara alcantarillado sanitario ' + ('sí' if dDo <= 0.85 else 'no') + ' cumple D/Do' \
            + '\nPara alcantarillado pluvial/combinado ' + ('sí' if dDo < 0.93 else 'no') + ' cumple D/Do' \
            + '\n\nCondiciones reales:\nV: ' + str(round(V, 3)) + ' m/s, d: ' + str(round(d, 3)) + ' mm, Rh: ' + str(round(Rh, 3)) + ' m' \
            + '\nPara alcantarillado sanitario/pluvial/combinado ' \
            + ('sí cumple velocidad' if V <= 5.0 else 'no cumple. Disminuir velocidad') \
            + '\n\nFuerza tractiva: ' + str(round(ft, 2)) + ' Pa' \
            + '\nPara alcantarillado sanitario ' + ('sí' if ft >= 1.0 else 'no') + ' cumple fuerza tractiva' \
            + '\nPara alcantarillado pluvial/combinado ' + ('sí' if ft >= 2.0 else 'no') + ' cumple fuerza tractiva'

    return texto
