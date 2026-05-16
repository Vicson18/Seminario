import streamlit as st
import time

# Configuración profesional - Equipo FIME
st.set_page_config(page_title="Planificador FIME - PRO", layout="wide")

# Inicializar estados de sesión para el cronómetro
if 'recomendacion_generada' not in st.session_state:
    st.session_state.recomendacion_generada = False
if 'ganadora' not in st.session_state:
    st.session_state.ganadora = ""
if 'score_ganador' not in st.session_state:
    st.session_state.score_ganador = 0

# Estilos visuales
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #0e1117; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar - Créditos del Equipo
st.sidebar.image("https://www.fime.uanl.mx/wp-content/uploads/2022/03/logo-fime.png", width=150)
st.sidebar.markdown("### 🎓 Equipo de Trabajo")
st.sidebar.write("- Víctor Alejandro Cruz Moreno")
st.sidebar.write("- Omar Azael Lozano Escobar")
st.sidebar.write("- Vicente Reyes De Luna")
st.sidebar.markdown("---")
st.sidebar.write("**Grupo:** 003 | **Carrera:** IAS")

# --- FUNCIÓN DE LÓGICA AVANZADA ---
def calcular_prioridad(minutos, dias, importancia):
    # Evitamos división por cero si ponen 0 días (entrega hoy)
    dias_ajustados = max(dias, 0.5) 
    # FÓRMULA: (Importancia / Días) + (Minutos / 60)
    # Entre menos días y más importancia, el score sube drásticamente.
    score = (importancia / dias_ajustados) + (minutos / 480) 
    return round(score, 2)

st.title("🚀 Sistema de Priorización Inteligente")
st.write("Algoritmo avanzado para la gestión de carga académica y reducción de estrés.")

# 1. Entrada de Datos
st.header("1. Parámetros de Tareas")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Tarea A")
    nom_a = st.text_input("Nombre de Tarea A", "Seminario", key="na")
    imp_a = st.slider("Nivel de Importancia (1-10)", 1, 10, 8, key="ia")
    dias_a = st.number_input("Días para la entrega (A)", min_value=0, value=2, key="da")
    tie_a = st.number_input("Minutos estimados de trabajo (A)", min_value=1, value=120, key="ta")

with col2:
    st.subheader("📝 Tarea B")
    nom_b = st.text_input("Nombre de Tarea B", "Tec. Emergentes", key="nb")
    imp_b = st.slider("Nivel de Importancia (1-10)", 1, 10, 7, key="ib")
    dias_b = st.number_input("Días para la entrega (B)", min_value=0, value=4, key="db")
    tie_b = st.number_input("Minutos estimados de trabajo (B)", min_value=1, value=180, key="tb")

tiempo_disponible = st.number_input("¿Minutos disponibles para trabajar hoy?", min_value=1, value=120)

# 2. Procesamiento
if st.button("📊 CALCULAR PRIORIDAD CIENTÍFICA"):
    score_a = calcular_prioridad(tie_a, dias_a, imp_a)
    score_b = calcular_prioridad(tie_b, dias_b, imp_b)
    
    st.session_state.recomendacion_generada = True
    
    if score_a >= score_b:
        st.session_state.ganadora = nom_a
        st.session_state.score_ganador = score_a
    else:
        st.session_state.ganadora = nom_b
        st.session_state.score_ganador = score_b

# 3. Resultados y Temporizador
if st.session_state.recomendacion_generada:
    st.divider()
    st.success(f"## ✅ Recomendación: Iniciar con **{st.session_state.ganadora}**")
    
    # Barra de color basada en el score (Riesgo)
    st.write(f"#### 📈 Índice de Urgencia Calculado: {st.session_state.score_ganador}")
    # Normalizamos el progreso para la barra (basado en un score máximo esperado de 20)
    progreso_visual = min(st.session_state.score_ganador / 20, 1.0)
    st.progress(progreso_visual)
    
    if progreso_visual > 0.7:
        st.error("🚨 ATENCIÓN: Esta tarea requiere acción inmediata debido al corto plazo.")
    
    # Temporizador Pomodoro
    st.subheader(f"⏲️ Temporizador de Enfoque: {st.session_state.ganadora}")
    if st.button("▶️ EMPEZAR SESIÓN DE 25 MIN"):
        t_placeholder = st.empty()
        p_bar = st.progress(0)
        
        segundos = 25 * 60
        for s in range(segundos, -1, -1):
            m, seg = divmod(s, 60)
            t_placeholder.metric("Tiempo Restante", f"{m:02d}:{seg:02d}")
            p_bar.progress(1, "Enfocado...") # Simulación de progreso
            time.sleep(1)
        
        st.balloons()
        st.success("¡Sesión completada! Descansa 5 minutos.")

st.caption("Desarrollado para la Actividad 6 - Seminario de Sistemas II (FIME).")