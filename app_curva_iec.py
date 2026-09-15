import cmath
import math
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Configuração global da página (Ajustada para layout "wide" do seu script)
st.set_page_config(
    page_title="Portal Elétrico - Jóber Fernandes",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Estilização CSS unificada para forçar o tema Dark e ajustar blocos
st.markdown(
    """
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    div[data-testid="stBlock"] {
        background-color: #161b22;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    h1, h2, h3, h4, h5 { color: #ffffff !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- MENU DE SELEÇÃO UNIFICADO ---
st.markdown("# ⚡ JÓBER FERNANDES - PORTAL DE ENGENHARIA")
modulo = st.selectbox(
    "Selecione a Ferramenta que deseja utilizar:",
    [
        "Página Inicial / Informações",
        "1. Componentes Simétricas",
        "2. Curvas IEC (Proteção)",
        "3. Calculadora de Tensões",
    ],
)

st.markdown("---")

# =========================================================================
# PÁGINA INICIAL / BOAS-VINDAS
# =========================================================================
if modulo == "Página Inicial / Informações":
    st.subheader("Bem-vindo ao seu ecossistema de ferramentas técnicas!")
    st.markdown("""
    Esta plataforma unifica suas principais ferramentas de cálculo e análise elétrica. 
    Use a **caixa de seleção acima** para navegar e alterar o módulo ativo na tela:

    * **1. Componentes Simétricas:** Análise fasorial e cálculo de sequências (Zero, Positiva e Negativa).
    * **2. Curvas IEC:** Dimensionamento e simulação de tempos de atuação de relés de proteção.
    * **3. Calculadora de Tensões:** Entrada de fasores monofásicos e plotagem polar de tensões de fase e linha.
    """)
    st.info(
        "💡 Se você estiver acessando pelo celular, basta tocar na caixa de seleção no topo para alternar entre as ferramentas de forma rápida!"
    )

# =========================================================================
# MODULO 1: COMPONENTES SIMÉTRICAS
# =========================================================================
elif modulo == "1. Componentes Simétricas":
    st.subheader("⚙️ Módulo de Componentes Simétricas")

    col_in1, col_in2, col_in3 = st.columns(3)

    with col_in1:
        st.markdown("### Corrente Ia")
        mod_a = st.number_input(
            "Módulo Ia (A):",
            min_value=0.0,
            value=210.0,
            step=5.0,
            key="mod_a",
        )
        ang_a = st.number_input(
            "Ângulo Ia (°):",
            min_value=-360.0,
            max_value=360.0,
            value=0.0,
            step=5.0,
            key="ang_a",
        )

    with col_in2:
        st.markdown("### Corrente Ib")
        mod_b = st.number_input(
            "Módulo Ib (A):", min_value=0.0, value=52.0, step=5.0, key="mod_b"
        )
        ang_b = st.number_input(
            "Ângulo Ib (°):",
            min_value=-360.0,
            max_value=360.0,
            value=240.0,
            step=5.0,
            key="ang_b",
        )

    with col_in3:
        st.markdown("### Corrente Ic")
        mod_c = st.number_input(
            "Módulo Ic (A):", min_value=0.0, value=65.0, step=5.0, key="mod_c"
        )
        ang_c = st.number_input(
            "Ângulo Ic (°):",
            min_value=-360.0,
            max_value=360.0,
            value=120.0,
            step=5.0,
            key="ang_c",
        )

    def ajustar_angulo(ang):
        while ang > 180:
            ang -= 360
        while ang <= -180:
            ang += 360
        return ang

    Ia = cmath.rect(mod_a, math.radians(ang_a))
    Ib = cmath.rect(mod_b, math.radians(ang_b))
    Ic = cmath.rect(mod_c, math.radians(ang_c))

    In = Ia + Ib + Ic
    mod_In, ang_In = cmath.polar(In)

    a = cmath.rect(1, math.radians(120))
    a2 = cmath.rect(1, math.radians(240))

    I0 = In / 3
    mod_I0, ang_I0 = cmath.polar(I0)
    I1 = (Ia + (a * Ib) + (a2 * Ic)) / 3
    mod_I1, ang_I1 = cmath.polar(I1)
    I2 = (Ia + (a2 * Ib) + (a * Ic)) / 3
    mod_I2, ang_I2 = cmath.polar(I2)

    resultado_texto = (
        "--- Correntes de Fase (Entrada) ---\n"
        f"Ia = {mod_a:.4f} |_ {ajustar_angulo(ang_a):.2f}° A\n"
        f"Ib = {mod_b:.4f} |_ {ajustar_angulo(ang_b):.2f}° A\n"
        f"Ic = {mod_c:.4f} |_ {ajustar_angulo(ang_c):.2f}° A\n\n"
        "--- Componentes de Sequência ---\n"
        f"I0 = {mod_I0:.4f} |_ {ajustar_angulo(math.degrees(ang_I0)):.2f}° A\n"
        f"I1 = {mod_I1:.4f} |_ {ajustar_angulo(math.degrees(ang_I1)):.2f}° A\n"
        f"I2 = {mod_I2:.4f} |_ {ajustar_angulo(math.degrees(ang_I2)):.2f}° A\n\n"
        "--- Corrente de Neutro ---\n"
        f"In = {mod_In:.4f} |_ {ajustar_angulo(math.degrees(ang_In)):.2f}° A\n"
    )

    st.text_area(
        label="Console de Resultados:",
        value=resultado_texto,
        height=260,
        disabled=True,
    )

    st.write("### 📈 Diagramas Fasoriais")
    col_g1, col_g2 = st.columns(2)

    def plotar_fasor(ax, complexo, label, cor):
        ax.quiver(
            0,
            0,
            complexo.real,
            complexo.imag,
            angles="xy",
            scale_units="xy",
            scale=1,
            color=cor,
            label=label,
            width=0.015,
        )

    limite_grafico = (
        max(mod_a, mod_b, mod_c, mod_In, mod_I0, mod_I1, mod_I2, 1) * 1.2
    )

    with col_g1:
        st.write("**Fase e Neutro**")
        fig1, ax1 = plt.subplots(figsize=(4, 4))
        plotar_fasor(ax1, Ia, "Ia", "blue")
        plotar_fasor(ax1, Ib, "Ib", "green")
        plotar_fasor(ax1, Ic, "Ic", "orange")
        plotar_fasor(ax1, In, "In", "red")
        ax1.set_xlim(-limite_grafico, limite_grafico)
        ax1.set_ylim(-limite_grafico, limite_grafico)
        ax1.axhline(0, color="black", linewidth=0.5, linestyle="--")
        ax1.axvline(0, color="black", linewidth=0.5, linestyle="--")
        ax1.grid(True, which="both", linestyle=":", alpha=0.5)
        ax1.set_aspect("equal")
        ax1.legend(loc="upper right")
        st.pyplot(fig1)

    with col_g2:
        st.write("**Componentes de Sequência**")
        fig2, ax2 = plt.subplots(figsize=(4, 4))
        plotar_fasor(ax2, I0, "I0 (Zero)", "purple")
        plotar_fasor(ax2, I1, "I1 (Pos)", "brown")
        plotar_fasor(ax2, I2, "I2 (Neg)", "magenta")
        ax2.set_xlim(-limite_grafico, limite_grafico)
        ax2.set_ylim(-limite_grafico, limite_grafico)
        ax2.axhline(0, color="black", linewidth=0.5, linestyle="--")
        ax2.axvline(0, color="black", linewidth=0.5, linestyle="--")
        ax2.grid(True, which="both", linestyle=":", alpha=0.5)
        ax2.set_aspect("equal")
        ax2.legend(loc="upper right")
        st.pyplot(fig2)

# =========================================================================
# MODULO 2: CURVAS IEC
# =========================================================================
elif modulo == "2. Curvas IEC (Proteção)":
    st.subheader("⚙️ Módulo de Curvas IEC (Proteção)")

    CURVAS_IEC = {
        "IEC Normal Inversa (NI)": (0.14, 0.02),
        "IEC Muito Inversa (MI)": (13.5, 1.0),
        "IEC Extremamente Inversa (EI)": (80.0, 2.0),
        "IEC Longo Tempo Inversa (LTI)": (120.0, 1.0),
    }

    col_iec1, col_iec2 = st.columns(2)
    with col_iec1:
        curva_selecionada = st.selectbox(
            "Selecione a Curva IEC:", list(CURVAS_IEC.keys())
        )
        k, alpha = CURVAS_IEC[curva_selecionada]
        dial = st.number_input(
            "Dial de Tempo (TMS):",
            min_value=0.01,
            max_value=10.0,
            value=0.1,
            step=0.05,
        )

    with col_iec2:
        i_falta = st.number_input(
            "Corrente de Falta (I) [A]:",
            min_value=0.1,
            value=150.0,
            step=10.0,
        )
        i_partida = st.number_input(
            "Corrente de Partida/Pick-up (I_p) [A]:",
            min_value=0.1,
            value=50.0,
            step=5.0,
        )

    multiplo_i = i_falta / i_partida

    if multiplo_i <= 1.0:
        st.error(
            f"A corrente de falta ({i_falta}A) é menor ou igual à partida ({i_partida}A). O relé não opera."
        )
        tempo_operacao = None
    else:
        tempo_operacao = dial * (k / (multiplo_i**alpha - 1))

        c1, c2, c3 = st.columns(3)
        c1.metric("Múltiplo M", f"{multiplo_i:.2f} x")
        c2.metric("Tempo (t)", f"{tempo_operacao:.3f} s")
        c3.metric("Constantes", f"k={k}, α={alpha}")

    st.write("### 📈 Gráfico da Curva Característica")
    m_valores = np.linspace(1.1, 20.0, 500)
    tempos_curva = dial * (k / (m_valores**alpha - 1))

    fig3, ax3 = plt.subplots(figsize=(7, 4))
    ax3.plot(
        m_valores,
        tempos_curva,
        label=f"Curva {curva_selecionada}",
        color="blue",
        linewidth=2,
    )

    if tempo_operacao is not None and multiplo_i <= 20.0:
        ax3.scatter(
            [multiplo_i],
            [tempo_operacao],
            color="red",
            s=100,
            zorder=5,
            label="Ponto de Operação",
        )
        ax3.axhline(y=tempo_operacao, color="red", linestyle="--", alpha=0.4)
        ax3.axvline(x=multiplo_i, color="red", linestyle="--", alpha=0.4)

    ax3.set_yscale("log")
    ax3.set_xlabel("Múltiplo da Corrente (I / I_p)")
    ax3.set_ylabel("Tempo (s) - Escala Log")
    ax3.grid(True, which="both", linestyle=":", alpha=0.5)
    ax3.legend()
    st.pyplot(fig3)
# =========================================================================
# MODULO 3: CALCULADORA DE TENSÕES (CÓDIGO POLAR ENVIADO)
# =========================================================================
elif modulo == "3. Calculadora de Tensões":
    st.markdown(
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuração da página (Tema Escuro e Layout Amplo)
st.set_page_config(
    page_title="Componentes de Tensão", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Estilização CSS para forçar o tema Dark e ajustar os cards
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    div[data-testid="stBlock"] {
        background-color: #161b22;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    h1, h2, h3, h4, h5 { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- TÍTULO PRINCIPAL ---
st.markdown("# ⚡ JÓBER FERNANDES - CALCULADORA DE TENSÕES")
st.markdown("<p style='color: #8b949e;'>Insira os valores das tensões monofásicas de fase para calcular e plotar as tensões de linha correspondentes.</p>", unsafe_allow_html=True)

# --- 1. ENTRADA DE DADOS EM COLUNAS (Fase A, B e C) ---
col_A, col_B, col_C = st.columns(3)

with col_A:
    st.markdown("### Fase A")
    vA_mag = st.number_input("Va - Módulo (V)", value=127.0, step=1.0, format="%.2f", key="vA_m")
    vA_ang = st.number_input("Va - Ângulo (°)", value=0.0, step=1.0, format="%.2f", key="vA_a")

with col_B:
    st.markdown("### Fase B")
    vB_mag = st.number_input("Vb - Módulo (V)", value=127.0, step=1.0, format="%.2f", key="vB_m")
    vB_ang = st.number_input("Vb - Ângulo (°)", value=-120.0, step=1.0, format="%.2f", key="vB_a")

with col_C:
    st.markdown("### Fase C")
    vC_mag = st.number_input("Vc - Módulo (V)", value=127.0, step=1.0, format="%.2f", key="vC_m")
    vC_ang = st.number_input("Vc - Ângulo (°)", value=120.0, step=1.0, format="%.2f", key="vC_a")

# --- 2. PROCESSAMENTO MATEMÁTICO ---
V_A = vA_mag * np.exp(1j * np.radians(vA_ang))
V_B = vB_mag * np.exp(1j * np.radians(vB_ang))
V_C = vC_mag * np.exp(1j * np.radians(vC_ang))

# Tensões de linha (Fase-Fase)
V_AB = V_A - V_B
V_BC = V_B - V_C
V_CA = V_C - V_A

# Funções auxiliares para formatar strings de exibição
def format_fasor(v_complex):
    mag = np.abs(v_complex)
    ang = np.degrees(np.angle(v_complex))
    return f"{mag:.4f}  |  {ang:.2f}°  V"

# --- 3. LAYOUT INFERIOR (Resultados à esquerda, Gráficos à direita) ---
col_res, col_graf = st.columns([1, 2])

with col_res:
    st.markdown("### 📋 Resultados")
    
    st.markdown("**Tensões de Fase (Entrada):**")
    st.markdown(f"<span style='color:#ff4b4b;'>**Va :**</span> {format_fasor(V_A)}", unsafe_allow_html=True)
    st.markdown(f"<span style='color:#00cc96;'>**Vb :**</span> {format_fasor(V_B)}", unsafe_allow_html=True)
    st.markdown(f"<span style='color:#636efa;'>**Vc :**</span> {format_fasor(V_C)}", unsafe_allow_html=True)
    
    st.markdown("<br>**Tensões de Linha (Calculadas):**", unsafe_allow_html=True)
    st.markdown(f"<span style='color:#ef553b;'>**Vab :**</span> {format_fasor(V_AB)}", unsafe_allow_html=True)
    st.markdown(f"<span style='color:#00cc96;'>**Vbc :**</span> {format_fasor(V_BC)}", unsafe_allow_html=True)
    st.markdown(f"<span style='color:#ab63fa;'>**Vca :**</span> {format_fasor(V_CA)}", unsafe_allow_html=True)

with col_graf:
    st.markdown("### 📈 Gráficos dos Fasores")
    
    # Criando os subplots polares lado a lado usando Plotly
    fig = go.Figure()
    
    # Gráfico 1: TENSÕES DE FASE (Subplot Polar 1)
    fig.add_trace(go.Scatterpolar(r=[0, np.abs(V_A)], theta=[0, np.degrees(np.angle(V_A))], mode='lines+markers', name='Va (Fase)', line=dict(color='#ff4b4b', width=3), subplot='polar1'))
    fig.add_trace(go.Scatterpolar(r=[0, np.abs(V_B)], theta=[0, np.degrees(np.angle(V_B))], mode='lines+markers', name='Vb (Fase)', line=dict(color='#00cc96', width=3), subplot='polar1'))
    fig.add_trace(go.Scatterpolar(r=[0, np.abs(V_C)], theta=[0, np.degrees(np.angle(V_C))], mode='lines+markers', name='Vc (Fase)', line=dict(color='#636efa', width=3), subplot='polar1'))
    
    # Gráfico 2: TENSÕES DE LINHA (Subplot Polar 2)
    fig.add_trace(go.Scatterpolar(r=[0, np.abs(V_AB)], theta=[0, np.degrees(np.angle(V_AB))], mode='lines+markers', name='Vab (Linha)', line=dict(color='#ef553b', width=2.5, dash='dash'), subplot='polar2'))
    fig.add_trace(go.Scatterpolar(r=[0, np.abs(V_BC)], theta=[0, np.degrees(np.angle(V_BC))], mode='lines+markers', name='Vbc (Linha)', line=dict(color='#00cc96', width=2.5, dash='dash'), subplot='polar2'))
    fig.add_trace(go.Scatterpolar(r=[0, np.abs(V_CA)], theta=[0, np.degrees(np.angle(V_CA))], mode='lines+markers', name='Vca (Linha)', line=dict(color='#ab63fa', width=2.5, dash='dash'), subplot='polar2'))
    
    # Configurações do layout escuro dos gráficos polares
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#161b22",
        plot_bgcolor="#161b22",
        margin=dict(l=20, r=20, t=40, b=20),
        grid=dict(rows=1, columns=2, pattern='independent'),
        polar1=dict(domain=dict(x=[0, 0.45]), angularaxis=dict(direction="counterclockwise", period=360)),
        polar2=dict(domain=dict(x=[0.55, 1]), angularaxis=dict(direction="counterclockwise", period=360)),
        title=dict(text="Fases (Va, Vb, Vc)                       |                       Linha (Vab, Vbc, Vca)", x=0.05, y=0.95),
        legend=dict(orientation="h", y=-0.1, x=0.05)
    )
    
    st.plotly_chart(fig, use_container_width=True)

