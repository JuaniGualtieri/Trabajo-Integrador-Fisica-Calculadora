import tkinter as tk
from tkinter import messagebox


FRECUENCIA = 50  # frecuencia de la red en Hz
IVA = 0.21  # IVA del 21%
ALUMBRADO_PUBLICO = 4.4260  # Costo de alumbrado público en pesos

# funcion para calcular el consumo neto entre dos lecturas
def calcular_consumo_neto(consumo_inicial, consumo_final):
    return max(0, consumo_final - consumo_inicial)

# funcion para calcular la corriente que toma en cuenta el consumo y la tension
def calcular_corriente(consumo_kwh, voltaje):
    consumo_wh = consumo_kwh * 1000  # convertidor de kWh a Wh
    horas_por_mes = 30 * 24  # aprox. de horas en un mes
    potencia_media_w = consumo_wh / horas_por_mes  # potencia media en W
    corriente = potencia_media_w / voltaje  # I = P / V
    return corriente

# funcion para calcular el costo bimestral basico y total
def calcular_facturacion(consumo_kwh):
    costo_fijo = 11.42  # Costo fijo del suministro
    costo_600_kwh = 123.97  # Precio de los primeros 600 kWh
    costo_exceso_600_kwh = 162.10  # Precio del consumo excedente de 600 kWh

    if consumo_kwh <= 600:
        facturacion_basica = costo_fijo + (consumo_kwh * costo_600_kwh / 600)
    else:
        exceso_kwh = consumo_kwh - 600
        facturacion_basica = costo_fijo + costo_600_kwh + (exceso_kwh * costo_exceso_600_kwh / 600)
    
    facturacion_total = facturacion_basica * (1 + IVA) + ALUMBRADO_PUBLICO
    return facturacion_basica, facturacion_total

# funcion que se activa cuando apretamos el boton "Calcular" en la interfaz
def calcular():
    try:
        consumo_inicial = float(entry_consumo_inicial.get())
        consumo_final = float(entry_consumo_final.get())
        voltaje = float(entry_voltaje.get())

        consumo_neto = calcular_consumo_neto(consumo_inicial, consumo_final)
        corriente = calcular_corriente(consumo_neto, voltaje)
        facturacion_basica, facturacion_total = calcular_facturacion(consumo_neto)

        # Mostrar resultados en la interfaz
        label_resultado_consumo.config(text=f"Consumo actual: {consumo_neto:.2f} kWh")
        label_resultado_corriente.config(text=f"Corriente consumida: {corriente:.2f} A")
        label_resultado_facturacion_basica.config(text=f"Facturacion Bimestral Basica: ${facturacion_basica:.3f}")
        label_resultado_facturacion_total.config(text=f"Facturacion Bimestral Final Total: ${facturacion_total:.3f}")

    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos.")


root = tk.Tk()
root.title("Calculadora de Facturacion Electrica")


label_consumo_inicial = tk.Label(root, text="Consumo Inicial (kWh):")
label_consumo_inicial.grid(row=0, column=0, padx=10, pady=10)
entry_consumo_inicial = tk.Entry(root)
entry_consumo_inicial.grid(row=0, column=1, padx=10, pady=10)

label_consumo_final = tk.Label(root, text="Consumo Final (kWh):")
label_consumo_final.grid(row=1, column=0, padx=10, pady=10)
entry_consumo_final = tk.Entry(root)
entry_consumo_final.grid(row=1, column=1, padx=10, pady=10)


label_voltaje = tk.Label(root, text="Tension (V):")
label_voltaje.grid(row=2, column=0, padx=10, pady=10)
entry_voltaje = tk.Entry(root)
entry_voltaje.grid(row=2, column=1, padx=10, pady=10)
entry_voltaje.insert(0, "220")  # Valor fijo

# Botón de cálculo
button_calcular = tk.Button(root, text="Calcular", command=calcular)
button_calcular.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Resultados
label_resultado_consumo = tk.Label(root, text="Consumo actual:")
label_resultado_consumo.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

label_resultado_corriente = tk.Label(root, text="Corriente consumida:")
label_resultado_corriente.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

label_resultado_facturacion_basica = tk.Label(root, text="Facturación Bimestral Basica:")
label_resultado_facturacion_basica.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

label_resultado_facturacion_total = tk.Label(root, text="Facturación Bimestral Final Total:")
label_resultado_facturacion_total.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()