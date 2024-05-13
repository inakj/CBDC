# CBDC
CBDC -  Concrete Beam design checker is a Python tool to control capacity for a concrete beam. The tool consist of a collection of scripts made in Python using object oriented programming. The script apply for a simply supported beam with evenly distrubuted self-load and live-load, with either one layer of ordinary reinforcement, one layer of prestressed reinforcement or a combination of these. The cross section must be rectangular. The script control capacity in SLS and ULS. The calculation is done according to Eurocode 2 and the book 'Betongkonstruksjoner' by Stein Ivar Sørensen.

All scripts are listed and explained below.

# A0_Input
Contain the class called 'Input'
All input for the script is given here by the user.
All values with a comment are where your input should be. Do not change the code or write something where there is no comments.
Returns:
        - Material -
        concrete_class(str):  concrete class, characteristic strength of concrete 
        steel_class(str):  steel class, characteristic strenght of steel
        cement_class(str):  cement class
        relative_humidity(int):  relative humidity around beam
        exposure_class(str):   exposure class
        - Geometry -
        width(float):  width [mm]
        height(float):  height [mm]
        beam_length(float): length [m]
        - Reinforcement -
        nr_ordinary_reinforcement_bars(int):  nr of ordinary reinforcement bars
        ordinary_reinforcement_diameter(float):  ordinary reinforcement diameter mm]
        stirrup_diameter(float):  diameter of stirrup diameter / shear reinforcement [mm]
        shear_reinforcement(float):  shear reinforcement / stirrup reinforcement [mm2] / [mm]
        - Load -
        distributed_selfload(float):  characteristic selfload [kN/m]
        selfload_application(int):  when self-load is applied[days]
        distributed_liveload(float): characteristic liveload [kN/m]
        liveload_application(int):  when live-load is applied [days]
        percent_longlasting_liveload(int):  longlasting live-load [%]
        - Prestress - 
        is_the_beam_prestressed(bool):  True or False
        nr_prestressed_bars(int):  nr of prestressed reinforcement bars
        prestressed_reinforcment_diameter(float):  prestressed reinforcement diameter [mm]
        prestressed_reinforcment_name(str):  name of prestressed reinforcement
        - Prestress and ordinary -
        prestressed_and_ordinary_in_top(bool):  True or False

# A0_Results
This script contain the Beam class that takes inn all other classes, makes instances of them and then control the relevant attributes regarding ULS and SLS.
First the script import all classes from their respective scripts. Then the the beam class is made with the input from the Input script. This class give out instances based on how the beam is reinforced.
The script use if-else sentences to differentiate between ordinary reinforced, prestressed, or both.
At the end of the script, the results of the ULS and SLS checks are printed based on the results from the Beam class.

Args:
            Input:  Instance with all input defined by the user in the Input script
Returns:
            material_instance:  Instance for the material based on the inputs  
            cross_section_instance:   Instance for the cross section based on the inputs  
            load_instance:   Instance for the load based on the inputs  
            creep_instance:   Instance for the creep number based on the inputs  
            deflection_instance:   Instance for the deflection based on the inputs  
            stress_uncracked_instanc:  Instance for the stress for prestressed, uncracked cross section based on the inputs 
            stress_cracked_instance:  Instance for the stress for prestressed,cracked cross section based on the inputs  
            stress_instance:  Instance for the stress for prestressed cross section based on the inputs
            ULS_instance:  Instance for the ULS calculations based on the inputs
            crack_instance:  Instance for the crack width based on the inputs
            reinforcement_instance:  Instance for the reinforcment based on the inputs 
            time_effect_instance:  Instance for the time effects for prestressed cross section based on the inputs  
            prestressed_and_ordinary_in_top(bool):  True or False
            is_the_beam_prestressed(bool):  True or False
            M_control(str):  Control of moment
            V_control(str):  Control of shear
            As_control(str):  Control of reinforcement
            Asw_control(str):  Control of shear reinforcment
            crack_control(str):  Control of crack widht
            deflection_control(str):  Control of deflection
            stress_control(str):  Control of stress for prestressed cross section
            concrete_emission(float):  Concrete emissions based on the inputs [kg CO2 eq.]
            ordinary_reinforcement_emission(float):  Emissons for ordinary reinforcement based on the inputs [kg CO2 eq.]
            prestressed_reinforcement_emission(float):  Emissions for prestressed reinforcement based on the inputs [kg CO2 eq.]
            total_emission(float):  Total emissions based on the inputs [kg CO2 eq.]
            printed_emission(str):  Printed total emission 
            cost_concrete(float):  Concrete cost based on the inputs [NOK]
            cost_reinforcement(float):  Reinforcement cost bast on the inputs [NOK]
            total_cost(float):  Total cost based on the inputs [NOK]
            printed_cost(str):  Printed total cost
            
# B0_Creep_number
This script contain the Creep number class that apply for all reinforcement cases. Class that contain creep number calculation from EC2, annex B.
Args: 
            cross_section:  instance from Cross section class that contain all cross section properties
            material:  instance from the Material class that conatin all material properties
            t0_self(int):  time of applied self load, from Input class  [days]
            t0_live(int):  time of applied live load, from Input class  [days]
            RH(int):  relative humidity, from Input class [%]
            cement_class(string):  cement class 'N','S' or 'R', from Input class 
            t(int):  concrete age at the considered time, assumed 50 years [days]
Returns: 
            h0(float): effective cross section thickness [mm]
            beta_fcm(float):  factor that takes into account concrete strength 
            phi_RH(float):  factor that takes into account the effect of relative humidity 
            t0_adjusted_self(float):  adjusted selfload application age because of effect from cement type [days]
            t0_adjusted_live(float):  adjusted liveload application age because of effect from cement type [days]
            beta_t0_self(float):  factor that take into acount the effect of concrete age of selfload application
            beta_t0_live(float):  factor that take into acount the effect of concrete age of liveload application
            phi_0_self(float):  standardized creep number for selfload
            phi_0_live(float):  standardized creep number for liveload
            beta_c(float):  factor to describe creep development compared to time after applied load
            phi_self(float):  creep number for selfload
            phi_live(float):  creep number for liveload
            
# B0_Cross_section
This script contain the Cross section class that apply for all reinforcement cases. Class to contain cross section properties used in calculations.
All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2).
Args:
            width(float):  width of cross-section, from Input class [mm]
            height(float):  height of cross-section, from Input class [mm]
            nr_bars(int):  numbers of reinforcement bars in longitudinal direction,from Input class 
            bar_diameter(float):  diameter of each longitudinal reinforcement bar, from Input class  [mm]
            stirrup_diameter(float):  diameter of each reinforcement stirrup, from Input class [mm]
            exposure_class(string):  exposure class to calculate nominal thickness, from Input class 
            prestress_diameter(float):  diameter of one prestressing strand, from Input class [mm2]
            nr_prestressed_bars(int):  number of prestressed reinforcement bars, from Input class 
            material:  instance from Material class that contain all material properties
Returns:
            width(float):  width of cross-section as attribute[mm]
            height(float):  height of cross-section as attribute [mm]
            Ac(float):  concrete area [mm2]
            Ic(float):  second moment of inertia [mm4]
            c_min_b(float):  smallest nominal cover because of bonding [mm]
            c_min_dur(float):  smallest nominal cover because of environmental effects [mm]
            cnom(float):  nominal concrete cover [mm]
            As(float): area of reinforcement [mm2]
            d_1(float):  effective height from compression edge to reinforcement center for ordinary reinforcement[mm]
            d_2(float):  effective height from compression edge to reinforcement center for prestressed reinforcement[mm]
            e(float):  distance from bottom to middle of prestressed reinforcement [mm]
            Ap(float):  prestressed reinforcement area in cross section [mm2]    
            
# B0_Load
This script contain the Load properties class that apply for all reinforcement cases. Load class to contain load properties used in calculations. 
All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2).
Args:
            selfload(float):  concrete beam's self weight, from Input class [kN/m]
            liveload(float):  applied load, from Input class [kN/m]
            length(float):  length of beam, from Input class [m]
            material:  instance from Material class that contain all material properties
            cross_section:  instance from Cross section class that contain all cross section properties
Returns: 
            g_k(float):  characteristic selfload [kN/m]
            p_k(float):  characteristic liveload [kN/m]
            q_k(float):  characteristic load [kN/m]
            g_d(float):  design selfload, including load factor [kN/m]
            p_d(float):  design liveload, including load factor [kN/m]
            q_d(float):  design load, including load factor [kN/m]
            Mg_k(float):  max moment in middle of beam because of characteristic selfload [kNm]
            Mp_k(float):  max moment in middle of beam because of characteristic liveload [kNm]
            M_k(float):  max total moment in middle of beam because of characteristic load [kNm]
            Mg_d(float):  max moment in middle of beam because of design selfload [kNm]
            Mp_d(float):  max moment in middle of beam because of design live load [kNm]
            M_Ed(float):  max total moment in middle of beam because of design load [kNm]
            V_k(float):  max shear force near supports because of characteristic total load [kN]
            V_Ed(float):  max shear force near supports becasue of design total load [kN]
            sigma_p_max(float):  design value of prestressing stress [N/mm2]
            P0_d(float):   design value of prestressign force [N]
            M_prestress(float):  moment because of prestressing force included loss [kNm]

# B0_Material
This script contain the Material class that apply for all reinforcement cases. Material class to contain material properties used in calculations.
All calculations are done according to the standards NS-EN 1992-1-1:2004 (abbreviated to EC2), NS-EN 1990:2002 and EN10138-3.
Args:
            concrete_class (str): concrete class, from Input class 
            steel_class (str): steel class, from Input class 
            prestress_name (str): name of prestress type, from Input class , according to table 2 in EN10138-3
            prestress_diameter (float): diameter of prestressed reinforcement, from Input class , according to table 2 in EN10138-3
Returns:
            - Load- and materialfactor attributes -
            gamma_shrinkage(float):  loadfactor for shrink
            gamma_0_9(float):  loadfactor for prestressing
            gamma_1_1(float):  loadfactors for prestressing
            gamma_selfload(float):  loadfactor for self-load
            gamma_liveload(float):  loadfactor for live-load
            gamma_concrete(float):  materialfactor for concrete
            gamma_reinforcement(float):  materialfactor for ordinary reinforcement steel
            gamma_prestressed_reinforcement(float):  materialfactor for prestressed reinforcement steel 
            - Concrete attributes - 
            fck(int):  cylinder compression strength [N/mm2] 
            fck_cube(int):  Cubic compressive strength [N/mm2]
            fcm(int):  middlevalue of cylinder compressive strength [N/mm2]
            fctm(float):  middlevalue of concrete axial tension strength [N/mm2]
            fctk_005(float):  0.05 % concrete characteristic axial tension strength [N/mm2]
            fctk_095(float):  0.95 % concrete characteristic axial tension strenght [N/mm2]
            Ecm(int):  Elasticity modulus for concrete [N/mm2]
            eps_c1(float):  compression strain for biggest stress 
            eps_cu1(float):  strain limit for compression
            eps_c2(float):  compression strain for biggest stress 
            eps_cu2(float):  strain limit for compression
            n(float):  exponent
            eps_c3(float):  compression strain for biggest stress 
            eps_cu3(float):  strain limit for compression 
            lambda_factor(float):  factor for effective height
            netta(float):  factor for effective strength
            alfa_cc(float):  design compressive strength coefficient
            alfa_ct(float):  design tensile strength coefficient 
            fcd(float):  design compressive strength [N/mm2]
            fctd(float):  design tensile strength [N/mm2]
            - Ordinary reinforcement attributes -
            fyk(int):  steel tensions characteristic strength [N/mm2]
            Es(int):  elasiticity modulus for steel [N/mm2]
            eps_yk(float):  characteristic yield strain
            fyd(float):  design tensile strength
            eps_yd(float):  design yield strain
            - Prestressed reinforcement attributes -
            Ep(int):  elasticity moduls for prestensioned steel [N/mm2]
            fpk(int):  tensile strength for prestress [N/mm2]
            Ap(float):  cross sectional area for prestress [mm2] 
            Fpk(float):  characteristic maximum force for prestressing [kN] 
            Fp01k(float):  characteristic 0.1% proof force [kN] 
            fp01k(float):  characteristic 0.1% proof stress [N/mm2] 
            fpd(float):  design 0.1% proof stress [N/mm2] 
            
# C1_ULS
This script contain the ULS class that apply for ordinary reinforced cross section.
Class to contain all relevant ultimate limit state (ULS) controls. 
Calculations are based on following assumptions from EC2 6.1(2)P:
    - Full bond between concrete and reinforcement
    - Naviers hypothesis
    - Stress-strain properties from EC 3.1.7, figure 3.5
    - Ignore concrete tension strength 
Assumed that the ultimate failure criterion is compression failure in concrete. All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Sørensen. 
Args:
            cross_section:  instance for Cross sectino class that contain all cross-section properties
            material:  instance for Caterial class that contain all material properties
            load:  instance for Load properties class that contain all load properties
            Asw(float):  area of shear reinforcement, from Input class  [mm2/mm] 
Returns:
            alpha(float):  Compression-zone-height factor
            M_Rd(float):  Moment capacity of beam [kNm]
            V_Rd(float):  Shear force capacity of beam [kNm]
            M_control(bool):  Control of moment capacity, return True or False 
            V_control(bool):  Control of shear force capacity, return True or False 
            M_utilization(float):  utilization degree for moment capacity [%]
            V_utilization(float):  utilization degree for shear capacity [%]

# C2_ULS
This script contain the ULS class that apply for prestressed reinforced cross section. Class to contain all relevant ultimate limit state (ULS) controls for prestressed cross section. All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Sørensen. 
Args:
            material:  instance for Material class that contain all material properties
            load:  instance for Load properties class that contain all load properties
            cross_section:  instance for Cross section class that contain all cross-section properties
            time_effect:  instance for Time effect class that contain all time effect losses
            Asw(float):  area of shear reinforcement, from Input class  [mm2/mm] 
Returns:
            eps_diff(float):  effective change differance beacuse of strain loss 
            alpha(float):  Compression-zone-height factor
            M_Rd(float):  moment capacity [kNm]
            M_control(bool):  Control of moment capacity, return True or False 
            V_Rd(float):  shear capacity [kN]
            V_control(bool):  Control of shear force capacity, return True or False
            M_utilization(float):  utilization degree for moment capacity [%]
            V_utilization(float):  utilization degree for shear capacity [%]

# C3_ULS
This script contain the ULS class that apply for prestressed reinforced cross section with ordinary reinforcement in top. Class to contain all relevant ultimate limit state (ULS) controls for prestressed cross section with ordinary reinforcement in top. All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Sørensen. 
Args:
            material:  instance for Material class that contain all material properties
            load:  instance for Load properties class that contain all load properties
            cross_section:  instance for Cross section class that contain all cross-section properties
            time_effect:  instance for Time effect class that contain all time effect losses
            Asw(float):  area of shear reinforcement, from Input class  [mm2/mm] 
Returns:
            eps_diff(float):  effective change differance beacuse of strain loss 
            alpha(float):  Compression-zone-height factor
            M_Rd(float):  moment capacity [kNm]
            control_M(boolean):  Control of moment capacity, return True or False 
            V_Rd(float):  shear capacity [kN]
            control_V(boolean):  Control of shear force capacity, return True or False
            M_utilization(float):  utilization degree for moment capacity [%]
            V_utilization(float):  utilization degree for shear capacity [%]

# D1_Reinforcement
This script contain the reinforcement classs that apply for ordinary reinforced cross section. Class to contain all reinforcement controls for ordinary reinforced cross section. All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Svein Ivar Sørensen.
Args: 
            cross_section:  instance for Cross sectino class that contain all cross-section properties
            material:  instance for Caterial class that contain all material properties
            load:  instance for Load properties class that contain all load properties
            ULS_nonprestressed:  instance for ULS class that contain all ULS control for ordinary reinforcement
            Asw(float):  area of shear reinforcement, from Input class  [mm2/mm] 
Returns: 
            As_necessary(float):  Necessary reinforcement [mm2]
            As(float):  Minimum reinforcement [mm2]
            As_max(float):  Maximum reinforcement [mm2]
            A_control(boolean):  Control of reinforcement, return True or False
            Asw_control(boolean):  Control of shear reinforcement, return True or False
            utilization:  utilization degree for reinforcement [%]
            utilization_shear:  utilization degree for shear reinforcement [%]

# D2_Reinforcement
This script contain the reinforcement classs that apply for prestressed reinforced cross section. Class to contain all reinforcement controls for prestressed cross section. All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Svein Ivar Sørensen.
Args: 
            cross_section:  instance for Cross sectino class that contain all cross-section properties
            material:  instance for Caterial class that contain all material properties
            load:  instance for Load properties class that contain all load properties
            ULS_prestressed:  instance for ULS prestressed class that contain all ULS control for prestressed reinforcement
            Asw(float):  area of shear reinforcement, from Input class  [mm2/mm] 
Returns: 
            As(float):  Minimum reinforcement [mm2]
            Asw_control(boolean):  Control of shear reinforcement, return True or False
            Ap_necessary(float):  area of prestress reinforcement necessary [mm2]
            A_control(boolean):  Control of prestress reinforcement area, return True or False
            utilization:  utilization degree for reinforcement [%]
            utilization_shear:  utilization degree for shear reinforcement [%]
  
# E1_SLS_Crack
This script contain the Crack control class that apply for ordinary reinforced cross section. Class to contain crack control in Service limit state (SLS) for ordinary reinforced cross section. All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Svein Ivar Sørensen.
Args:
            cross_section:  instance for Cross sectino class that contain all cross-section properties
            load:  instance for Load properties class that contain all load properties
            material:  instance for Material class that contain all material properties
            exposure_class(string):  exposure class to calculate nominal thickness, from Input class
            creep_number:  instance for Creep number class that contain creep number 
            bar_diameter(float):  rebar diameter, from Input class [mm]
Returns: 
            k_c(float):  factor that take into consideration the ratio between cnom and cmin,dur
            crack_width(float):  limit value of crack width [mm]
            alpha(float):  factor for calculating reinforcment stress
            sigma_s(float):  reinforcement stress [N/mm2]
            max_bar_diameter(float):  maximum bar diameter to limit crack width [mm
            control_bar_diameter(boolean):  control of bar diameter, return True or False

# E2_SLS_Crack
This script contain the Crack control class that apply for prestressed reinforced cross section. Class to contain crack control in Service limit state (SLS) for prestressed cross section. All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Svein Ivar Sørensen. 
Args:
            cross_section:  instance for Cross sectino class that contain all cross-section properties
            load:  instance for Load properties class that contain all load properties
            material:  instance for Material class that contain all material properties
            exposure_class(string):  exposure class to calculate nominal thickness, from Input class
            stress:  instance for Stress class that contain stress in cross section
            prestress_bar_diameter(float):  diameter of prestressed rebar, from Input class[mm]
Returns: 
            k_c(float):  factor that take into consideration the ratio between cnom and cmin,dur
            crack_width(float):  limit value of crack width [mm]
            alpha(float):  factor for calculating reinforcment stress
            sigma_p(float):  reinforcement stress [N/mm2]
            max_bar_diameter(float):  maximum bar diameter to limit crack width [mm]
            control_bar_diameter(boolean):  control of bar diameter, return True or False

# F1_SLS_Deflection
This script contain the Deflection class that apply for ordinary reinforced cross section. Class to contain deformation for ordinary reinforced cross section. All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Svein Ivar Sørensen.
Args:
            cross_section:  instance from Cross section class that contain all cross-section properties
            material:  instance from Material class that contain all material properties
            load:  instance from Load properties class that contain all load properties
            creep:  class that contain creep number phi for self- and liveload
            factor(float):  percentage of live load that is long lasting, from Input class[%]
            length(float):  length of beam, from Input class [m]
            RH(int):  relative humidity, from Input class [%]
            cement_class(str):  cement class 'N','S' or 'R', from Input class
Returns:
            Ec_middle(float):  middle elasticity modulus [N/mm2]
            netta(float):  factor to calculate alpha
            ro(float):  factor to calculate alpha
            alpha_uncracked(float):  factor for uncracked cross section
            EI_1(float):  bending stiffness for uncracked cross section [Nmm2]
            deflection_uncracked(float):  deflection including creep for cracked cross section [mm]
            alpha_cracked(float):  factor for cracked cross section
            EI_2(float):  bending stiffnes for cracked cross section [Nmm2]
            deflection_cracked(float):  deflection including creep for cracked cross section [mm]
            M_cr(float):  crack moment [kNm]
            control_Mcr(bool)  True if cracked cross section. False if uncracked cross section
            eps_cd(float):  shrinkage strain due to drying over time
            eps_ca(float):  autogenous shrinkage strain
            eps_cs(float):  total shrinkage strain
            K_s(float):  curvature because of shrinkage [mm-1]
            deflection_shrinkage(float):  delfection only because of shrinkage [mm]
            total_deflection(float):  deflection including both shrinkage and creep, with tension stiffening [mm]
            control_deflection(boolean):  Return true if the deflection is within the limit, and False
            if the deflection is to big
        
# F2_SLS_Deflection
This script contain the Deflection class that apply for prestressed reinforced cross section. Class to contain deformation for prestressed cross section.
All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Svein Ivar Sørensen. 
Args:
            cross_section:  instance from Cross section class that contain all cross-section properties
            material:  instance from Material class that contain all material properties
            load:  instance from Load properties class that contain all load properties
            creep_number:  class that contain creep number phi for self- and liveload
            factor(float):  percentage of live load that is long lasting, from Input class[%]
            length(float):  length of beam, from Input class [m]
            RH(int):  relative humidity, from Input class [%]
            cement_class(str):  cement class 'N','S' or 'R', from Input class
            time_effect:  instance from Time effects class that contain all time dependant losses
Returns:
            Ec_middle(float):  middle elasticity modulus [N/mm2]
            netta(float):  factor to calculate alpha
            ro(float):  factor to calculate alpha
            alpha_uncracked(float):  factor for uncracked cross section
            EI_1(float):  bending stiffness for uncracked cross section [Nmm2]
            deflection_uncracked(float):  deflection including creep for cracked cross section [mm]
            alpha_cracked(float):  factor for cracked cross section
            EI_2(float):  bending stiffnes for cracked cross section [Nmm2]
            deflection_cracked(float):  deflection including creep for cracked cross section [mm]
            M_cr(float):  crack moment [kNm]
            control_Mcr(float)  True if cracked cross section. False if uncracked cross section
            eps_cd(float):  shrinkage strain due to drying over time
            eps_ca(float):  autogenous shrinkage strain
            eps_cs(float):  total shrinkage strain
            K_s(float):  curvature because of shrinkage [mm-1]
            deflection_shrinkage(float):  delfection only because of shrinkage [mm]
            total_deflection(float):  deflection including both shrinkage and creep, with tension stiffening [mm]
            control_deflection(boolean):  Return true if the deflection is within the limit, and False
            if the deflection is to big
            
# G2_SLS_Cracked
This script contain the Cracked stress class that apply for prestressed reinforced cross section.
Class to contain calculation of cracked prestressed cross section. All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Svein Ivar Sørensen.
Args:
            cross_section:  instance from Cross section class that contain all cross-section properties
            material:  instance from Material class that contain all material properties
            load:  instance from Load properties class that contain all load properties 
            deflection:  instance from Deflection prestressed class that contain deflection control 
            time_effect:  instance from Time effect class that contain time effects because of shrink, creep and relaxation
            creep_number:  instance from Creep number class that contain creep number calculations
Returns:    
            E_middle(float):  middle elasticity modulus [N/mm2]
            netta(float):  material stiffness ratio 
            ro(float):  Reinforcement ratio 
            Ns(float):  axial force because of free shrink [kN]
            a(float):  ratio between moment and axial force [mm]
            alpha(float):  factor for calculating stresses
            sigma_c(float):  stress in concrete top [N/mm2]
            
# H2_SLS_Uncracked
This script contain the Uncracked stress class that apply for prestressed reinforced cross section.
Class to contain calculation of uncracked prestressed
    cross section. All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the 
    book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Svein Ivar Sørensen.
Args:
            cross_section:  instance from Cross section class that contain all cross-section properties
            material:  instance from Material class that contain all material properties
            load:  instance from Load properties class that contain all load properties 
Returns:    
            netta(float):  material stiffness ratio 
            At(float):  transformed cross section area [mm2]
            yt(float):  distance between reinforced gravity axis and concrete gravity axis [mm]
            It(float):  moment of inertia for tranforsmed cross section [mm4]
            sigma_c_uncracked(float):  concrete stress for uncracked cross section [N/mm2]
        
# H3_SLS_Uncracked
This script contain the Uncracked stress class that apply for prestressed and ordinary reinforced cross section. Class to contain calculation of uncracked prestressed and ordinary reinforced cross section. All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the 
book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Svein Ivar Sørensen.
Args:
            cross_section:  instance from Cross section class that contain all cross-section properties
            material:  instance from Material class that contain all material properties
            load:  instance from Load properties class that contain all load properties 
            stirrup_diameter(float):  diameter of stirrup around the longitudinal bars [mm]  
            bar_diameter(float):  diameter of ordinary reinforcement bars in longitudinal direction [mm]
Returns:    
            netta_p(float):  material stiffness ratio for prestressed reinforcement
            netta_s(float):  material stiffness ratio for ordinary reinforcement
            At(float):  transformed cross section area [mm2]
            yt(float):  distance between reinforced gravity axis and concrete gravity axis [mm]
            It(float):  moment of inertia for tranforsmed cross section [mm4]
            sigma_c_uncracked(float):  concrete stress for uncracked cross section [N/mm2]

# I2_SLS_Stress
This script contain the Stress class that apply for prestressed reinforced cross section. Class to contain calculation stress calculation for prestressed cross section. Include calculations from both Uncracked and Cracked Stress Class. All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Svein Ivar Sørensen.
Args:
            material:  instance for Material class that contain all material properties
            deflection:  instance for Deflection class that contain deflection control 
            uncracked_stress:  instance for Uncracked sress class that contain stress calculation for uncracked cross section
            cracked_stress:  instance for Cracked stress class that contain stress calculation for cracked cross section
            load:  instance for Load properties class that contain all load properties 
            time_effect:  instance for Time effects class that contain time effects because of shrink, creep and relaxation
Returns:    
            sigma_p_uncracked(float):  reinforcement stress for uncracked cross section [N/mm2]
            sigma_p_cracked(float):  reinforcement stress for cracked cross section [N/mm2]
            control(bool):  control of concrete stress, return True or False
            
# J2_Time_Effects
This script contain the Time effects class that apply for prestressed reinforced cross section. Class to contain losses that is caused by time, including shrink, creep and relaxation. All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Svein Ivar Sørensen.
Args:
            material:  instance from Material class that contain all material properties
            cross_section:  instance from Cross section class that contain all cross-section properties
            creep_number:  instance from Creep number class that contain creep number calculation
            Stress_uncracked:  instance from Uncracked stress class that contain control of prestressed uncracked cross section
            deflection:  instance from Deflection class that contain all calculations for deflection
            load:  instance from Load properties class that contain all load properties 
Returns:
            delta_relaxation(float):  loss in stress because of relaxation [N/mm2]
            loss(float):  stress reduction in prestress because for relaxation, shrink and creep [N/mm2]
            loss_percentage(float):  stress reduction in prestress because for relaxation, shrink and creep [%]

        
