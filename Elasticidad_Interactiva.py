import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ------------------------------
#     CONFIGURACIÓN DE LA PÁGINA
# ------------------------------
st.set_page_config(
    page_title="Elasticidad de la Demanda",
    layout="centered"
)

st.title("📊 Elasticidad Precio de la Demanda (App Interactiva)")
st.write("Modifica el precio y observa cómo se desplazan los puntos en las gráficas.")

# ------------------------------
#     FUNCIONES
# ------------------------------
def calcular_q_desde_p(p):
    return 100 - 2 * p

def calcular_p_desde_q(q):
    return 50 - 0.5 * q

# ------------------------------
#     SLIDER
# ------------------------------
precio = st.slider(
    "Selecciona el Precio (P):",
    min_value=1.0,
    max_value=49.0,
    value=25.0,
    step=0.5
)

q = calcular_q_desde_p(precio)
it = precio * q

# Elasticidad
dq_dp = -2
elasticidad = dq_dp * (precio / q)

# Tipo de elasticidad
if abs(elasticidad) > 1:
    color_el = "green"
    tipo_texto = "Demanda Elástica"
elif abs(elasticidad) < 1:
    color_el = "red"
    tipo_texto = "Demanda Inelástica"
else:
    color_el = "blue"
    tipo_texto = "Demanda Unitaria"

# ------------------------------
#     MÉTRICAS
# ------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Precio (P)", f"${precio:.2f}")
col2.metric("Cantidad (Q)", f"{q:.1f} unidades")
col3.metric("Ingreso Total (IT)", f"${it:.2f}")

st.markdown(
    f"<h4 style='color:{color_el}; text-align:center;'>{tipo_texto}</h4>",
    unsafe_allow_html=True
)

# ------------------------------
#     DATOS PARA GRÁFICAS
# ------------------------------
q_vals = np.linspace(0.1, 100, 200)
p_vals = calcular_p_desde_q(q_vals)
it_vals = q_vals * calcular_p_desde_q(q_vals)

# ------------------------------
#     GRÁFICA 1 — DEMANDA (P vs Q)
# ------------------------------
fig1 = go.Figure()

# Curva de demanda
fig1.add_trace(go.Scatter(
    x=q_vals, y=p_vals,
    mode="lines",
    line=dict(color="royalblue", width=3),
    name="Curva de Demanda"
))

# Punto dinámico
fig1.add_trace(go.Scatter(
    x=[q], y=[precio],
    mode="markers",
    marker=dict(size=16, color="crimson"),
    name="Punto actual"
))

fig1.update_layout(
    title="Curva de Demanda (P vs Q)",
    xaxis_title="Cantidad (Q)",
    yaxis_title="Precio (P)",
    template="plotly_white",
    height=450
)

# ------------------------------
#     GRÁFICA 2 — INGRESO TOTAL (IT)
# ------------------------------
fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=q_vals, y=it_vals,
    mode="lines",
    line=dict(color="green", width=3),
    name="Ingreso Total"
))

fig2.add_trace(go.Scatter(
    x=[q], y=[it],
    mode="markers",
    marker=dict(size=16, color="crimson"),
    name="Punto actual"
))

fig2.update_layout(
    title="Ingreso Total (IT = P × Q)",
    xaxis_title="Cantidad (Q)",
    yaxis_title="IT ($)",
    template="plotly_white",
    height=450
)

# ------------------------------
#     MOSTRAR GRÁFICAS
# ------------------------------
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
