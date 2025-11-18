import streamlit as st
import plotly.graph_objects as go
import numpy as np

# ------------------------------
# Funciones de microeconomía
# ------------------------------

def demanda_lineal(a, b, elasticidad):
    """
    Genera una curva de demanda con elasticidad controlada.
    """
    p = np.linspace(1, a, 200)
    q = a - b * p
    q = np.maximum(q, 0)

    # Ajuste de elasticidad “lógica”
    q = q ** (1 / elasticidad)
    return p, q

def oferta_lineal(c, d):
    p = np.linspace(1, 40, 200)
    q = d * p - c
    q = np.maximum(q, 0)
    return p, q

def calcular_elasticidad(p, q):
    pct_q = (q[1] - q[0]) / q[0]
    pct_p = (p[1] - p[0]) / p[0]
    return pct_q / pct_p

# ------------------------------
# Interfaz Streamlit
# ------------------------------
st.title("📈 Simulador Visual de Elasticidad (Microeconomía)")
st.write("")
st.write("Modifica los parámetros y observa cómo cambia la elasticidad y la forma de la curva.")

tab1, tab2 = st.tabs(["Elasticidad Precio de la Demanda", "Elasticidad Ingreso"])

# ------------------------------
# TAB 1: ELASTICIDAD PRECIO
# ------------------------------
with tab1:
    st.header("Elasticidad Precio de la Demanda")

    col1, col2 = st.columns(2)

    with col1:
        a = st.slider("Intercepto (a)", 20, 100, 60)
        b = st.slider("Pendiente (b)", 1, 10, 3)
        elasticidad = st.slider("Elasticidad (E)", 0.5, 3.0, 1.0, 0.1)

    p, q = demanda_lineal(a, b, elasticidad)
    E = calcular_elasticidad(p, q)

    # ------------------------------
    # GRAFICA
    # ------------------------------
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=q, y=p, mode="lines", name="Demanda"))

    fig.update_layout(
        xaxis_title="Cantidad (Q)",
        yaxis_title="Precio (P)",
        title=f"Curva de Demanda – Elasticidad calculada: {E:.2f}",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # ------------------------------
    # EXPLICACIÓN
    # ------------------------------
    st.subheader("Explicación económica")

    if E > 1:
        st.success("**Demanda elástica (>1):** una pequeña variación en el precio genera un cambio proporcionalmente mayor en la cantidad. La curva es más plana.")
    elif E < 1:
        st.info("**Demanda inelástica (<1):** la cantidad cambia poco frente a variaciones en precio. La curva es empinada.")
    else:
        st.warning("**Elasticidad unitaria (=1):** el cambio porcentual en cantidad es igual al cambio porcentual en precio.")

    st.write("""
    **Interpretación:**  
    - El intercepto *a* y la pendiente *b* cambian la forma básica de la curva.  
    - El parámetro de **elasticidad** ajusta cuán sensible es la cantidad ante cambios en el precio.  
    - La gráfica se actualiza en tiempo real mostrando estos efectos.
    """)

# ------------------------------
# TAB 2: ELASTICIDAD INGRESO
# ------------------------------
with tab2:
    st.header("Elasticidad Ingreso")

    col1, col2 = st.columns(2)
    with col1:
        m = st.slider("Ingreso del consumidor (M)", 100, 2000, 800)
        y = st.slider("Sensibilidad del bien al ingreso (k)", -3.0, 3.0, 1.0, 0.1)

    precios = np.linspace(1, 50, 200)
    cantidades = (m / precios) ** y

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=precios, y=cantidades, mode="lines", name="Curva ingreso"))

    fig2.update_layout(
        xaxis_title="Precio",
        yaxis_title="Cantidad demandada",
        title="Elasticidad Ingreso",
        height=500
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Explicación económica")

    if y > 0:
        st.success("**Bien normal:** cuando aumenta el ingreso, aumenta la demanda.")
    elif y < 0:
        st.error("**Bien inferior:** cuando sube el ingreso, la demanda cae.")
    else:
        st.info("**Elasticidad cero:** la demanda no depende del ingreso.")

    st.write("""
    **Interpretación:**  
    - La elasticidad ingreso determina si el bien es normal o inferior.  
    - La gráfica muestra cómo cambia la cantidad demandada cuando el ingreso varía.  
    """)

