import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph
import pandas as pd
import os


current_dir = os.path.dirname(__file__)
uni_path = os.path.join(current_dir, "logo.png")
image_path = os.path.join(current_dir, "logo3.jpeg")
logo_path = os.path.join(current_dir, "logo4.png")
file_path = os.path.join(current_dir, "database4_example.ttl")


prologue_text = "SELECT DISTINCT ?Year ?DOI ?Title "
coldspray_text =""
custom_results = ""
author_query = ""
query_mic_results = [""]
query_mech_results = [""]
approach_query = ""
numerical_query = ""
experimental_query = ""
dim_query = ""
cons_query = ""
soft_query = ""
mesh_query = ""
constant_query = ""

selected_materials_query = "any" 
selected_model_materials_query = "any"
selected_preprocessing_query = "any"
selected_characterization_query = "any" 
selected_mic_result_query = 0
selected_mech_result_query = 0


st.set_page_config(
    page_title="Cold Spray Hub",        
    page_icon= logo_path,                  
    layout="centered",                   
    initial_sidebar_state="expanded",
    menu_items = {'About': 'This is a tool desined and provided by ## University of Waterloo ## and ##University of Ottowa##'} 
)

# Optional: Top navigation using st.page_link
left, mid, right = st.columns([9, 1, 1])

with left:
    col1, col2, col3, col4 = st.columns([1.3, 3, 3, 1.5])
    with col1:
        st.page_link("Home.py", label= "Database")

    with col2:
        st.page_link("pages/Calculator.py", label="Critical Velocity Calculator")
    
    with col3:
        st.page_link("pages/ParticleVelocity.py", label="Particle Velocity Calculator")

    with col4:
        st.page_link("pages/Submit.py", label="Your Contribution")



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

#st.markdown('<div class="title-font">Cold Spray Hub</div>', unsafe_allow_html=True)
#st.markdown('<div class="subtitle-font">(Cold Spray Additive Manufacturing Database)</div>', unsafe_allow_html=True)


@st.cache_resource
def load_graph(ttl_path):
    g = Graph()
    g.parse(ttl_path, format="ttl")
    return g

def run_query(g, query):
    results = g.query(query)
    rows = []
    for row in results:
        rows.append([str(cell) for cell in row])
    cols = results.vars
    return pd.DataFrame(rows, columns=[str(c) for c in cols])

#st.title("Cold Spray Database")
st.image(uni_path, width=600, output_format="auto")

#ttl_file = st.file_uploader("Upload RDF file", type=["ttl"])
ttl_file = file_path

if ttl_file is not None:
    g = load_graph(ttl_file)

    ################################################################Numerical
    query_model_materials = {
        "any":"""""",
        "Aluminum and Aluminum Alloys":"""
        
    ?paper a cs:ColdSprayPaper ;
         cs:hasComputationalStudy ?comp .
    ?comp cs:modelsMaterial ?Model_Material .
                
    
    FILTER (regex(?Model_Material, "Al|Aluminum|aluminum"))
        """
,
        "Copper and Copper Alloys":"""
        
    ?paper a cs:ColdSprayPaper ;
         cs:hasComputationalStudy ?comp .
    ?comp cs:modelsMaterial ?Model_Material .

    FILTER (regex(?Model_Material, "Cu|Copper|copper"))
        """,
        "Nickel and Nickel Alloys":"""
        
    ?paper a cs:ColdSprayPaper ;
         cs:hasComputationalStudy ?comp .
    ?comp cs:modelsMaterial ?Model_Material .

    FILTER (regex(?Model_Material, "Ni|Nickel|nickel"))
        """,
        "Titanium and Titanium Alloys":"""
        
    ?paper a cs:ColdSprayPaper ;
         cs:hasComputationalStudy ?comp .
    ?comp cs:modelsMaterial ?Model_Material .

    FILTER (regex(?Model_Material, "Ti|Titanium|titanium"))
        """,
        "Iron and Steel Alloys":"""
        
    ?paper a cs:ColdSprayPaper ;
         cs:hasComputationalStudy ?comp .
    ?comp cs:modelsMaterial ?Model_Material .

    FILTER (regex(?Model_Material, "Fe|Iron|Steel|iron|steel"))
        """,
        "Magnesium and Magnesium Alloys":"""
        
    ?paper a cs:ColdSprayPaper ;
         cs:hasComputationalStudy ?comp .
    ?comp cs:modelsMaterial ?Model_Material .

    FILTER (regex(?Model_Material, "Mg|Magnesium|magnesium"))
        """,
        "Carbides":"""
        
    ?paper a cs:ColdSprayPaper ;
         cs:hasComputationalStudy ?comp .
    ?comp cs:modelsMaterial ?Model_Material .

    FILTER (regex(?Model_Material, "SiC|WC|CBN|Carbide|carbide"))
        """,
        "Keyword Search":"""

    ?paper a cs:ColdSprayPaper ;
         cs:hasComputationalStudy ?comp .
    ?comp cs:modelsMaterial ?Model_Material .

    FILTER (regex(?Model_Material, "keyword"))

""",
    }



    ################################################################End of Numerical

    query_materials = {
        "any":"""""",
        "Aluminum and Aluminum Alloys":"""
        
    ?paper a cs:ColdSprayPaper ;
         cs:hasMaterial ?material .
    ?material cs:hasCondition ?Material_Condition ;
                cs:hasComposition ?Composition .
    
    FILTER (regex(?Composition, "Al|Aluminum|aluminum"))
        """
,
        "Copper and Copper Alloys":"""
        
    ?paper a cs:ColdSprayPaper ;
         cs:hasMaterial ?material .
    ?material cs:hasCondition ?Material_Condition ;
                cs:hasComposition ?Composition .

    FILTER (regex(?Composition, "Cu|Copper|copper"))
        """,
        "Nickel and Nickel Alloys":"""
        
    ?paper a cs:ColdSprayPaper ;
         cs:hasMaterial ?material .
    ?material cs:hasCondition ?Material_Condition ;
                cs:hasComposition ?Composition .

    FILTER (regex(?Composition, "Ni|Nickel|nickel"))
        """,
        "Titanium and Titanium Alloys":"""
        
    ?paper a cs:ColdSprayPaper ;
         cs:hasMaterial ?material .
    ?material cs:hasCondition ?Material_Condition ;
                cs:hasComposition ?Composition .

    FILTER (regex(?Composition, "Ti|Titanium|titanium"))
        """,
        "Iron and Steel Alloys":"""
        
    ?paper a cs:ColdSprayPaper ;
         cs:hasMaterial ?material .
    ?material cs:hasCondition ?Material_Condition ;
                cs:hasComposition ?Composition .

    FILTER (regex(?Composition, "Fe|Iron|Steel|iron|steel"))
        """,
        "Magnesium and Magnesium Alloys":"""
        
    ?paper a cs:ColdSprayPaper ;
         cs:hasMaterial ?material .
    ?material cs:hasCondition ?Material_Condition ;
                cs:hasComposition ?Composition .

    FILTER (regex(?Composition, "Mg|Magnesium|magnesium"))
        """,
        "Carbides":"""
        
    ?paper a cs:ColdSprayPaper ;
         cs:hasMaterial ?material .
    ?material cs:hasCondition ?Material_Condition ;
                cs:hasComposition ?Composition .

    FILTER (regex(?Composition, "SiC|WC|CBN|Carbide|carbide"))
        """,
        "Keyword Search":"""

    ?paper a cs:ColdSprayPaper ;
         cs:hasMaterial ?material .
    ?material cs:hasCondition ?Material_Condition ;
                cs:hasComposition ?Composition .

    FILTER (regex(?Composition, "keyword"))

""",
    }


    query_preprocessing = {
        "any":"""""",
        "Heat Treatment":"""
        
            ?paper cs:hasPreprocessing ?preprocessing .
  ?preprocessing cs:hasHeatTreatment ?heatTreatment .
  ?heatTreatment cs:annealingTemperature ?annealingTemperature .
  ?heatTreatment cs:annealingTime ?annealingTime .
  BIND(CONCAT(STR(?annealingTemperature), ", ", STR(?annealingTime)) AS ?Preprocessing_Method)
        """,

        "Powder Production":"""
        
            ?paper cs:hasPreprocessing ?preprocessing .
  ?preprocessing cs:hasPowderProduction ?Preprocessing_Method .
  
        """,

        "Substrate Preparation":"""
        
            ?paper cs:hasPreprocessing ?preprocessing .
  ?preprocessing cs:hasSubstratePreparation ?Preprocessing_Method .

        """,
        
    }

    query_characterization = {
        "any":"""""",
        "Scanning Electron Microscopy":"""
        
            ?paper cs:hasCharacterization ?characterization .
  ?characterization cs:techniqueName ?techniqueName .
  FILTER (regex(?techniqueName, "SEM"))
  ?characterization cs:parameter ?parameter .
  BIND(CONCAT(?techniqueName," : ", STR(?parameter)) AS ?Characterization_Method)
  
        """,
        "Transmission Electron Microscopy":"""
        
            ?paper cs:hasCharacterization ?characterization .
  ?characterization cs:techniqueName ?techniqueName .
  FILTER (regex(?techniqueName, "TEM"))
  ?characterization cs:parameter ?parameter .
  BIND(CONCAT(?techniqueName," : ", STR(?parameter)) AS ?Characterization_Method)
  
        """,
        "Light Optical Microscopy":"""
        
            ?paper cs:hasCharacterization ?characterization .
  ?characterization cs:techniqueName ?techniqueName .
  FILTER (regex(?techniqueName, "LOM|Light Optical Microscopy"))
  ?characterization cs:parameter ?parameter .
  BIND(CONCAT(?techniqueName," : ", STR(?parameter)) AS ?Characterization_Method)
  
        """,
        "Electron Backscatter Diffraction":"""
        
            ?paper cs:hasCharacterization ?characterization .
  ?characterization cs:techniqueName ?techniqueName .
  FILTER (regex(?techniqueName, "EBSD"))
  ?characterization cs:parameter ?parameter .
  BIND(CONCAT(?techniqueName," : ", STR(?parameter)) AS ?Characterization_Method)
  
        """,
        "Energy-dispersive X-ray":"""
        
            ?paper cs:hasCharacterization ?characterization .
  ?characterization cs:techniqueName ?techniqueName .
  FILTER (regex(?techniqueName, "EDS|EDX|EDAX"))
  ?characterization cs:parameter ?parameter .
  BIND(CONCAT(?techniqueName," : ", STR(?parameter)) AS ?Characterization_Method)
  
        """,
        "X-ray Diffraction":"""
        
            ?paper cs:hasCharacterization ?characterization .
  ?characterization cs:techniqueName ?techniqueName .
  FILTER (regex(?techniqueName, "XRD"))
  ?characterization cs:parameter ?parameter .
  BIND(CONCAT(?techniqueName," : ", STR(?parameter)) AS ?Characterization_Method)
  
        """,
        "X-ray Photoelectron Spectroscopy":"""
        
            ?paper cs:hasCharacterization ?characterization .
  ?characterization cs:techniqueName ?techniqueName .
  FILTER (regex(?techniqueName, "XPS"))
  ?characterization cs:parameter ?parameter .
  BIND(CONCAT(?techniqueName," : ", STR(?parameter)) AS ?Characterization_Method)
  
        """,

        
    }


    custom_author_query =  st.text_input("Author Search:")
    custom_doi_query =  st.text_input("DOI Search:")
    paper_type = st.selectbox("Select the type of study", ["any", "Experimental", "Numerical"])
    if paper_type == "Experimental":
        numerical_query = """

                ?paper a cs:ColdSprayPaper ;
                    cs:hasColdSprayProcess ?y .

                """
        with st.expander(f"#### Advanced Search", expanded = True):
            selected_materials_query = st.selectbox("Material", ["any", "Aluminum and Aluminum Alloys", "Copper and Copper Alloys", "Nickel and Nickel Alloys", "Titanium and Titanium Alloys", "Iron and Steel Alloys", "Magnesium and Magnesium Alloys", "Carbides", "Keyword Search"])
            
            if query_materials[selected_materials_query] != "":
                prologue_text = prologue_text + "?Composition ?Material_Condition" 

            if selected_materials_query == "Keyword Search":
                custom_material = st.text_input("Enter material keyword:")
                query_materials = {
                
                "Keyword Search":f"""

            ?paper a cs:ColdSprayPaper ;
                cs:hasMaterial ?material .
            ?material cs:hasCondition ?Material_Condition ;
                        cs:hasComposition ?Composition .

            FILTER (regex(?Composition, "{custom_material}"))

        """,
                        }
                
                

            selected_preprocessing_query = st.selectbox("Preprocessing", list(query_preprocessing.keys()))
            coldspray_checkbox = st.checkbox("Cold Spray Details", value=False)
            selected_characterization_query = st.selectbox("Characterization", list(query_characterization.keys()))

            if query_preprocessing[selected_preprocessing_query] != """""":
                prologue_text = prologue_text + "?Preprocessing_Method " 

            if coldspray_checkbox:
                prologue_text = prologue_text +  "?Process_Gas " + "?Gas_Pressure " + "?Gas_Temperature " + "?StandOff_Distance "   +  "?Particle_or_Impact_Velocity" 
                coldspray_text = """Optional{?paper cs:hasColdSprayProcess ?process . 
        Optional{?process cs:carrierGas ?Process_Gas .
        ?process cs:gasPressure ?gasPressure .
        ?process cs:gasPressureUnit ?gasPressureUnit .
        BIND(CONCAT(STR(?gasPressure)," ", STR(?gasPressureUnit)) AS ?Gas_Pressure) . }
        Optional{?process cs:nozzleTemperature ?nozzleTemperature .
        ?process cs:nozzleTemperatureUnit ?nozzleTemperatureUnit.
        BIND(CONCAT(STR(?nozzleTemperature)," ", STR(?nozzleTemperatureUnit)) AS ?Gas_Temperature) . }
        Optional{?process cs:standOffDistance ?standOffDistance .
        ?process cs:standOffDistanceUnit ?standOffDistanceUnit .
        BIND(CONCAT(STR(?standOffDistance)," ", STR(?standOffDistanceUnit)) AS ?StandOff_Distance) . }
            
        
        Optional{
            ?paper cs:hasResult ?result .
            ?result cs:hasMechanicalProperty ?mechProp .
            ?mechProp cs:propertyName ?propName .
            ?mechProp cs:propertyValue ?propVal .
            ?mechProp cs:propertyUnit ?propUnit .
            FILTER (REGEX(STR(?propName), "velocity", "i"))
            BIND(CONCAT(STR(?propName), ": ", STR(?propVal)," ", STR(?propUnit)) AS ?Particle_or_Impact_Velocity) .
            
            }

        Optional {?process cs:traverseVelocity ?velocity .
            ?process cs:traverseVelocityUnit ?velocityUnit .

            BIND(COALESCE(CONCAT("Traverse Velocity: ", STR(?velocity)," ", STR(?velocityUnit)), "NA") AS ?Particle_or_Impact_Velocity) .
            }

        
            

        }
        """
                
            if query_characterization[selected_characterization_query] != """""":
                prologue_text = prologue_text + "?Characterization_Method " 
            
            selected_mic_result_query = st.selectbox("Microstructure Results", ["None", "Grain Size", "Particle Size", "Deposition Efficiency", "Porosity", "Grain Boundary", "Roughness", "Corrosion Properties", "Fracture Morphology", "Deformation", "Keyword Search"])
            if selected_mic_result_query != "None":
                prologue_text = prologue_text + "?Microstructure_Parameter "
                if selected_mic_result_query != "Keyword Search":

                    query_mic_results = {"None":"""""",
                    "Grain Size":"""
                    
                        ?paper a cs:ColdSprayPaper ;
                            cs:hasResult ?result.
                        ?result cs:hasMicrostructureResult ?microstructure .
                        ?microstructure cs:featureDescription ?featureDescription .
                        ?microstructure cs:featureValue ?featureValue.
                        ?microstructure cs:featureUnit ?featureUnit.
            
                        FILTER (REGEX(STR(?featureDescription), "grain size", "i"))
                        BIND(CONCAT(STR(?featureDescription), ": ", STR(?featureValue)," ", STR(?featureUnit)) AS ?Microstructure_Parameter) .
                                """,
                    "Particle Size":"""
                    
                        ?paper a cs:ColdSprayPaper ;
                            cs:hasResult ?result.
                        ?result cs:hasMicrostructureResult ?microstructure .
                        ?microstructure cs:featureDescription ?featureDescription .
                        ?microstructure cs:featureValue ?featureValue.
                        ?microstructure cs:featureUnit ?featureUnit.
            
                        FILTER (REGEX(STR(?featureDescription), "particle size", "i"))
                        BIND(CONCAT(STR(?featureDescription), ": ", STR(?featureValue)," ", STR(?featureUnit)) AS ?Microstructure_Parameter) .
                        
                                """,

                    "Deposition Efficiency":"""
                    
                        ?paper a cs:ColdSprayPaper ;
                        cs:hasResult ?result.
                    ?result cs:depositionEfficiency ?microstructure .
                    
                    BIND(CONCAT("Deposition Efficiency: ", STR(?microstructure)," %") AS ?Microstructure_Parameter) .
                            """,

                    "Porosity":"""
                        ?paper a cs:ColdSprayPaper ;
                                cs:hasResult ?result .

                        ?result cs:hasMicrostructureResult ?microstructure .

                        OPTIONAL {
                            ?result cs:porosity ?porosity ;
                                    cs:porosityUnit ?porosityUnit .
                        }

                        OPTIONAL {
                            ?microstructure cs:featureDescription ?featureDescription ;
                                            cs:featureValue ?featureValue ;
                                            cs:featureUnit ?featureUnit .
                            FILTER(REGEX(STR(?featureDescription), "porosity", "i"))
                        }

                        
                        BIND(
                            IF(BOUND(?featureDescription),
                            CONCAT(STR(?featureDescription), ": ", STR(?featureValue), " ", STR(?featureUnit)),
                            ""
                            ) AS ?MicrostructurePorosity
                        )

                        BIND(
                            IF(BOUND(?porosity),
                            CONCAT("Porosity: ", STR(?porosity), " ", STR(?porosityUnit)),
                            ""
                            ) AS ?csPorosity
                        )

                        BIND(CONCAT(?MicrostructurePorosity, " ", ?csPorosity) AS ?Microstructure_Parameter)

                        
                        FILTER(REGEX(?Microstructure_Parameter, "porosity", "i"))
                                """,
                    "Grain Boundary":"""
                    
                        ?paper a cs:ColdSprayPaper ;
                            cs:hasResult ?result .

                        ?result cs:hasMicrostructureResult ?microstructure .
                        ?microstructure cs:featureDescription ?featureDescription .
                        ?microstructure cs:featureValue ?featureValue .

                        OPTIONAL { ?microstructure cs:featureUnit ?featureUnit }

                        FILTER (REGEX(STR(?featureDescription), "grain boundary", "i"))

                        BIND(
                            CONCAT(
                            STR(?featureDescription), ": ",
                            STR(?featureValue),
                            IF(BOUND(?featureUnit), CONCAT(" ", STR(?featureUnit)), "")
                            ) AS ?Microstructure_Parameter
                        )
                                        """,
                    "Roughness":"""
                    
                        ?paper a cs:ColdSprayPaper ;
                            cs:hasResult ?result.
                        ?result cs:hasMicrostructureResult ?microstructure .
                        ?microstructure cs:featureDescription ?featureDescription .
                        ?microstructure cs:featureValue ?featureValue.
                        ?microstructure cs:featureUnit ?featureUnit.
            
                        FILTER (REGEX(STR(?featureDescription), "roughness", "i"))
                        BIND(CONCAT(STR(?featureDescription), ": ", STR(?featureValue)," ", STR(?featureUnit)) AS ?Microstructure_Parameter) .
                                """,
                    "Corrosion Properties":"""
                        ?paper a cs:ColdSprayPaper ;
                            cs:hasResult ?result .

                        ?result cs:hasMicrostructureResult ?microstructure .
                        ?microstructure cs:featureDescription ?featureDescription .
                        ?microstructure cs:featureValue ?featureValue .

                        OPTIONAL { ?microstructure cs:featureUnit ?featureUnit }

                        FILTER (REGEX(STR(?featureDescription), "corrosion|Icorr|Ecorr", "i"))

                        BIND(
                            CONCAT(
                            STR(?featureDescription), ": ",
                            STR(?featureValue),
                            IF(BOUND(?featureUnit), CONCAT(" ", STR(?featureUnit)), "")
                            ) AS ?Microstructure_Parameter
                        )
                                        """,
                    "Fracture Morphology":"""
                    
                        ?paper a cs:ColdSprayPaper ;
                            cs:hasResult ?result .

                        ?result cs:hasMicrostructureResult ?microstructure .
                        ?microstructure cs:featureDescription ?featureDescription .
                        ?microstructure cs:featureValue ?featureValue .

                        OPTIONAL { ?microstructure cs:featureUnit ?featureUnit }

                        FILTER (REGEX(STR(?featureDescription), "fracture morphology", "i"))

                        BIND(
                            CONCAT(
                            STR(?featureDescription), ": ",
                            STR(?featureValue),
                            IF(BOUND(?featureUnit), CONCAT(" ", STR(?featureUnit)), "")
                            ) AS ?Microstructure_Parameter
                        )
                                        """,
                    "Deformation":"""
                    
                        ?paper a cs:ColdSprayPaper ;
                            cs:hasResult ?result .

                        ?result cs:hasMicrostructureResult ?microstructure .
                        ?microstructure cs:featureDescription ?featureDescription .
                        ?microstructure cs:featureValue ?featureValue .

                        OPTIONAL { ?microstructure cs:featureUnit ?featureUnit }

                        FILTER (REGEX(STR(?featureDescription), "deformation", "i"))

                        BIND(
                            CONCAT(
                            STR(?featureDescription), ": ",
                            STR(?featureValue),
                            IF(BOUND(?featureUnit), CONCAT(" ", STR(?featureUnit)), "")
                            ) AS ?Microstructure_Parameter
                        )
                                        """,
                        }
                else:
                    custom_mic = st.text_input("Enter a keyword for a microstructure parameter (e.g., texture, lattice strain, volume fraction):")
                    query_mic_results = {"Keyword Search":f"""
                            ?paper a cs:ColdSprayPaper ;
                            cs:hasResult ?result .

                        ?result cs:hasMicrostructureResult ?microstructure .
                        ?microstructure cs:featureDescription ?featureDescription .
                        ?microstructure cs:featureValue ?featureValue .

                        OPTIONAL {{ ?microstructure cs:featureUnit ?featureUnit }}

                        FILTER (REGEX(STR(?featureDescription), "{custom_mic}", "i"))

                        BIND(
                            CONCAT(
                            STR(?featureDescription), ": ",
                            STR(?featureValue),
                            IF(BOUND(?featureUnit), CONCAT(" ", STR(?featureUnit)), "")
                            ) AS ?Microstructure_Parameter
                        )
                                        """,
                                        }
                    #custom_results = st.text_input("Enter Result keyword:")
                    
            
            
                    

                    
                #st.write(query_results[selected_result_query])
            else:
                query_mic_results = {"None":"""""",}
                

            

            

            #"?Particle_Size_Evaluation" + "Particle_Size_Value" +    

            #if query_results[selected_result_query] != """""":
            #    prologue_text = prologue_text + "?propertyName " + "?propertyValue " + "?propertyUnit" 

            selected_mech_result_query = st.selectbox("Mechanical Property Results", ["None", "Hardness", "Tensile Strength", "Yield Strength", "Bonding Strength", "Elastic Modulus", "Wear Properties", "Ductility", "Residual Stress", "Keyword Search"])
            if selected_mech_result_query != "None":
                prologue_text = prologue_text + "?Mechanical_Property "
                if selected_mech_result_query != "Keyword Search": 
                    
                    query_mech_results = {"None":"""""",
                    "Hardness":"""
                        ?paper a cs:ColdSprayPaper ;
                            cs:hasResult ?result.
                        ?result cs:hasMechanicalProperty ?mechanical .
                        ?mechanical cs:propertyName ?propertyName .
                        ?mechanical cs:propertyValue ?propertyValue.
                        ?mechanical cs:propertyUnit ?propertyUnit.
            
                        FILTER (REGEX(STR(?propertyName), "hardness", "i"))
                        BIND(CONCAT(STR(?propertyName), ": ", STR(?propertyValue)," ", STR(?propertyUnit)) AS ?Mechanical_Property) .
                    """,
                    "Tensile Strength":"""
                        ?paper a cs:ColdSprayPaper ;
                            cs:hasResult ?result.
                        ?result cs:hasMechanicalProperty ?mechanical .
                        ?mechanical cs:propertyName ?propertyName .
                        ?mechanical cs:propertyValue ?propertyValue.
                        ?mechanical cs:propertyUnit ?propertyUnit.
            
                        FILTER (REGEX(STR(?propertyName), "tensile", "i"))
                        BIND(CONCAT(STR(?propertyName), ": ", STR(?propertyValue)," ", STR(?propertyUnit)) AS ?Mechanical_Property) .
                    """,
                    "Yield Strength":"""
                        ?paper a cs:ColdSprayPaper ;
                            cs:hasResult ?result.
                        ?result cs:hasMechanicalProperty ?mechanical .
                        ?mechanical cs:propertyName ?propertyName .
                        ?mechanical cs:propertyValue ?propertyValue.
                        ?mechanical cs:propertyUnit ?propertyUnit.
            
                        FILTER (REGEX(STR(?propertyName), "yield", "i"))
                        BIND(CONCAT(STR(?propertyName), ": ", STR(?propertyValue)," ", STR(?propertyUnit)) AS ?Mechanical_Property) .
                    """,
                    "Bonding Strength":"""
                        ?paper a cs:ColdSprayPaper ;
                            cs:hasResult ?result.
                        ?result cs:hasMechanicalProperty ?mechanical .
                        ?mechanical cs:propertyName ?propertyName .
                        ?mechanical cs:propertyValue ?propertyValue.
                        ?mechanical cs:propertyUnit ?propertyUnit.
            
                        FILTER (REGEX(STR(?propertyName), "bond|shear|cohesive|adhesion", "i"))
                        BIND(CONCAT(STR(?propertyName), ": ", STR(?propertyValue)," ", STR(?propertyUnit)) AS ?Mechanical_Property) .
                    """,
                    "Elastic Modulus":"""
                        ?paper a cs:ColdSprayPaper ;
                            cs:hasResult ?result.
                        ?result cs:hasMechanicalProperty ?mechanical .
                        ?mechanical cs:propertyName ?propertyName .
                        ?mechanical cs:propertyValue ?propertyValue.
                        ?mechanical cs:propertyUnit ?propertyUnit.
            
                        FILTER (REGEX(STR(?propertyName), "elastic modulus|young's modulus", "i"))
                        BIND(CONCAT(STR(?propertyName), ": ", STR(?propertyValue)," ", STR(?propertyUnit)) AS ?Mechanical_Property) .
                    """,
                    "Wear Properties":"""
                        ?paper a cs:ColdSprayPaper ;
                            cs:hasResult ?result.
                        ?result cs:hasMechanicalProperty ?mechanical .
                        ?mechanical cs:propertyName ?propertyName .
                        ?mechanical cs:propertyValue ?propertyValue.
                        ?mechanical cs:propertyUnit ?propertyUnit.
            
                        FILTER (REGEX(STR(?propertyName), "wear", "i"))
                        BIND(CONCAT(STR(?propertyName), ": ", STR(?propertyValue)," ", STR(?propertyUnit)) AS ?Mechanical_Property) .
                    """,
                    "Ductility":"""
                        ?paper a cs:ColdSprayPaper ;
                            cs:hasResult ?result.
                        ?result cs:hasMechanicalProperty ?mechanical .
                        ?mechanical cs:propertyName ?propertyName .
                        ?mechanical cs:propertyValue ?propertyValue.
                        ?mechanical cs:propertyUnit ?propertyUnit.
            
                        FILTER (REGEX(STR(?propertyName), "ductility|elongation", "i"))
                        BIND(CONCAT(STR(?propertyName), ": ", STR(?propertyValue)," ", STR(?propertyUnit)) AS ?Mechanical_Property) .
                    """,
                    "Residual Stress":"""
                        ?paper a cs:ColdSprayPaper ;
                            cs:hasResult ?result.
                        ?result cs:hasMechanicalProperty ?mechanical .
                        ?mechanical cs:propertyName ?propertyName .
                        ?mechanical cs:propertyValue ?propertyValue.
                        ?mechanical cs:propertyUnit ?propertyUnit.
            
                        FILTER (REGEX(STR(?propertyName), "residual stress", "i"))
                        BIND(CONCAT(STR(?propertyName), ": ", STR(?propertyValue)," ", STR(?propertyUnit)) AS ?Mechanical_Property) .
                    """,
                    }

                else:
                    custom_mech = st.text_input("Enter a keyword for a mechanical property (e.g., thermal stress, strain at fracture, deposition stress):")
                    query_mech_results = {"Keyword Search":f"""
                                            ?paper a cs:ColdSprayPaper ;
                            cs:hasResult ?result .

                        ?result cs:hasMechanicalProperty ?mechanical .
                        ?mechanical cs:propertyName ?propertyName .
                        ?mechanical cs:propertyValue ?propertyValue .

                        OPTIONAL {{ ?mechanical cs:propertyUnit ?propertyUnit }}

                        FILTER (REGEX(STR(?propertyName), "{custom_mech}", "i"))

                        BIND(
                            CONCAT(
                            STR(?propertyName), ": ",
                            STR(?propertyValue),
                            IF(BOUND(?propertyUnit), CONCAT(" ", STR(?propertyUnit)), "")
                            ) AS ?Mechanical_Property
                        )
                                            """,
                                        
                                        }
                    

            else:
                query_mech_results = {"None":"""""",}    
                


            #if selected_result_query == "Microstructure":
            #        prologue_text = prologue_text + "?featureDescription " + "?featureValue " + "?featureUnit" 

    elif paper_type == "Numerical":
        numerical_query = """

                ?paper a cs:ColdSprayPaper ;
                    cs:hasComputationalStudy ?x .

                """
        with st.expander(f"#### Advanced Search", expanded = True):
            selected_model_materials_query = st.selectbox("Model Material", ["any", "Aluminum and Aluminum Alloys", "Copper and Copper Alloys", "Nickel and Nickel Alloys", "Titanium and Titanium Alloys", "Iron and Steel Alloys", "Magnesium and Magnesium Alloys", "Carbides", "Keyword Search"]) 

            if query_model_materials[selected_model_materials_query] != "":
                prologue_text = prologue_text + "?Model_Material" 

            if selected_model_materials_query == "Keyword Search":
                custom_model_material = st.text_input("Enter material keyword:")
                query_model_materials = {
                
                "Keyword Search":f"""

            ?paper a cs:ColdSprayPaper ;
                cs:hasComputationalStudy ?comp .
            ?comp cs:modelsMaterial ?Model_Material .

            FILTER (regex(?Model_Material, "{custom_model_material}"))

        """,
                        }
            approachcol1, approachcol2 = st.columns([1.2, 3])
            with approachcol1:
                approach_check = st.checkbox("Numerical Approach", value = True)
            with approachcol2:
                custom_approach_type = st.text_input("", label_visibility="collapsed", placeholder="Leave blank to show all, or enter a numerical approach")
            if approach_check:
                prologue_text = prologue_text + "?Numerical_Approach"

                if custom_approach_type == "":
                    approach_query = """
                    OPTIONAL{
                    ?paper a cs:ColdSprayPaper ;
                        cs:hasComputationalStudy ?approach .
                    ?approach cs:hasNumericalApproach ?approach2 .
                    ?approach2 cs:approachType ?Numerical_Approach .
                    }
                    """
                else:
                    approach_query = f"""
                    
                    ?paper a cs:ColdSprayPaper ;
                        cs:hasComputationalStudy ?approach .
                    ?approach cs:hasNumericalApproach ?approach2 .
                    ?approach2 cs:approachType ?Numerical_Approach .

                    FILTER (REGEX(STR(?Numerical_Approach), "{custom_approach_type}", "i"))
                    
                    """

            conscol1, conscol2 = st.columns([1.2, 3])
            with conscol1:
                cons_check = st.checkbox("Constitutive Model", value = True)
            with conscol2:
                custom_cons = st.text_input("", label_visibility="collapsed", placeholder="Leave blank to show all, or enter a constitutive model")
            if cons_check:
                prologue_text = prologue_text + "?Constitutive_Model"

                if custom_cons == "":
                    cons_query = """
                    OPTIONAL{
                    ?paper a cs:ColdSprayPaper ;
                        cs:hasComputationalStudy ?cons .
                    ?cons cs:hasNumericalApproach ?cons2 .
                    ?cons2 cs:hasApproachDetail ?cons3 .
                    ?cons3 cs:constitutiveModel ?Constitutive_Model .
                    }
                    """
                else:
                    cons_query = f"""
                    
                    ?paper a cs:ColdSprayPaper ;
                        cs:hasComputationalStudy ?cons .
                    ?cons cs:hasNumericalApproach ?cons2 .
                    ?cons2 cs:hasApproachDetail ?cons3 .
                    ?cons3 cs:constitutiveModel ?Constitutive_Model .

                    FILTER (REGEX(STR(?Constitutive_Model), "{custom_cons}", "i"))
                    
                    """

            
            dimcol1, dimcol2 = st.columns([1.2, 3])
            with dimcol1:
                dim_check = st.checkbox("Dimensionality", value = True)
            with dimcol2:
                dim_select = st.selectbox("", ["all", "1D", "2D", "3D"], label_visibility = "collapsed")
            if dim_check:
                prologue_text = prologue_text + "?Dimensionality"
                if dim_select == "all":
                    dim_query = """
                    OPTIONAL{
                    ?paper a cs:ColdSprayPaper ;
                        cs:hasComputationalStudy ?dim .
                    ?dim cs:hasNumericalApproach ?dim2 .
                    ?dim2 cs:dimensionality ?Dimensionality .
                    }
                    """
                else:
                    dim_query = f"""
                    
                    ?paper a cs:ColdSprayPaper ;
                        cs:hasComputationalStudy ?dim .
                    ?dim cs:hasNumericalApproach ?dim2 .
                    ?dim2 cs:dimensionality ?Dimensionality .

                    FILTER (regex(?Dimensionality, "{dim_select}"))
                    
                    """

            softcol1, softcol2 = st.columns([1.2, 3])
            with softcol1:
                soft_check = st.checkbox("Software", value = True)
            with softcol2:
                custom_soft = st.text_input("", label_visibility="collapsed", placeholder="Leave blank to show all, or enter a software")
            if soft_check:
                prologue_text = prologue_text + "?Software"

                if custom_soft == "":
                    soft_query = """
                    OPTIONAL{
                    ?paper a cs:ColdSprayPaper ;
                        cs:hasComputationalStudy ?soft .
                    ?soft cs:usesSoftware ?Software .
                    }
                    """
                else:
                    soft_query = f"""
                    
                    ?paper a cs:ColdSprayPaper ;
                        cs:hasComputationalStudy ?soft .
                    ?soft cs:usesSoftware ?Software .

                    FILTER (REGEX(STR(?Software), "{custom_soft}", "i"))
                    
                    """

            meshcol1, meshcol2 = st.columns([1.2, 3])
            with meshcol1:
                mesh_check = st.checkbox("Mesh Resolution", value = True)
            if mesh_check:
                prologue_text = prologue_text + "?Mesh_Resolution"

                mesh_query = """
                OPTIONAL{
                ?paper a cs:ColdSprayPaper ;
                    cs:hasComputationalStudy ?mesh .
                ?mesh cs:hasNumericalApproach ?mesh2 .
                ?mesh2 cs:hasApproachDetail ?mesh3 .
                ?mesh3 cs:meshResolution ?Mesh_Resolution .
                }
                """

            constantcol1, constantcol2 = st.columns([1.2, 3])
            with constantcol1:
                constant_check = st.checkbox("Model Constants", value = False)
            if constant_check:
                prologue_text = prologue_text + "?Model_Constant " + "?Model_Constant_Source"

                constant_query = """
                OPTIONAL{
                ?paper a cs:ColdSprayPaper ;
                    cs:hasComputationalStudy ?const .
                ?const cs:hasNumericalApproach ?const2 .
                ?const2 cs:hasApproachDetail ?const3 .
                ?const3 cs:hasModelingConstant ?const4 .
                ?const4 cs:parameterName ?constpara .
                ?const4 cs:parameterValue ?constval .
                ?const4 cs:parameterUnit ?constunit .
                OPTIONAL{
                ?const4 cs:derivedFromSourceTitle ?Model_Constant_Source .
                }
                BIND(
                CONCAT(
                STR(?constpara), ": ",
                STR(?constval),
                IF(BOUND(?constunit), CONCAT(" ", STR(?constunit)), "")
                ) AS ?Model_Constant
                )
                }
                """

                     



    title_text = """
    ?paper a cs:ColdSprayPaper ;
         cs:hasDOI ?nDOI ;
         cs:hasMetadata ?metadata .
         BIND(CONCAT("https://doi.org/", STR(?nDOI)) AS ?DOI) .
         
         
  ?metadata a cs:Metadata ;
            cs:hasTitle ?Title ;
            cs:hasPublicationYear ?Year .
  """
    if custom_author_query != "":
            prologue_text = prologue_text + "?Author "
            author_query = f"""
            ?metadata a cs:Metadata ;
                cs:hasAuthor ?Author .
            FILTER (regex(?Author, "{custom_author_query}", "i"))    

            """

    if custom_doi_query != "":
        title_text = title_text + "\n" + f"""FILTER (REGEX(STR(?DOI), "{custom_doi_query}"))"""

    query_text = prologue_text + "\n WHERE {" + title_text + author_query + experimental_query + query_materials[selected_materials_query] + query_preprocessing[selected_preprocessing_query] + coldspray_text + query_characterization[selected_characterization_query] + query_mic_results[selected_mic_result_query] + query_mech_results[selected_mech_result_query] + numerical_query + query_model_materials[selected_model_materials_query]  + approach_query + dim_query + cons_query + soft_query + mesh_query + constant_query + "}" + "\n" + "ORDER BY DESC(?Year)"
    #+ query_approach_type[selected_approach_type_query]
    if st.button("Run Query"):
        with st.spinner("Querying the database, large or complex queries may take longer...", show_time = False):
            df = run_query(g, query_text)
            #st.dataframe(df)
            
            df_display = df.copy()
            if custom_author_query != "":
                df_display.loc[df_display.duplicated(subset=["Year", "DOI", "Title", "Author"]), ["Year","DOI", "Title", "Author"]] = ""
            else:    
                df_display.loc[df_display.duplicated(subset=["Year", "DOI", "Title"]), ["Year","DOI", "Title"]] = ""
            #st.dataframe(df_display, use_container_width=True)
            df_display.insert(0, " ", "")
            row_numbers = (~df_display["DOI"].eq("")).cumsum()  # count only when DOI not blank
            df_display.loc[df_display["DOI"] != "", " "] = row_numbers[df_display["DOI"] != ""].astype(str)
            st.data_editor(
                df_display,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "DOI": st.column_config.TextColumn(width="medium"),
                    "Title": st.column_config.TextColumn(width="large"),
                },
                disabled=True,  # makes it behave like dataframe
            )

            #group_keys = ["DOI", "Title"]
            #value_columns = [c for c in df.columns if c not in group_keys]
            #agg_rules = {col: lambda x: ", ".join(sorted(set(map(str, x.dropna())))) for col in value_columns}
            #grouped = df.groupby(group_keys).agg(agg_rules).reset_index()
            #st.dataframe(grouped)
        
    #st.markdown("---")
    #with st.expander("Custom Query"):
    #    st.markdown("The selections above generated the SPARQL query below. You may modify it or enter your own custom SPARQL query.")
    #    st.code(query_text, language="sparql")

    #custom_query = st.text_area("Enter your SPARQL Query here", height=200)
    #if st.button("Run Custom Query"):
    #    try:
    #        df = run_query(g, custom_query)
    #        st.dataframe(df)
    #    except Exception as e:
    #        st.error(f"Query failed: {e}")
        #st.subheader("Query")


    
