import streamlit as st
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from rdflib import Graph
import pandas as pd

# --- Streamlit UI Setup ---
current_dir = os.path.dirname(__file__)
logo_path = os.path.join(current_dir, "logo4.png")
uni_path = os.path.join(current_dir, "calculator_logo.png")

if "other" not in st.session_state:
    st.session_state.other = False



st.set_page_config(
    page_title="Critical Velocity Calculator",        
    page_icon= logo_path,                  
    layout="centered",                   
    initial_sidebar_state="expanded",
    menu_items = {'About': 'This is a tool desined and provided by ## University of Waterloo ## and ##University of Ottowa##'} 
)

st.markdown("""
    <style>
    .title-font {
        font-family: 'Lato', sans-serif;
        font-size: 48px;
        font-weight: 400;
        margin-bottom: 0px;
        color: #2c3e50;
    }
    .subtitle-font {
        font-family: 'Lato', sans-serif;
        font-size: 18px;
        font-weight: 200;
        margin-top: -20px;
        color: #2c3e50;
    }
    </style>
            
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    }

    </style>

""", unsafe_allow_html=True)



# Optional: Top navigation using st.page_link
left, mid, right = st.columns([40, 1, 1])

with left:
    col1, col2, col3, col4 = st.columns([1.1, 2.6, 2.6, 1.8])
    with col1:
        st.page_link("main.py", label= "Database")

    with col2:
        st.page_link("pages/Calculator.py", label="Critical Velocity Calculator")
    
    with col3:
        st.page_link("pages/ParticleVelocity.py", label="Particle Velocity Calculator")

    with col4:
        st.page_link("pages/Submit.py", label="Your Contribution")

st.image(uni_path, width=600, output_format="auto")

MATERIAL_DB = {
    "Copper (Cu)": {
        "rho": 8.96,  # Density (g/cm³)
        "Tm": 1083,   # Melting Temp (°C)
        "Cp": 384, # Specific Heat Capacity (J/Kg per K)
        "B": 140, # Bulk Modulus (GPA)
        "su_default": 220,  # Ultimate Strength (MPa) - Default
        "Ti_default": 320,  # Initial Temp (°C) - Default
        "Tp_default": 26.85, # Particle Imact Temp (°C) - Default
        "d_default": 20, # Particle Diameter (μm) - Default
        "dref_default": 10, # Reference Particle Diameter (μm) - Default
        #"k1_default": 0.6, #A particle-size-dependent fitting parameter, used in vcr formula (Dimensionless) - Default
        "gamma_default": 230, #A material-dependent model parameter that incorporates correlation between spall strength and tensile strength (μm^0.19) - Default
    },
    "Aluminum (Al)": { 
        "rho": 2.70,  # Density (g/cm³)
        "Tm": 660,    # Melting Temp (°C)
        "Cp": 890, # Specific Heat Capacity (J/Kg per K)
        "B": 75, # Bulk Modulus (GPA)
        "su_default": 110,   # Ultimate Strength (MPa) - Default
        "Ti_default": 20,    # Initial Temp (°C) - Default
        "Tp_default": 0.0, # Particle Imact Temp (°C) - Default
        "d_default": 20, # Particle Diameter (μm) - Default
        "dref_default": 10, # Reference Particle Diameter (μm) - Default
        "k1_default": 0.55, # A particle-size-dependent fitting parameter, used in vcr formula (Dimensionless) - Default
        "gamma_default": 230, #A material-dependent model parameter that incorporates correlation between spall strength and tensile strength (μm^0.19) - Default
    }
}

# --- Critical Velocity Calculation Functions ---
def calculate_critical_velocity_1(rho, Tm, su, Ti):
    """
    Calculates critical velocity (v_cr) in m/s using the formula:
    v_cr = 667 - 14*rho + 0.08*Tm + 0.1*su - 0.4*Ti
    where units are: rho (g/cm³), Tm (°C), su (MPa), Ti (°C)
    """
    
    v_cr = 667 - (14 * rho) + (0.08 * Tm) + (0.1 * su) - (0.4 * Ti)
    return v_cr

def calculate_critical_velocity_2(k1, Cp, rho, Tm, Tp, su):
    """
    Calculates critical velocity (v_cr) in m/s using the formula:
    v_cr = k1*sqrt(Cp*(Tm-Tp) + 16*su/rho*((Tm - Tp)/(Tm - 293)))
    where units are: Cp (J/kg per K), rho (Kg/m³), Tm (K), su (Pa), Tp (K), k1 (dimensionless)
    """
    
    v_cr = k1*math.sqrt(Cp*((Tm + 273.15) - (Tp + 273.15)) + 16*((su*1000000)/(rho*1000))*(((Tm + 273.15) - (Tp + 273.15))/((Tm + 273.15) - 293)))
    return v_cr

def calculate_critical_velocity_3(gamma, su, B, rho, Tm, Tp, d):
    """
    Calculates critical velocity (v_cr) in m/s using the formula:
    v_cr = gamma*(su/B)*sqrt(B/(rho*1000))*(((Tm - Tp)/(Tm - 20.0))^0.5)*(1/(d^0.19))
    where units are: gamma (μm^0.19), su (MPa), B (GPa), rho (Kg/m³), Tm (°C) , Tp (°C), d (μm)
    """
    
    #v_cr = gamma*(su/B)*math.sqrt(B/(rho*1000))*(((Tm - Tp)/(Tm - 20))**0.5)*(1/(d**0.19))
    v_cr = gamma*((su*10**6)/(B*10**9))*math.sqrt((B*10**9)/(rho*1000))*(((Tm - Tp)/(Tm - 20))**0.5)*(d**(-0.19))
    
    return v_cr

def calculate_k1(d, dref):
    return 0.64*(d/dref)**(-0.18)

# 1. Material Selection
st.sidebar.header("Parameter Selection")
material_name = st.sidebar.selectbox(
    "Select Material",
    list(MATERIAL_DB.keys())
)

material_data = MATERIAL_DB[material_name]

# Load fixed material parameters
rho = material_data["rho"]
Tm = material_data["Tm"]
Cp = material_data["Cp"]
B = material_data["B"]
su_default = material_data["su_default"]
Ti_default = material_data["Ti_default"]
Tp_default = material_data["Tp_default"]
d_default = material_data["d_default"]
dref_default = material_data["dref_default"]
#k1_default = material_data["k1_default"]
gamma_default = material_data["gamma_default"]


# Display fixed material parameters in the sidebar
st.sidebar.markdown(f"**Fixed Material Properties:**")
st.sidebar.metric("Density ($ρ$)", f"{rho} g/cm³")
st.sidebar.metric("Melting Temperature ($T_m$)", f"{Tm} °C")
st.sidebar.metric("Specific Heat Capacity ($C_p$)", f"{Cp} J/Kg per K")
st.sidebar.metric("Bulk Modulus ($B$)", f"{B} GPa")

# Initial Particle Temperature (Ti)
Ti = st.sidebar.slider(
    "Initial Particle Temperature ($T_i$) in °C:", 
    min_value=20, 
    max_value=500, 
    value=Ti_default,
    help="Higher initial temperature decreases the critical velocity."
)

# Particle Impact Temperature (Tp)
Tp = st.sidebar.slider(
    "Particle Impact Temperature ($T_p$) in °C:", 
    min_value=20.0, 
    max_value=500.0, 
    value=Tp_default,
    help="Higher impact temperature decreases the critical velocity."
)

# Ultimate Strength (su)
su = st.sidebar.slider(
    "Ultimate Strength ($σ_u$) in MPa:", 
    min_value=50, 
    max_value=600, 
    value=su_default,
    help="Higher ultimate strength increases the critical velocity."
)

# Particle Diameter (μm)
d = st.sidebar.slider(
    "Particle Diameter ($d$) in μm:", 
    min_value=1, 
    max_value=100, 
    value=d_default,
    help="Higher particle diameter decreases the critical velocity."
)

# particle-size-dependent fitting parameter (k1)
#k1 = st.sidebar.slider(
#    "Particle-size-dependent fitting parameter (k1)", 
#    min_value=0.1, 
#    max_value=0.7, 
#    value=k1_default,
#    help="."
#)

# material-dependent model parameter (gamma)
gamma = st.sidebar.slider(
    "Material-dependent parameter correlating spall and tensile strengths (γ)", 
    min_value=50, 
    max_value=500, 
    value=gamma_default,
    help="A material-dependent model parameter that incorporates correlation between spall strength and tensile strength."
)
#------------------------------------------------------------------------from [1]
# Calculation and Result Display
v_cr_calculated_1 = calculate_critical_velocity_1(rho, Tm, su, Ti)

st.divider()

st.markdown(f"#### Calculated Critical Velocity based on Assadi et al. (2003)[1]")
st.metric(
    "Critical Velocity ($\mathbf{v_{cr}}$)", 
    f"{v_cr_calculated_1:.2f} m/s"
)

# Formula Display
with st.expander("Formulation"):
    st.markdown(f"**Formula Used [1]:**")
    st.latex(r"v_{cr} = 667 - 14\rho + 0.08T_m + 0.1\sigma_u - 0.4T_i")
    st.latex(f"       = 667 - 14×{rho} + 0.08×{Tm} + 0.1×{su} - 0.4×{Ti}")
    st.latex(f"       = {v_cr_calculated_1:.2f}  m/s")
    st.markdown(f"Where:")
    st.markdown(f"- $ρ$ = {rho} g/cm³")
    st.markdown(f"- $T_m$ = {Tm} °C")
    st.markdown(f"- $σ_u$ = {su} MPa (Adjustable)")
    st.markdown(f"- $T_i$ = {Ti} °C (Adjustable)")

#------------------------------------------------------------------------from [2]
# Calculation and Result Display
if "dref" not in st.session_state:
    st.session_state.dref = dref_default 

def update_my_value():
    st.session_state.dref = st.session_state.dref_slider_widget


k1 = calculate_k1(d, st.session_state.dref)
v_cr_calculated_2 = calculate_critical_velocity_2(k1, Cp, rho, Tm, Tp, su)

st.divider()

st.markdown(f"#### Calculated Critical Velocity based on Assadi et al. (2011)[2]")
st.metric(
    "Critical Velocity ($\mathbf{v_{cr}}$)", 
    f"{v_cr_calculated_2:.2f} m/s"
)

# Formula Display k1*sqrt(Cp*(Tm-Tp) + 16*su/rho*((Tm - Tp)/(Tm - 293)))
with st.expander("Formulation"):
    st.markdown(f"**Formula Used [2]:**")
    st.latex(r"v_{cr} = k_1 \sqrt{ C_p (T_m - T_p) + \frac{16\, \sigma_u}{\rho} \left( \frac{T_m - T_p}{T_m - 293} \right) }")
    st.latex(
        fr"= {k1} \sqrt{{ {Cp} ({Tm+273.15} - {Tp+273.15}) + \frac{{16\, × {su*1000000}}}{{{rho*1000}}} \left( \frac{{{Tm+273.15} - {Tp+273.15}}}{{{Tm+273.15} - 293}} \right) }}"
    )
    st.latex(f"       = {v_cr_calculated_2:.2f}  m/s")

    st.markdown(f"Where:")
    st.markdown(f"- $ρ$ = {rho*1000} Kg/m³")
    st.markdown(f"- $C_p$ = {Cp} J/Kg per K")
    st.markdown(f"- $T_m$ = {Tm+273.15} K")
    st.markdown(f"- $T_p$ = {Tp+273.15} K")
    st.markdown(f"- $σ_u$ = {su} MPa (Adjustable)")
    #st.markdown(f"- $k_1$ = {k1} (Adjustable)")
    st.latex(r"k_1 = 0.64 \left( \frac{d_p}{d_p^{\mathrm{ref}}} \right)^{-0.18}")
    #st.latex(fr" = 0.64 \left( \frac{{{d}{st.session_state.dref}}} \right)^{{-0.18}}")
    st.latex(fr"k_1 = 0.64 \left( \frac{{{d}}}{{{st.session_state.dref}}} \right)^{{-0.18}}")
    st.latex(fr" = {k1}")
    # Reference Particle Diameter (μm)
    col4, col5 = st.columns([1, 2]) 
    with col4:
        st.session_state.dref = st.slider(
            #"Reference Particle Diameter ($d$) in μm:", 
            "Reference Particle Diameter ($d_{{ref}}$) in μm:",
            min_value=1, 
            max_value=100, 
            value= st.session_state.dref,
            key="dref_slider_widget",
            on_change=update_my_value,
            help="A reference particle size",
        )

    st.markdown(f"- $d_p$ = {d} μm (Adjustable)")
    st.markdown(f"- $d_{{ref}}$ = {st.session_state.dref} μm (Adjustable)")

#--------------------------Plot
st.markdown("""\n
\n""")
st.divider()
st.markdown("""\n
\n""")
st.markdown(f"#### Model Comparison: Critical Velocity as a Function of Parameter")
#variables = {"rho" : rho, "Tm" : Tm, "Cp" : Cp, "B" : B, "Ti" : Ti, "Tp" : Tp, "su" : su, "d" : d, "k1" : k1, "gamma" : gamma}
variables = {"ρ" : rho, "Tm" : Tm, "Cp" : Cp, "B" : B, "Ti" : Ti, "Tp" : Tp, "σu" : su, "d" : d, "γ" : gamma}
variables_text = {"ρ" : "ρ", "Tm" : "$T_m$","Cp" :"$C_p$", "B" : "B", "Ti" : "$T_i$", "Tp" : "$T_p$", "σu" :"$σ_u$", "d" : "d", "γ" : "γ"}
var_text = st.selectbox("Select parameter to vary:", variables)
var_to_vary = variables[var_text]
var_range = st.slider(f"Select a range of values for {variables_text[var_text]}", var_to_vary/2, 3*var_to_vary/2, (3*var_to_vary/4, 5*var_to_vary/4))
var_min, var_max = var_range
x = np.linspace(var_min, var_max, 200)

vcr1_vals = []
vcr2_vals = []
vcr3_vals = []

for val in x:
    variables[var_text] = val
    k1 = calculate_k1(variables["d"], st.session_state.dref)
    vcr1_vals.append(calculate_critical_velocity_1(variables["ρ"], variables["Tm"], variables["σu"], variables["Ti"]))
    vcr2_vals.append(calculate_critical_velocity_2(k1, variables["Cp"], variables["ρ"], variables["Tm"], variables["Tp"], variables["σu"]))
    vcr3_vals.append(calculate_critical_velocity_3(variables["γ"], variables["σu"], variables["B"], variables["ρ"], variables["Tm"], variables["Tp"], variables["d"]))

fig, ax = plt.subplots()
ax.plot(x, vcr1_vals, "b", label = "Assadi et al. (2003)[1]")
ax.plot(x, vcr2_vals, "r", label = "Assadi et al. (2011)[2]")
if st.session_state.other:
    ax.plot(x, vcr3_vals, "k", label = "Zhang et al. (2025)[4]")
#ax.set_xlabel(variables_text[var_text])
#ax.set_ylabel("Critical Velocity (m/s)")
#ax.set_title(f"Critical Velocity vs {variables_text[var_text]}")
#ax.legend()

plot_placeholder = st.empty()
#st.pyplot(fig)

#------------------------------------------------------------------------from [3]
# Calculation and Result Display


v_cr_calculated_3 = calculate_critical_velocity_3(gamma, su, B, rho, Tm, Tp, d)

st.divider()
st.markdown(f"#### Other Methods")
st.markdown("\n")
st.markdown(f"##### Calculated Critical Velocity based on Hassani et al. (2016)[3] and Zhang et al. (2025)[4]")
st.metric(
    "Critical Velocity ($\mathbf{v_{cr}}$)", 
    f"{v_cr_calculated_3:.2f} m/s"
)


#st.session_state.other = st.toggle(
#    "Show on the plot",
#    value=st.session_state.other
#)
other_check = st.checkbox("Show on the plot", value=False)
if other_check:
    st.session_state.other = False
else:
    st.session_state.other = True

# Formula Display gamma*(su/B)*sqrt(B/(rho*1000))*(((Tm - Tp)/(Tm - 20))^0.5)*(1/(d^0.19))
with st.expander("Formulation"):
    st.markdown(f"**Formula Used [4]:**")
    st.latex(r"""
    v_{cr} = \gamma \left(\frac{\sigma_u}{B}\right)
    \sqrt{\frac{B}{\rho}}
    \left(\frac{T_m - T_p}{T_m - T_{room}}\right)^{m}
    \frac{1}{d^{n}}
    """)
    st.latex(
        fr"""
    = {gamma} \left( \frac{{{su}}}{{{B}}} \right)
    \sqrt{{ \frac{{{B}}}{{{rho}}} }}
    \left( \frac{{{Tm} - {Tp}}}{{{Tm} - 20}} \right)^{{0.5}}
    \frac{{1}}{{ d^{{0.19}} }}
    """
    )


    st.latex(f"       = {v_cr_calculated_3:.2f}  m/s")

    st.markdown(f"Where:")
    st.markdown(f"- $ρ$ = {rho*1000} Kg/m³")
    st.markdown(f"- $B$ = {B} GPa")
    st.markdown(f"- $T_m$ = {Tm} °C")
    st.markdown(f"- $T_p$ = {Tp} °C")
    st.markdown(f"- $T_{{room}}$ = 20 °C")
    st.markdown(f"- $σ_u$ = {su} MPa (Adjustable)")
    st.markdown(f"- $d$ = {d} μm (Adjustable)")
    st.markdown(f"- $γ$ = {gamma} (Adjustable)")
    st.markdown(f"- $m \; \\text{{(constant representing power-law dependency on temperature)}}$ = 0.5")
    st.markdown(f"- $n \; \\text{{(constant representing power-law relationship with particle diameter)}}$ = 0.19")

st.divider()

st.markdown("Disclaimer: The models used to calculate the critical velocity values have been developed based on specific materials and conditions. For the applicability of the models to a specific range of parameters, refer to the original publications.")

ax.set_xlabel(variables_text[var_text])
ax.set_ylabel("Critical Velocity (m/s)")
ax.set_title(f"Critical Velocity vs {variables_text[var_text]}")
ax.legend()
plot_placeholder.pyplot(fig)
#--------------------------
st.divider()
st.caption("[1] Hamid Assadi, Frank Gärtner, Thorsten Stoltenhoff, Heinrich Kreye, Bonding mechanism in cold gas spraying, Acta materialia, 51(15), 4379-4394, 2003.")
st.caption("[2] Hamid Assadi, T Schmidt, H Richter, J-O Kliemann, K Binder, F Gärtner, T Klassen, H Kreye, On parameter selection in cold spraying, Journal of thermal spray technology, 20(6), 1161-1176, 2011.")
st.caption("[3] Mostafa Hassani-Gangaraj, David Veysset, Keith A. Nelson, Christopher A. Schuh, Supersonic Impact of Metallic Micro-particles, arXiv preprint, arXiv:1612.08081, 2016.")
st.caption("[4] Che Zhang, Tesfaye Molla, Christian Brandl, Jarrod Watts, Rick Mccully, Caixian Tang, Graham Schaffer, Critical velocity and deposition efficiency in cold spray: A reduced-order model and experimental validation, Journal of Manufacturing Processes, 134, 547-557, 2025.")
