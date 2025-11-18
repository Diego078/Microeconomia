
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# --- 1. Definir la Curva de Demanda Lineal ---
# Usamos una demanda simple: Q = 100 - 2P
# O, reordenando para el gráfico (P en el eje Y): P = 50 - 0.5Q

def calcular_p_desde_q(q):
    """ Calcula el Precio (P) dada la Cantidad (Q) """
    return 50 - 0.5 * q

def calcular_q_desde_p(p):
    """ Calcula la Cantidad (Q) dado el Precio (P) """
    return 100 - 2 * p

# --- 2. Crear los datos para los gráficos estáticos ---
# Rango de Cantidad (Q) de 0 a 100
q_vals = np.linspace(0.01, 99.99, 200) # Evitamos 0 y 100 exactos para evitar div/cero
# Precios (P) correspondientes
p_vals = calcular_p_desde_q(q_vals)
# Ingreso Total (IT = P * Q)
it_vals = p_vals * q_vals

# --- 3. Configurar la Figura y los Ejes (Subplots) ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7), constrained_layout=True,
                               gridspec_kw={'height_ratios': [2, 1]})
fig.suptitle('Análisis Interactivo de Elasticidad e Ingreso Total', fontsize=16)

# --- GRÁFICO 1: Curva de Demanda ---
ax1.plot(q_vals, p_vals, 'b-', lw=2, label='Demanda (P = 50 - 0.5Q)')
ax1.set_title('Curva de Demanda')
ax1.set_xlabel('Cantidad (Q)')
ax1.set_ylabel('Precio (P)')
ax1.set_xlim(0, 100)
ax1.set_ylim(0, 50)
ax1.grid(True, linestyle='--', alpha=0.6)

# Añadir líneas para el punto de elasticidad unitaria (Q=50, P=25)
ax1.axvline(50, color='gray', linestyle='--', label='Elasticidad Unitaria (Q=50)')
ax1.axhline(25, color='gray', linestyle='--')

# Puntos y texto que se actualizarán dinámicamente
punto_demanda, = ax1.plot(0, 0, 'ro', markersize=10) # Punto rojo en la demanda
texto_info = ax1.text(5, 40, '', fontsize=9, 
                        bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

# --- GRÁFICO 2: Ingreso Total ---
ax2.plot(q_vals, it_vals, 'g-', lw=2, label='Ingreso Total (IT = P*Q)')
ax2.set_title('Ingreso Total')
ax2.set_xlabel('Cantidad (Q)')
ax2.set_ylabel('Ingreso Total ($)')
ax2.set_xlim(0, 100)
ax2.set_ylim(0, max(it_vals) * 1.1)
ax2.grid(True, linestyle='--', alpha=0.6)

# Punto de Ingreso Total que se actualizará
punto_it, = ax2.plot(0, 0, 'ro', markersize=10)
# Línea vertical para el IT máximo
ax2.axvline(50, color='gray', linestyle='--', label='IT Máximo')
ax2.legend()


# --- 4. Configurar el Widget (Slider) ---
# Eje para el slider
ax_slider = fig.add_axes([0.15, 0.01, 0.7, 0.03], facecolor='lightgoldenrodyellow')

# Crear el slider. Controlará el PRECIO (P) de 0.01 a 49.99
slider_p = Slider(
    ax=ax_slider,
    label='Mover Precio (P)',
    valmin=0.01,     # Precio mínimo (evita div/cero en P=0)
    valmax=49.99,    # Precio máximo (evita div/cero en Q=0)
    valinit=35,      # Precio inicial
    valstep=0.5      # Incremento
)

# --- 5. Definir la Función de Actualización ---
def actualizar(precio_actual):
    
    # 1. Calcular valores basados en el precio del slider
    q_actual = calcular_q_desde_p(precio_actual)
    it_actual = precio_actual * q_actual
    
    # 2. Calcular Elasticidad (PED)
    # Fórmula: Ed = (dQ/dP) * (P/Q)
    # Para nuestra demanda Q = 100 - 2P, la derivada (dQ/dP) es constante: -2
    dq_dp = -2
    
    # No necesitamos chequear div/cero porque el slider evita P=0 y P=50
    elasticidad = dq_dp * (precio_actual / q_actual)
    
    # 3. Clasificar la elasticidad
    if abs(elasticidad) > 1.001: # Pequeño margen de error
        tipo_elasticidad = "Elástica"
    elif abs(elasticidad) < 0.999: # Pequeño margen de error
        tipo_elasticidad = "Inelástica"
    else:
        tipo_elasticidad = "Unitaria"

    # 4. Formatear el texto de información
    info = f"Precio (P):   ${precio_actual:,.2f}\n"
    info += f"Cantidad (Q): {q_actual:,.1f}\n"
    info += f"Ingreso Total:  ${it_actual:,.2f}\n"
    info += f"Elasticidad:  {elasticidad:,.2f} ({tipo_elasticidad})"
    
    # 5. Actualizar los gráficos
    texto_info.set_text(info)
    punto_demanda.set_data([q_actual], [precio_actual])
    punto_it.set_data([q_actual], [it_actual])
    
    # Redibujar la figura
    fig.canvas.draw_idle()

# --- 6. Conectar el Slider a la Función y Mostrar ---
slider_p.on_changed(actualizar)

# Llamar a la función una vez al inicio
actualizar(slider_p.val)

plt.show()
