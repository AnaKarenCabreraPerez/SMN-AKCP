import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# -------------------------------------------------------- #

# Intentar leer archivo xlsx 
# El formato del SMN no es valido se tiene que editar 
# Ver manual de uso 

# -------------------------------------------------------- #

ruta_excel = "Estacion_EL SALADO_90_dias.xlsx"

# Intenta leer el Excel incluso si hay errores de formato
try:
    df = pd.read_excel(ruta_excel, header=None, engine='openpyxl') 
except ValueError:
    print("Hubo un error de formato. Intentalo con otro motor:")
    df = pd.read_excel(ruta_excel, header=None)  # Utiliza el motor predeterminado de Pandas

# Guardar el DataFrame como archivo CSV
df.to_csv("archivo.csv", index=False, header=False)

# -------------------------------------------------------- #

# Cargar datos del archivo recien generado
# Deberia ser automatico este proceso

# -------------------------------------------------------- #

datos = pd.read_csv("archivo.csv")

# Convertir la columna "Fecha Local" a tipo datetime
datos["Fecha Local"] = pd.to_datetime(datos["Fecha Local"])

# Seleccionar la columna de precipitación
precipitacion = datos["Precipitación (mm)"]

# -------------------------------------------------------- #

# Visualizar serie de tiempo

# -------------------------------------------------------- #

plt.plot(datos["Fecha Local"], precipitacion)
plt.xlabel("Fecha")
plt.ylabel("Precipitación (mm)")
plt.show()

# -------------------------------------------------------- #

# Estadísticas básicas

# -------------------------------------------------------- #

print(precipitacion.describe())

# -------------------------------------------------------- #

# Rescaled Range (R/S) Method
# Función para calcular R/S y el exponente de Hurst
# Como en nuestros datos existen "0" de dias sin lluvia 

# Opcion 1: Filtrar ceros 
    # non_zero_idx = np.nonzero(diff)[0]
    # diff = diff[non_zero_idx]    
# Opcion 2: Agregar pequeña constante a los valores 0 
    # diff = diff + 1e-10  

# -------------------------------------------------------- #

def rescaled_range(data):
    diff = np.diff(data)
    mean = np.mean(diff)
    std = np.std(diff)
    # ----------------- #
    diff = diff + 1e-10 
    # ----------------- #
    rs = np.zeros(len(data))
    for i in range(1, len(data)):
        rs[i] = max(diff[:i]) - min(diff[:i]) / (std if std != 0 else 1e-10) 
    return rs

# Calcular R/S para la serie de precipitacion
rs = rescaled_range(precipitacion)

# Calcular el exponente de Hurst
hurst_exponent = stats.linregress(np.log(np.arange(1, len(precipitacion)+1)), np.log(rs))[0]
