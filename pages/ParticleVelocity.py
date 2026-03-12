import streamlit as st
import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve
from scipy.optimize import brentq
import sympy as sp

# --- Streamlit UI Setup ---
current_dir = os.path.dirname(__file__)
logo_path = os.path.join(current_dir, "logo4.png")
uni_path = os.path.join(current_dir, "particle_logo.png")

st.set_page_config(
    page_title="Particle Velocity Calculator",        
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
col1, col2, col3, col4 = st.columns([1.15, 3.1, 3.25, 2.1])
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
        "rho_p": 8960.0,  # Particle Density (Kg/m³)
    },
    "Aluminum (Al)": { 
        "rho_p": 2700.0,  # Particle Density (Kg/m³)
    },
    "Iron (Fe)": { 
        "rho_p": 7870.0,  # Density (Kg/cm³)
    },
    "Magnesium (Mg)": { 
        "rho_p": 1740.0,  # Density (Kg/cm³)
    },
    "Nickel (Ni)": { 
        "rho_p": 8910.0,  # Density (Kg/cm³)
    },
    "Titanium (Ti)": { 
        "rho_p": 4510.0,  # Density (Kg/cm³)
    },
    "Custom Material": { 
        "rho_p": 2700.0,  # Density (Kg/cm³)
    },
}

GAS_DB = {
    "Nitrogen (N2)": {
        "Gamma": 1.4,  # Ratio of specific heats
        "R": 296.8,   # Gas constant for Nitrogen (J/kg·K)
    },
    "Helium (He)": {
        "Gamma": 1.67,  # Ratio of specific heats
        "R": 2077.1,   # Gas constant for Nitrogen (J/kg·K)
    },
    "Argon (Ar)": {
        "Gamma": 1.67,  # Ratio of specific heats
        "R": 208.0,   # Gas constant for Nitrogen (J/kg·K)
    },
    "Hydrogen (H2)": {
        "Gamma": 1.41,  # Ratio of specific heats
        "R": 4124.0,   # Gas constant for Nitrogen (J/kg·K)
    },
    "Air": {
        "Gamma": 1.4,  # Ratio of specific heats
        "R": 287.1,   # Gas constant for Nitrogen (J/kg·K)
    },
}

###External functions###
####################################
#Functions

def get_viscosity(T):
    """Sutherland's Law for Nitrogen viscosity."""
    mu0 = 1.781e-5
    S = 111.0
    return mu0 * (T / 288.15)**1.5 * (288.15 + S) / (T + S)


def henderson_drag(Re, M_rel, T_p, T_g):
    """
    Henderson's Drag Coefficient Correlation (1976) for all 3 regimes.
    Note: These formulas are not in the sources and should be verified.
    """
    if Re < 1e-6: return 0.44 # Default for very high Re/low viscosity
    
    S = M_rel * np.sqrt(gamma / 2.0) # Molecular speed ratio
    
    # 1. Subsonic Regime (M_rel < 1.0)
    def cd_subsonic(Re_val, M_val, S_val):
        term1 = 24.0 / (Re_val + S_val * (4.33 + (3.65 - 1.53 * T_p / T_g) / (1.0 + 0.353 * T_p / T_g) * np.exp(-0.247 * Re_val / S_val)))
        term2 = np.exp(-0.5 * M_val / np.sqrt(Re_val)) * ((4.5 + 0.38 * (0.03 * Re_val + 0.48 * np.sqrt(Re_val))) / (1.0 + 0.03 * Re_val + 0.48 * np.sqrt(Re_val)) + 0.1 * M_val**2 + 0.2 * M_val**8)
        term3 = (1.0 - np.exp(-M_val / Re_val)) * 0.6 * S_val
        return term1 + term2 + term3

    # 2. Supersonic Regime (M_rel >= 1.75)
    def cd_supersonic(Re_val, M_val, S_val):
        term1 = (0.9 + 0.34 / (M_val**2) + 1.86 * np.sqrt(M_val / Re_val) * (2.0 + 2.0/(S_val**2) + 1.058/S_val * np.sqrt(T_p/T_g) - 1.0/(S_val**4)))
        term2 = 1.0 + 1.86 * np.sqrt(M_val / Re_val)
        return term1 / term2

    # Logic for Mach Number Ranges
    if M_rel < 1.0:
        return cd_subsonic(Re, M_rel, S)
    elif M_rel >= 1.75:
        return cd_supersonic(Re, M_rel, S)
    else:
        # 3. Transonic/Transition Regime (1.0 <= M_rel < 1.75)
        # Linear interpolation between M=1.0 and M=1.75
        cd_1 = cd_subsonic(Re, 1.0, 1.0 * np.sqrt(gamma / 2.0))
        cd_175 = cd_supersonic(Re, 1.75, 1.75 * np.sqrt(gamma / 2.0))
        return cd_1 + (M_rel - 1.0) / 0.75 * (cd_175 - cd_1)
    



###Particle Velocity Calculations###
####################################
#Functions

linear_or_custom = "Linear"
#Calculating supersonic Mach number M based on local area A(x)
def get_mach_from_area_ratio(x_val):

    # Assuming a linear divergent nozzle for area calculation
    D_local = Dnt + (De - Dnt) * (x_val / Lf)
    A_local = np.pi * (D_local/2)**2
    area_ratio = A_local / At

    # Isentropic Area-Mach Relation
    def equation(M):
        if M <= 0: return 1e6
        term = (2 / (gamma + 1)) * (1 + (gamma - 1) / 2 * M**2)
        exponent = (gamma + 1) / (2 * (gamma - 1))
        return (1/M) * (term**exponent) - area_ratio

    # Solve for M > 1 (supersonic branch for divergent section) [3]
    #for fsolve
    #if x_val < Lf/2:
    #    initial_guess = 0.5  # subsonic near throat
    #else:
    #    initial_guess = 2.0 
        # Automatic branch selection
    if area_ratio < 1:
        # Subsonic: M < 1
        a, b = 1e-6, 1.0
    else:
        # Supersonic: M > 1
        a, b = 1.0, 5.0
        # expand upper bound if necessary
        res_a, res_b = equation(a), equation(b)
        if res_a * res_b > 0:
            for b_try in np.linspace(5.0, 20.0, 4):
                if equation(b_try) * res_a < 0:
                    b = b_try
                    break
            else:
                return np.nan  # no root found

    return brentq(equation, a, b, maxiter=100)

#Calculating gas state-Returns local gas density (rho) and temperature (T) 
def get_gas_state(M):

    T = T0 / (1 + (gamma - 1) / 2 * M**2)
    P = P0 / (1 + (gamma - 1) / 2 * M**2)**(gamma / (gamma - 1))
    rho = P / (R * T)
    #vgx = M * np.sqrt(gamma * R * T)
    return rho, T

#Governing differential equation-The ODE based on Newton's Second Law
def dvp_dx(x, vp):
    
    if vp <= 0: return 1e-6 
    
    M = get_mach_from_area_ratio(x)
    rho_gas, T_gas = get_gas_state(M)
    v_gas = M * np.sqrt(gamma * R * T_gas)
    mu_gas = get_viscosity(T_gas)
    v_rel = np.abs(v_gas - vp)
    Re_p = (rho_gas * v_rel * dp) / mu_gas
    M_rel = v_rel / np.sqrt(gamma * R * T_gas)
    #Cd = 0.44 # Drag Coefficient (Cd)
    Cd = henderson_drag(Re_p, M_rel, 1/2*T_gas, T_gas)
    
    acceleration = (Cd * rho_gas * Ap) / (2 * mp * vp) * (v_gas - vp)**2
    return acceleration

####################################
####################################


#Material Selection
st.sidebar.header("Parameter Selection")
material_name = st.sidebar.selectbox(
    "Select Material",
    list(MATERIAL_DB.keys())
)

material_data = MATERIAL_DB[material_name]

gas_name = st.sidebar.selectbox(
    "Select Carrier Gas",
    list(GAS_DB.keys())
)

gas_data = GAS_DB[gas_name]

# Load fixed material and gas parameters
rho_p_default = material_data["rho_p"]
gamma = gas_data["Gamma"]
R = gas_data["R"]

P0_default = 30e5
T0_default = 973
dp_default = 20
Dnt_default = 1.5
De_default = 5.0
Lf_default = 100.0
v0_default = 20

# Display fixed material and gas parameters in the sidebar

st.sidebar.markdown(f"**Fixed Material Properties:**")
if material_name != "Custom Material":
    rho_p = rho_p_default
    st.sidebar.metric("Particle Density ($ρ_p$)", f"{rho_p} Kg/m³")
else:
    rho_p = st.sidebar.slider(
    "Particle Density ($ρ_p$) in Kg/cm³:", 
    min_value=1000.0, 
    max_value=20000.0, 
    value=rho_p_default,
    )

st.sidebar.metric("Heat Capacity Ratio ($γ$)", f"{gamma}")
st.sidebar.metric("Gas Constant ($R$)", f"{R} J/kg·K")

# Select material and gas parameters in the sidebar

# Stagnation pressure (P0)
P0 = st.sidebar.slider(
    "Stagnation Pressure ($P_0$) in Pa:", 
    min_value=5e5, 
    max_value=60e5, 
    value=P0_default
)

# Stagnation Temperature (T0)
T0 = st.sidebar.slider(
    "Stagnation Temperature ($T_0$) in K:", 
    min_value=573, 
    max_value=1373, 
    value=T0_default
)

# Particle Diameter (dp)
dp = st.sidebar.slider(
    "Particle Diameter ($d_p$) in μm:", 
    min_value=1, 
    max_value=100, 
    value=dp_default
)

dp = dp*1e-6
mp = rho_p * (4/3) * np.pi * (dp/2)**3  # Particle mass (Kg)
Ap = np.pi * (dp/2)**2 # Particle projected area

# Select nozzle geometry in the sidebar

#st.sidebar.markdown(f"**Nozzle Geometry:**")

# Nozzle throat diameter (m)
#linear_or_custom = st.sidebar.selectbox(
#    "Nozzle Geometry",
#    ["Linear", "Custom Geometry"]
#)
if linear_or_custom == "Custom Geometry":
    function_string = st.sidebar.text_input("Enter the function describing the nozzle geometry:", help="""Write the equation using Python syntax with "x" for the longitudinal coordinate and "L" for the length of the divergent part of the nozzle.""")
    x, L = sp.symbols('x L')

    f_geom = None
    if function_string:
        try:
            expr = sp.sympify(
            function_string,
            locals={"x": x, "L": L}
        )
            f_geom = sp.lambdify((x, L), expr, "numpy")

        except Exception as e:
            st.error(f"Invalid expression: {e}")
            st.stop()

Dnt = st.sidebar.slider(
    "Nozzle Throat Diameter ($D_nt$) in mm:", 
    min_value=1.0, 
    max_value=4.0, 
    value=Dnt_default
)

Dnt = Dnt*1e-3

De = st.sidebar.slider(
    "Nozzle Exit Diameter ($D_e$) in mm:", 
    min_value=4.0, 
    max_value=20.0, 
    value=De_default
)

De = De*1e-3

Lf = st.sidebar.slider(
    "Length of divergent region ($L_f$) in mm:", 
    min_value=40.0, 
    max_value=300.0, 
    value=Lf_default
)

Lf = Lf*1e-3

At = np.pi * (Dnt/2)**2 # Throat area (A*)

v0 = st.sidebar.slider(
    "Particle velocity at throat (x=0) ($V_0$) in m/s:", 
    min_value=10, 
    max_value=300, 
    value=v0_default
)


#Solution

x_span = (0, Lf) # Integrate from throat to exit

sol = solve_ivp(dvp_dx, x_span, [v0], t_eval=np.linspace(0, Lf, 100))

#Output
#print(f"Final Particle Velocity at Exit: {sol.y[-1, -1]:.2f} m/s")
st.divider()
st.markdown(f"#### Calculated Particle Velocity based on Alonso et al. (2023)[1]")
st.metric(
    "Particle Velocity at Exit($\mathbf{v_{p}}$)", 
    f"{sol.y[-1, -1]:.2f} m/s"
)

#--------------------------Plot
st.markdown("\n\n")
st.divider()
st.markdown(f"#### Particle Velocity as a Function of Parameter")

variables = {"P0" : P0, "T0" : T0,  "dp" : dp, "Lf" : Lf, "v0" : v0}
variables_text = {"P0" : "$P_0$", "T0" : "$T_0$","dp" :"$d_p$", "Lf" : "$L_f$", "v0" :"$V_0$"}
var_text = st.selectbox("Select parameter to vary:", variables)
var_to_vary = variables[var_text]
var_range = st.slider(f"Select a range of values for {variables_text[var_text]}", var_to_vary/2, 3*var_to_vary/2, (3*var_to_vary/4, 5*var_to_vary/4))
var_min, var_max = var_range
plot_range = np.linspace(var_min, var_max, 200)

vp_vals = []

for val in plot_range:
    variables[var_text] = val
    P0 = variables["P0"]
    T0 = variables["T0"]
    dp = variables["dp"]
    mp = rho_p * (4/3) * np.pi * (dp/2)**3  # Particle mass (Kg)
    Ap = np.pi * (dp/2)**2 # Particle projected area
    Lf = variables["Lf"]
    v0 = variables["v0"]
    x_span = (0, Lf) # Integrate from throat to exit
    sol = solve_ivp(dvp_dx, x_span, [v0], t_eval=np.linspace(0, Lf, 100))
    vp_vals.append(sol.y[-1, -1])


fig, ax = plt.subplots()
ax.plot(plot_range, vp_vals, "b")

ax.set_xlabel(variables_text[var_text])
ax.set_ylabel("Particle Velocity (m/s)")
ax.set_title(f"Particle Velocity vs {variables_text[var_text]}")

st.pyplot(fig)

#--------------------------
#--------------------------
st.divider()
st.caption("[1] L. Alonso, M.A. Garrido-Maneiro, P. Poza, A study of the parameters affecting the particle velocity in cold-spray: Theoretical results and comparison with experimental data, Additive Manufacturing, 67, 103479, 2023.")
st.caption("[2] X. Ning, Q. Wang, Z. Ma, H. Kim, Numerical Study of In-flight Particle Parameters in Low-Pressure Cold Spray Process, Journal of Thermal Spray Technology, 19, 1211–1217, 2010.")
