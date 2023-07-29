import sentencias
import random
from decimal import Decimal
import matplotlib.pyplot as plt
import mplcursors
import tkinter as tk
from tkinter import font

class AlgoritmoGenetico:
    def __init__(self, suelo, cultivos_usuario, cantidad_de_cultivos, cultivo_deseado, tipo_cultivo_usuario,
                 clima_usuario, mes_de_siembra, riesgos_conocidos,datos_algoritmos):
        self.cantidad_poblacion_inicial = int(datos_algoritmos[0])
        self.poblacion_maxima = int(datos_algoritmos[1])
        self.posibilidad_cruza = int(datos_algoritmos[2])
        self.posibilidad_mut_individuo = int(datos_algoritmos[3])
        self.posibilidad_mut_gen = int(datos_algoritmos[4])
        self.cantidad_iteraciones = int(datos_algoritmos[5])

        self.suelo = suelo
        self.cultivos_usuario = cultivos_usuario
        self.cantidad_de_cultivos = cantidad_de_cultivos
        self.cultivo_deseado = cultivo_deseado
        self.tipo_cultivo_usuario = tipo_cultivo_usuario
        self.clima_usuario = clima_usuario
        self.mes_de_siembra = mes_de_siembra
        self.riesgos_conocidos = riesgos_conocidos
        self.id_cultivo_usuario = []
        self.poblacion = []
        self.arreglo_claves = []
        self.mejor_individuo = []
        self.promedio_individuo = []
        self.peor_individuo = []
        self.poblacion_puntuacion = {}
        self.lo_mejor = []
        self.data = {}

        self.obtener_ids_plantas()
        self.poblacion = self.generar_n_individuos()

    def obtener_ids_plantas(self):
        for nombre_cultivo in self.cultivos_usuario:
            self.id_cultivo_usuario.append(sentencias.obtener_id_por_nombre(nombre_cultivo))
        self.id_planta_por_tipo_suelo = sentencias.obtener_lista_de_plantas_por_suelo(self.suelo)
        self.data = sentencias.obtener_datos_por_ids_planta(self.id_cultivo_usuario + self.id_planta_por_tipo_suelo)

    def generar_n_individuos(self):
        poblacion_inicial = []
        auxiliar_claves = []

        for clave in self.id_planta_por_tipo_suelo:
            self.arreglo_claves.append(clave)
        auxiliar_claves = self.arreglo_claves

        for i in range(self.cantidad_poblacion_inicial):
            auxiliar_claves_copia = auxiliar_claves[:] 
            random.shuffle(auxiliar_claves_copia) 
            poblacion_inicial.append(auxiliar_claves_copia) 

        return poblacion_inicial

    def seleccion_parejas(self):   
        numero_de_parejas = (len(self.poblacion) / 2) + 0.5 
        parejas_aleatorias = [random.sample(self.poblacion, 2) for _ in range(int(numero_de_parejas))]
        return parejas_aleatorias

    def cruza(self, parejas_aleatorias):
        hijos = []
        punto_de_cruce = 2 ###
        for pareja in parejas_aleatorias:
            if random.randrange(0, 100) <= self.posibilidad_cruza:
                tupla1 = pareja[0]
                tupla2 = pareja[1]
                # Realizar el cruce por punto fijo
                hijo1 = tupla1[:punto_de_cruce] + tupla2[punto_de_cruce:]
                hijo2 = tupla2[:punto_de_cruce] + tupla1[punto_de_cruce:]
                # Agregar las tuplas cruzadas a la lista de parejas cruzadas
                hijos.append(hijo1)
                hijos.append(hijo2)
        return hijos

    def reparar_hijos(self, hijos_sin_reparar):
        hijos_reparados = []
        for hijo in hijos_sin_reparar:
            auxiliar_elementos_usados = []

            for elemento in hijo:
                if elemento in auxiliar_elementos_usados:
                    for claves in self.arreglo_claves: 
                        if claves not in auxiliar_elementos_usados:
                            auxiliar_elementos_usados.append(claves)
                            break
                else:       
                    auxiliar_elementos_usados.append(elemento)
            hijos_reparados.append(auxiliar_elementos_usados)    
        return hijos_reparados

    def mutacion(self, hijos_reparados):    
        for hijo in hijos_reparados:
            arreglo_posiciones_que_mutan = []

            if random.randint(0, 100) <= self.posibilidad_mut_individuo:
                for posicion in range(len(hijo)):
                    if random.randint(0, 100) <= self.posibilidad_mut_gen:
                        arreglo_posiciones_que_mutan.append(posicion)

                self.Intercambio_de_valor(arreglo_posiciones_que_mutan, hijo)

            else:
                self.poblacion.append(hijo)

    def Intercambio_de_valor(self, arreglo_posiciones_que_mutan, hijo):
        for elemento in arreglo_posiciones_que_mutan:
            posicion_random = random.randint(0, len(hijo) - 1)
            elemento_1 = hijo[elemento]
            elemento_2 = hijo[posicion_random]

            hijo[elemento] = elemento_2
            hijo[posicion_random] = elemento_1

        self.poblacion.append(hijo)

    def valorar_individuo(self):
        index = 0
        for individuo in self.poblacion:
            aux_individuo = self.id_cultivo_usuario + individuo 
            self.obtener_aptitud(aux_individuo, index)
            index += 1

    def obtener_aptitud(self, individuo, index):
        puntuacion = Decimal(0)
        for id in individuo[:self.cantidad_de_cultivos + len(self.cultivos_usuario)]:

            if any(tipo_cultivo in self.cultivo_deseado for tipo_cultivo in self.data[id][2]):
                puntuacion += Decimal('0.3')
            else:
                puntuacion -= Decimal('0.1')

            if any(deseado in self.cultivo_deseado for deseado in self.data[id][0]):
                puntuacion += Decimal('0.3')

            for sub_id in self.data:
                if sub_id == id:
                    pass
                else:
                    if any(compatible in individuo[:self.cantidad_de_cultivos + len(self.cultivos_usuario)] for compatible in self.data[sub_id][12]):
                        puntuacion += Decimal('0.5')
                    else:
                        puntuacion -= Decimal('0.6')

                    for efectos_generados in self.data[sub_id][10]:
                        if efectos_generados in self.data[sub_id][11]:
                            puntuacion += Decimal('0.28')

            ph_planta_rango = [float(num) for num in self.data[id][5].split("-")]
            if ph_planta_rango[0] <= float(self.data[id][7][0]) <= ph_planta_rango[1]:
                puntuacion += Decimal('0.8')
            else:
                puntuacion -= Decimal('0.9')

            if self.clima_usuario in self.data[id][3]:
                puntuacion += Decimal('0.6')
            else:
                puntuacion -= Decimal('0.5')

            for riesgos in self.riesgos_conocidos:
                if riesgos in self.data[id][4]:
                    puntuacion -= Decimal('0.3')
                else:
                    puntuacion += Decimal('0.45')

            nutrientes_planta = [self.data[id][6][0], self.data[id][6][1], self.data[id][6][2], self.data[id][6][3]]
            nutrientes_suelo = [self.data[id][7][1], self.data[id][7][2], self.data[id][7][3], self.data[id][7][4], self.data[id][7][0]]
            if nutrientes_planta[0] <= nutrientes_suelo[0]:
                puntuacion += Decimal('0.3')
            if nutrientes_planta[1] <= nutrientes_suelo[1]:
                puntuacion += Decimal('0.3')
            if nutrientes_planta[2] <= nutrientes_suelo[2]:
                puntuacion += Decimal('0.3')
            if nutrientes_planta[3] <= nutrientes_suelo[3]:
                puntuacion += Decimal('0.3')

            if self.mes_de_siembra in self.data[id][9]:
                puntuacion += Decimal('0.8')
            else:
                puntuacion -= Decimal('0.7')

        self.poblacion_puntuacion[index] = puntuacion

    def ordenar_poblacion(self):
        diccionario_ordenado = {k: v for k, v in sorted(self.poblacion_puntuacion.items(), key=lambda item: item[1], reverse=True)}
        self.poblacion = [self.poblacion[key] for key in diccionario_ordenado.keys()]
        primer_elemento = next(iter(diccionario_ordenado.items()))
        ultimo_elemento = diccionario_ordenado.popitem()
        suma_valores = sum(self.poblacion_puntuacion.values())
        promedio = suma_valores / len(self.poblacion_puntuacion)
        self.lo_mejor = self.poblacion[0]
        self.mejor_individuo.append(primer_elemento[1])
        self.peor_individuo.append(ultimo_elemento[1])
        self.promedio_individuo.append(promedio)
        self.poblacion = self.poblacion[:self.poblacion_maxima]

    def tratamiento_suelo(self):
        ultima_clave = list(self.data.keys())[-1]
        individuo_completo = self.id_cultivo_usuario + self.lo_mejor
        nutrientes_suelo = [self.data[ultima_clave][7][1], self.data[ultima_clave][7][2], self.data[ultima_clave][7][3], self.data[ultima_clave][7][4], self.data[ultima_clave][7][0]]
        suma_absorcion = [0, 0, 0, 0]
        suma_incremento = [0, 0, 0, 0, 0]

        for id in individuo_completo[:self.cantidad_de_cultivos + len(self.cultivos_usuario)]:
            nutrientes_absorcion = [self.data[id][6][0], self.data[id][6][1], self.data[id][6][2], self.data[id][6][3]]
            nutrientes_incremento = [self.data[id][8][1], self.data[id][8][2], self.data[id][8][3], self.data[id][8][4], self.data[id][8][0]]

            suma_absorcion = [suma_absorcion[i] + nutrientes_absorcion[i] for i in range(len(suma_absorcion))]
            suma_incremento = [suma_incremento[i] + nutrientes_incremento[i] for i in range(len(suma_incremento))]

        for i in range(4):
            nutrientes_suelo[i] -= suma_absorcion[i]
        for i in range(5):
            nutrientes_suelo[i] += suma_incremento[i]

        self.suelo_final = nutrientes_suelo

    def main(self):
        for i in range(0, self.cantidad_iteraciones):
            parejas_aleatorias = self.seleccion_parejas()
            hijos_sin_reparar = self.cruza(parejas_aleatorias)
            hijos_reparados = self.reparar_hijos(hijos_sin_reparar)
            self.mutacion(hijos_reparados)
            self.valorar_individuo()
            self.ordenar_poblacion()
            self.poblacion_puntuacion.clear()
        #mostrar ventana
        ventana = tk.Tk()
        ventana.title("Resultado AG")
        fuente = font.Font(size=20)
        ##data
        self.tratamiento_suelo()
        ultima_clave = list(self.data.keys())[-1]
        nutrientes_suelo = [self.data[ultima_clave][7][1], self.data[ultima_clave][7][2], self.data[ultima_clave][7][3], self.data[ultima_clave][7][4], self.data[ultima_clave][7][0]]
        nitrogeno = f"{self.suelo_final[0]:.2f}"
        potasio =  f"{self.suelo_final[1]:.2f}"
        calcio =  f"{self.suelo_final[2]:.2f}"
        fosforo =  f"{self.suelo_final[3]:.2f}"
        ph =  f"{self.suelo_final[4]:.2f}"
        plantas_usuario = sentencias.obtener_datos_por_ids_planta(self.id_cultivo_usuario)
        label1 = tk.Label(ventana,font=fuente,  text=f"Plantas seleccionadas: "+ ', '.join(self.data[elemento][0] for elemento in plantas_usuario))
        label2 = tk.Label(ventana,font=fuente,  text=f"Plantas recomendadas: "+ ', '.join(self.data[elemento][0] for elemento in self.lo_mejor[:self.cantidad_de_cultivos]))
        label3 = tk.Label(ventana,font=fuente,  text=f"Configuracion del suelo inicial:  Nitrogeno:{nutrientes_suelo[0]}  Potasio:{nutrientes_suelo[1]}  Calcio:{nutrientes_suelo[2]}  Fosforo:{nutrientes_suelo[3]} PH:{nutrientes_suelo[4]}")
        label4 = tk.Label(ventana,font=fuente,  text=f"Configuracion del suelo final: Nitrogeno:{nitrogeno}  Potasio:{potasio}  Calcio:{calcio}  Fosforo:{fosforo} PH:{ph}")
        boton_grafica = tk.Button(ventana, text="Gráfica", command=self.plot_grafico)
        label1.grid(row=0, column=0)
        label2.grid(row=1, column=0)
        label3.grid(row=2, column=0)
        label4.grid(row=3, column=0)
        boton_grafica.grid(row=4, column=0, pady=10)
        ventana.geometry("800x500")
        ventana.mainloop()

    def plot_grafico(self):
        iteraciones = range(1, len(self.mejor_individuo) + 1)
        plt.figure(figsize=(19, 8))
        plt.plot(iteraciones, self.mejor_individuo, color='g', marker='o', linestyle='-', label='Mejor individuo')
        plt.plot(iteraciones, self.promedio_individuo, color='b', marker='o', linestyle='-', label='Promedio individuo')
        plt.plot(iteraciones, self.peor_individuo, color='r', marker='o', linestyle='-', label='Peor individuo')
        titulo = 'Comparación de individuos a lo largo de las iteraciones\n Se le recomienda al usuario: ' + ', '.join(self.data[elemento][0] for elemento in self.lo_mejor[:self.cantidad_de_cultivos])
        plt.title(titulo)
        plt.xlabel('Iteraciones')
        plt.ylabel('Valor del individuo')
        plt.legend()
        mplcursors.cursor(hover=True)
        plt.show()


