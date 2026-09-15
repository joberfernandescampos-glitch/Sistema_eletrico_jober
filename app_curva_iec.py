import cmath
import math
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Configuração global da página
st.set_page_config(
    page_title="Portal Elétrico - Jóber Fernandes", layout="centered"
)

# --- TÍTULO DO PORTAL ---
st.title("⚡ JÓBER FERNANDES - PORTAL DE ENGENHARIA")

# --- MENU DE SELEÇÃO UNIFICADO ---
modulo = st.selectbox(
    "Selecione a Ferramenta que deseja utilizar:",
    [
        "Página Inicial / Informações",
        "1. Componentes Simétricas",
        "2. Curvas IEC (Proteção)",
        "3. Cálculo de Tensões",
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

    * **Componentes Simétricas:** Análise fasorial e cálculo de sequências (Zero, Positiva e Negativa).
    * **Curvas IEC:** Dimensionamento e simulação de tempos de atuação de relés de proteção.
    * **Cálculo de Tensões:** Análise de regulação e queda de tensão em circuitos de distribuição.
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
        st.markdown("**Corrente Ia**")
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
        st.markdown("**Corrente Ib**")
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
        st.markdown("**Corrente Ic**")
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

