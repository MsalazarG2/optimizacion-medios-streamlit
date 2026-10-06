import streamlit as st
import pandas as pd
import pulp
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Optimización de Medios",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Optimización de Medios Publicitarios")
st.write(
    "Selecciona los canales publicitarios que maximicen el impacto "
    "sin superar el presupuesto disponible."
)

st.sidebar.header("⚙️ Configuración")

presupuesto = st.sidebar.number_input(
    "Presupuesto disponible",
    min_value=0.0,
    value=9.0,
    step=1.0
)

st.sidebar.info(
    "Puedes modificar el presupuesto, los costos y los impactos. "
    "Luego presiona 'Optimizar'."
)

datos_iniciales = pd.DataFrame({
    "Canal": ["TV", "Radio", "Redes sociales", "Prensa"],
    "Costo": [8.0, 3.0, 4.0, 2.0],
    "Impacto": [14.0, 5.0, 7.0, 3.0]
})

st.subheader("📋 Canales publicitarios")

datos = st.data_editor(
    datos_iniciales,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Canal": st.column_config.TextColumn("Canal"),
        "Costo": st.column_config.NumberColumn(
            "Costo", min_value=0.0, step=1.0
        ),
        "Impacto": st.column_config.NumberColumn(
            "Impacto", min_value=0.0, step=1.0
        )
    },
    hide_index=True
)

if st.button("🚀 Optimizar", type="primary", use_container_width=True):

    if datos.empty:
        st.error("Debes agregar al menos un canal.")
        st.stop()

    if datos["Canal"].astype(str).str.strip().eq("").any():
        st.error("Todos los canales deben tener un nombre.")
        st.stop()

    if (datos["Costo"] < 0).any() or (datos["Impacto"] < 0).any():
        st.error("Los costos e impactos no pueden ser negativos.")
        st.stop()

    # Modelo de maximización
    modelo = pulp.LpProblem(
        "Optimizacion_Medios",
        pulp.LpMaximize
    )

    # PuLP 4.x: las variables se crean desde el problema
    variables = {}

    for i in datos.index:
        variables[i] = modelo.add_variable(
            name=f"x_{i}",
            cat="Binary"
        )

    # Función objetivo
    modelo += pulp.lpSum(
        datos.loc[i, "Impacto"] * variables[i]
        for i in datos.index
    )

    # Restricción de presupuesto
    modelo += (
        pulp.lpSum(
            datos.loc[i, "Costo"] * variables[i]
            for i in datos.index
        )
        <= presupuesto
    )

    # Resolver
    modelo.solve(pulp.PULP_CBC_CMD(msg=False))

    estado = pulp.LpStatus[modelo.status]

    if estado != "Optimal":
        st.error(f"No se encontró una solución óptima. Estado: {estado}")
        st.stop()

    # Resultados
    seleccion = [
        1 if pulp.value(variables[i]) == 1 else 0
        for i in datos.index
    ]

    datos_resultado = datos.copy()
    datos_resultado["Seleccionado"] = [
        "✅ Sí" if valor == 1 else "❌ No"
        for valor in seleccion
    ]

    datos_resultado["Costo seleccionado"] = [
        datos.loc[i, "Costo"] if seleccion[pos] == 1 else 0
        for pos, i in enumerate(datos.index)
    ]

    datos_resultado["Impacto obtenido"] = [
        datos.loc[i, "Impacto"] if seleccion[pos] == 1 else 0
        for pos, i in enumerate(datos.index)
    ]

    costo_total = datos_resultado["Costo seleccionado"].sum()
    impacto_total = datos_resultado["Impacto obtenido"].sum()

    st.subheader("🏆 Solución óptima")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("💰 Presupuesto", f"{presupuesto:.2f}")

    with col2:
        st.metric("💵 Costo utilizado", f"{costo_total:.2f}")

    with col3:
        st.metric("📈 Impacto máximo", f"{impacto_total:.2f}")

    st.success(
        f"La solución óptima utiliza {costo_total:.2f} "
        f"de presupuesto y obtiene un impacto de {impacto_total:.2f}."
    )

    st.dataframe(
        datos_resultado,
        use_container_width=True,
        hide_index=True
    )

    seleccionados = datos_resultado[
        datos_resultado["Seleccionado"] == "✅ Sí"
    ]

    if not seleccionados.empty:
        st.subheader("📌 Canales seleccionados")

        for _, fila in seleccionados.iterrows():
            st.write(
                f"**{fila['Canal']}** — "
                f"Costo: {fila['Costo']:.2f} | "
                f"Impacto: {fila['Impacto']:.2f}"
            )

    st.subheader("📊 Comparación de impacto")

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.bar(datos["Canal"], datos["Impacto"])
    ax.set_xlabel("Canal")
    ax.set_ylabel("Impacto")
    ax.set_title("Impacto por canal publicitario")
    plt.xticks(rotation=20)
    plt.tight_layout()
    st.pyplot(fig)

else:
    st.info(
        "Modifica los datos si quieres y presiona "
        "**🚀 Optimizar** para calcular la solución."
    )

with st.expander("📚 Ver modelo matemático"):
    st.markdown("""
    ### Variables de decisión

    Para cada canal:

    **xᵢ ∈ {0, 1}**

    - `1` = utilizar el canal.
    - `0` = no utilizarlo.

    ### Función objetivo

    **Max Z = Σ (impactoᵢ × xᵢ)**

    ### Restricción

    **Σ (costoᵢ × xᵢ) ≤ presupuesto**

    El problema es de programación lineal entera binaria
    y se resuelve utilizando **PuLP**.
    """)

