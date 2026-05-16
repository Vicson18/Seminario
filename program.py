import streamlit as st
import time

# Configuración de página y créditos del equipo FIME
st.set_page_config(page_title="Planificador FIME - PRO", layout="wide")

# --- DISEÑO VISUAL AVANZADO (CSS CORREGIDO PARA VISIBILIDAD) ---
st.markdown("""
    <style>
    /* Fondo general oscuro */
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1c24 100%);
    }
    
    /* FORZAR COLOR DE LETRA BLANCO EN TODA LA APP */
    .stApp, .stMarkdown, p, label, .stSlider, .stNumberInput label {
        color: #ffffff !important;
    }

    /* Tarjetas de tareas con bordes redondeados */
    [data-testid="stVerticalBlock"] > div:has(div.stSlider) {
        background-color: #262730;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #3e404b;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Ajuste para que los títulos de los sliders se vean claros */
    .stSlider label, .stTextInput label, .stNumberInput label {
        font-weight: bold;
        font-size: 1.1rem;
        color: #00c6ff !important;
    }

    /* Botón estilo Neón/Píldora */
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        height: 3.5em;
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        color: white !important;
        font-weight: bold;
        border: none;
        transition: 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        box-shadow: 0 0 25px rgba(0, 198, 255, 0.7);
        transform: scale(1.01);
    }

    /* Títulos principales en Azul Neón */
    h1, h2, h3, h4 {
        color: #00c6ff !important;
    }
    
    /* Color de los inputs de texto y número */
    .stTextInput input, .stNumberInput input {
        color: #ffffff !important;
        background-color: #1a1c24 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicialización de estados para evitar reinicios del cronómetro
if 'ejecutado' not in st.session_state:
    st.session_state.ejecutado = False
if 'ganadora' not in st.session_state:
    st.session_state.ganadora = ""
if 'score' not in st.session_state:
    st.session_state.score = 0.0

# Sidebar con información del equipo
st.sidebar.image("https://www.fime.uanl.mx/wp-content/uploads/2022/03/logo-fime.png", width=130)
st.sidebar.markdown("### 🎓 Equipo de Trabajo")
st.sidebar.write("- Víctor Alejandro Cruz Moreno")
st.sidebar.write("- Omar Azael Lozano Escobar")
st.sidebar.write("- Vicente Reyes De Luna")
st.sidebar.markdown("---")
st.sidebar.write("**Grupo:** 003 | **Carrera:** IAS")

# --- FUNCIÓN DE LÓGICA DE PRIORIZACIÓN ---
def calcular_indice(minutos, dias, importancia):
    # La urgencia aumenta exponencialmente conforme se acerca la fecha de entrega
    dias_criticos = max(dias, 0.5)
    # Fórmula: (Importancia / Tiempo restante) + Esfuerzo estimado
    score = (importancia / dias_criticos) + (minutos / 480)
    return round(score, 2)

st.title("⚡ Smart Task Prioritizer v3.0")
st.write("Algoritmo de optimización para estudiantes de Ingeniería de la FIME.")

# 1. Entrada de Datos
st.header("📌 Parámetros de Análisis")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔹 Tarea A")
    nom_a = st.text_input("Nombre de la Tarea A", "Seminario", key="na")
    imp_a = st.slider("Importancia Académica (1-10)", 1, 10, 8, key="ia")
    dias_a = st.number_input("Días faltantes (A)", min_value=0, value=2, key="da")
    tie_a = st.number_input("Minutos de trabajo (A)", min_value=1, value=120, key="ta")

with col2:
    st.subheader("🔹 Tarea B")
    nom_b = st.text_input("Nombre de la Tarea B", "Tec. Emergentes", key="nb")
    imp_b = st.slider("Importancia Académica (1-10)", 1, 10, 7, key="ib")
    dias_b = st.number_input("Días faltantes (B)", min_value=0, value=4, key="db")
    tie_b = st.number_input("Minutos de trabajo (B)", min_value=1, value=180, key="tb")

tiempo_disponible = st.number_input("¿Minutos disponibles hoy?", min_value=1, value=120)

# 2. Ejecución del Algoritmo
st.markdown("---")
if st.button("🔍 ANALIZAR Y DETERMINAR PRIORIDAD"):
    score_a = calcular_indice(tie_a, dias_a, imp_a)
    score_b = calcular_indice(tie_b, dias_b, imp_b)
    
    st.session_state.ejecutado = True
    
    if score_a >= score_b:
        st.session_state.ganadora, st.session_state.score = nom_a, score_a
    else:
        st.session_state.ganadora, st.session_state.score = nom_b, score_b

# 3. Despliegue de Resultados y Herramientas
if st.session_state.ejecutado:
    st.markdown(f"""
        <div style="background-color: #1e2129; padding: 30px; border-radius: 25px; border-left: 10px solid #00c6ff; margin-top: 20px; border-right: 1px solid #3e404b; border-bottom: 1px solid #3e404b;">
            <h2 style="margin:0; color:#00c6ff;">🎯 Recomendación: {st.session_state.ganadora}</h2>
            <p style="color:#ffffff; opacity: 0.8;">Prioridad calculada mediante análisis de esfuerzo vs. tiempo de entrega.</p>
        </div>
        """, unsafe_allow_html=True)
    
    res_col1, res_col2 = st.columns([2, 1])
    
    with res_col1:
        st.write(f"#### 🔥 Índice de Urgencia: {st.session_state.score}")
        progreso_visual = min(st.session_state.score / 20, 1.0)
        st.progress(progreso_visual)
        
        if progreso_visual > 0.75:
            st.error("🚨 ALERTA: Plazo crítico detectado. Iniciar de inmediato.")
        elif progreso_visual > 0.4:
            st.warning("⚠️ Atención: Tarea en zona de riesgo. No postergar.")
        else:
            st.info("✅ Estado: Tarea bajo control.")

    with res_col2:
        st.subheader("⏲️ Modo Enfoque")
        if st.button("▶️ INICIAR POMODORO (25 MIN)"):
            placeholder = st.empty()
            p_bar = st.progress(0)
            
            total_segundos = 25 * 60
            for s in range(total_segundos, -1, -1):
                m, seg = divmod(s, 60)
                placeholder.metric("Tiempo Restante", f"{m:02d}:{seg:02d}")
                p_bar.progress(100 - int((s / total_segundos) * 100))
                time.sleep(1)
            
            st.balloons()
            st.success("¡Sesión completada!")

st.caption("FIME | Seminario de Sistemas II | Grupo 003")