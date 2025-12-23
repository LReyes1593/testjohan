import pandas as pd
import streamlit as st
from PIL import Image
import altair as alt

logo = Image.open("logo.jpg")

# Cargar CSV y seleccionar columnas de interés
df = pd.read_csv('Employee_data.csv')
columnas = ['name_employee', 'birth_date', 'age', 'gender', 'marital_status',
            'hiring_date', 'position', 'salary', 'performance_score',
            'last_performance_date', 'average_work_hours', 'satisfaction_level',
            'absences']
df = df[columnas]

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Desempeño - Socialize Your Knowledge",
    layout="wide"
)

# ------------------------------------------------------------------
# Código que contiene el título y la breve descripción de la APP web
# ------------------------------------------------------------------
col1, col2 = st.columns([4, 1])
with col1:
    st.title("Análisis de Desempeño de los Colaboradores")
    st.markdown(
        """
        Esta aplicación web te permitirá visualizar y analizar métricas clave sobre el rendimiento de los colaboradores.  
        Utiliza las herramientas de visualización y filtros disponibles para explorar los datos en detalle.
        """
    )
# ------------------------------------------------------------------
# Código que permite desplegar el logotipo de la empresa
# ------------------------------------------------------------------
with col2:
    st.image(logo, width=160)


# SIDEBAR: Filtros interactivos
st.sidebar.markdown("## Filtros")
st.sidebar.markdown("---")

# ------------------------------------------------------------------
# Código que permite desplegar un control para seleccionar el género
# ------------------------------------------------------------------
genero_seleccionado = st.sidebar.selectbox(
    "Selecciona el género de los empleados:", ["Todos", "Masculino", "Femenino"]
)
df_filtrado = df.copy()
if genero_seleccionado == "Masculino":
    df_filtrado = df_filtrado[df_filtrado['gender'].str.strip() == "M"]
elif genero_seleccionado == "Femenino":
    df_filtrado = df_filtrado[df_filtrado['gender'].str.strip() == "F"]

st.sidebar.write(f"**Mostrando empleados de género:** {genero_seleccionado}")
st.sidebar.markdown("---")

# ------------------------------------------------------------------
# Código que permite desplegar un control para seleccionar el rango de puntaje
# ------------------------------------------------------------------
rango_desempeño = st.sidebar.slider(
    "Selecciona el rango de puntaje de desempeño:",
    min_value=0.0,
    max_value=5.0,
    value=(0.0, 5.0),
    step=0.1
)
df_filtrado = df_filtrado[(df_filtrado['performance_score'] >= rango_desempeño[0]) & (df_filtrado['performance_score'] <= rango_desempeño[1])]
st.sidebar.write(f"**Mostrando empleados con puntaje de desempeño entre:** {rango_desempeño[0]} y {rango_desempeño[1]}")
st.sidebar.markdown("---")

# ------------------------------------------------------------------
# Código que permite desplegar un control para seleccionar el estado civil
# ------------------------------------------------------------------
estados_civiles = list(df['marital_status'].unique())
estados_civil_seleccionados = st.sidebar.multiselect(
    "Selecciona el estado civil de los empleados:",
    opciones := estados_civiles,
    default=[]
)
if estados_civil_seleccionados:
    df_filtrado = df_filtrado[df_filtrado['marital_status'].isin(estados_civil_seleccionados)]
st.sidebar.write(f"**Estados civiles seleccionados:** {', '.join(estados_civil_seleccionados) if estados_civil_seleccionados else 'Todos'}")
st.sidebar.markdown("---")

# ------------------------------------------------------------------
# Código que permite desplegar un resumén de filtros
# ------------------------------------------------------------------
st.markdown("### Resumen de la Selección Actual")
colA, colB, colC = st.columns(3)
colA.metric("Total de empleados", f"{len(df_filtrado)}")
colB.metric("Promedio de desempeño", f"{df_filtrado['performance_score'].mean():.2f}" if not df_filtrado.empty else "—")
colC.metric("Promedio de horas trabajadas", f"{df_filtrado['average_work_hours'].mean():,.2f}" if not df_filtrado.empty else "—")

# ------------------------------------------------------------------
# Código que permite mostrar gráfico de distribución de puntajes de desempeño
# ------------------------------------------------------------------
hist = alt.Chart(df_filtrado).mark_bar(color='steelblue').encode(
    alt.X('performance_score', bin=alt.Bin(step=0.5), title='Puntaje de Desempeño'),
    alt.Y('count()', title="Cantidad de empleados")
).properties(
    title='Distribución de Puntajes de Desempeño'
)
st.altair_chart(hist, use_container_width=True)

# ------------------------------------------------------------------
# Código que permite mostrar gráfico de promedio de horas trabajadas por género
# ------------------------------------------------------------------
grafico_promedio_horas = alt.Chart(df_filtrado).mark_bar().encode(
    alt.X('gender:N', title='Género'),
    alt.Y('average_work_hours:Q', aggregate='mean', title='Promedio de horas trabajadas'),
    color='gender:N',
    tooltip=[alt.Tooltip('gender:N', title='Género'),
             alt.Tooltip('average_work_hours:Q', aggregate='mean', title='Promedio de horas')]
).properties(
    title="Promedio de Horas Trabajadas por Género"
)
st.altair_chart(grafico_promedio_horas, use_container_width=True)

# ------------------------------------------------------------------
# Código que permite mostrar gráfico de edad vs salario
# ------------------------------------------------------------------
if not df_filtrado.empty:
    grafico_edad_salario = alt.Chart(df_filtrado).mark_point().encode(
        x=alt.X('age:Q', title="Edad"),
        y=alt.Y('salary:Q', title="Salario"),
        color=alt.Color('gender:N', legend=alt.Legend(title="Género")),
        tooltip=['name_employee', 'age', 'salary']
    ).properties(
        title="Relación entre Edad y Salario de los Empleados"
    )
    st.altair_chart(grafico_edad_salario, use_container_width=True)
else:
    st.warning("No hay datos para mostrar la relación entre edad y salario en la selección actual.")

# ------------------------------------------------------------------
# Código que permite mostrar gráfico de horas trabajadas vs puntaje de desempeño
# ------------------------------------------------------------------
if not df_filtrado.empty:
    scatter_plot = alt.Chart(df_filtrado).mark_point().encode(
        x=alt.X('average_work_hours', title='Promedio de horas trabajadas'),
        y=alt.Y('performance_score', title='Puntaje de desempeño'),
        color=alt.Color('gender:N', legend=alt.Legend(title="Género")),
        tooltip=['name_employee', 'average_work_hours', 'performance_score']
    ).properties(
        width=600,
        height=400,
        title="Relación entre Promedio de Horas Trabajadas y Puntaje de Desempeño"
    )
    st.altair_chart(scatter_plot, use_container_width=True)
else:
    st.warning("No hay datos para mostrar la relación entre horas y desempeño en la selección actual.")

# ------------------------------------------------------------------
# Código que permite desplegar una conclusión sobre el análisis
# ------------------------------------------------------------------
st.markdown("---")
st.subheader("Conclusión")
st.markdown(
    """
    A partir del análisis realizado, se pueden observar tendencias importantes relacionadas con el desempeño de los colaboradores.  
    El rango de puntajes de desempeño y su relación con el promedio de horas trabajadas muestra posibles áreas de mejora o refuerzo.  
    Además, se detectan variaciones por género y estado civil que podrían ser consideradas para estrategias de gestión del talento.  
    Esta herramienta permite explorar los datos de manera interactiva para apoyar la toma de decisiones en la empresa **Socialize Your Knowledge**.
    """
)
