
'''
---OVERVIEW OF RESULT SCRIPT---

This script contain the Beam class that takes inn all other classes, makes instances of them and then control the relevant attributes regarding ULS and SLS.
First the script import all classes from their respective scripts. Then the the beam class is made with the input from the Input script. This class give out instances based on how the beam is reinforced.
The script use if-else sentences to differentiate between ordinary reinforced, prestressed, or both.
At the end of the script, the results of the ULS and SLS checks are printed based on the results from the Beam class.

'''

from A0_Input import Input # From the Input script, import the Input class (for all reinforcement patterns)
from B0_Material import Material # From the Material script, import the Material Class (for all reinforcement patterns)
from B0_Cross_section import Cross_section # From the Cross section script, import the Cross section class (for all reinforcement patterns)
from B0_Load import Load_properties # From the Load script, import the Load properties class (for all reinforcement patterns)
from C1_ULS import ULS # From the ULS script, import the ULS class (for ordinary reinforcement)
from D1_Reinforcement import Reinforcement_control # From the Reinforcement script import the Reinforcement control class(for ordinary reinforcement)
from E1_SLS_Crack import Crack_control # From the SLS Crack script, import the Crack Control class (for ordinary reinforcement)
from F1_SLS_Deflection import Deflection # From the SLS Deflection script, import the Deflection class (for ordinary reinforcement)
from B0_Creep_number import Creep_number # From the Creep Number script, import the Creep Number CLass (for all reinforcment patterns)
from D2_Reinforcement import Reinforcement_control_prestressed # From the Reinforcemnt script, import the Reinforcement control prestressed class (for prestressed reinforcement)
from E2_SLS_Crack import Crack_control_prestressed # From the SLS Crack script, import the Crack Control prestressed class (for prestressed reinforcement)
from F2_SLS_Deflection import Deflection_prestressed # From the SLS Deflection script, import the Deflection prestressed class (for prestressed reinforcement)
from H2_SLS_Uncracked import Uncracked_stress # From the SLS Uncracked script, import the Uncracked stress class (for prestressed reinforcement)
from H3_SLS_Uncracked import Uncracked_stress_prestress_and_ordinary # From the SLS Uncracked script, import the Uncracked stress class (for prestressed and ordinary reinforcement)
from G2_SLS_Cracked import Cracked_Stress # From the SLS Cracked script, import the Cracked stress class (for prestressed reinforcement)
from I2_SLS_Stress import Stress # Fromt the SLS Stress script, import the Stress class (for prestressed reinforcement)
from J2_Time_effects import time_effects # From the Time effects script, import the Time effects class (for prestressed reinforcement)
from C2_ULS import ULS_prestressed # From the ULS script, import the ULS prestressed class (for prestressed reinforcement)
from C3_ULS import ULS_prestress_and_ordinary # From the ULS script, import the ULS prestressed and ordinary class (for prestressed with ordinary reinforcement)


class Beam:
    ''' Class to contain all beam checks related to ULS and SLS.
    '''
    def __init__(self,input):
        '''
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
            cost_reinforcement(float):  Reinforcement cost based on the inputs [NOK]
            total_cost(float):  Total cost based on the inputs [NOK]
            printed_cost(str):  Printed total cost
            
        '''
        # Defines the instances that is common for all cases of reinforcement

        self.material_instance = Material(input.concrete_class, (float(input.steel_class[1:4])), input.prestressed_reinforcment_name, input.prestressed_reinforcment_diameter)
        self.cross_section_instance = Cross_section(input.width, input.height, input.nr_ordinary_reinforcement_bars, input.ordinary_reinforcement_diameter, input.stirrup_diameter,
                                                    input.exposure_class, input.prestressed_reinforcment_diameter, input.nr_prestressed_bars, self.material_instance)
        self.load_instance = Load_properties(input.distributed_selfload, input.distributed_liveload, input.beam_length, self.material_instance, self.cross_section_instance)
        self.creep_instance = Creep_number(self.cross_section_instance, self.material_instance, input.selfload_application, input.liveload_application, input.relative_humidity, input.cement_class)
        self.deflection_instance_1 = Deflection(self.cross_section_instance, self.material_instance, self.load_instance, self.creep_instance, input.percent_longlasting_liveload,
                                                input.beam_length, input.relative_humidity, input.cement_class)

        # If the beam is prestressed, the following inctances and attribute apply to all prestressed beams 

        if input.is_the_beam_prestressed == True:
            
            self.concrete_emission = self.calculate_emissinos_concrete(input)

            # If the beam is NOT prestressed with ordinary reinforcement in top, the following inctances and attributes apply to the beam

            if input.prestressed_and_ordinary_in_top == False:
                
                self.prestressed_and_ordinary_in_top = False
                self.is_the_beam_prestressed = True
                self.stress_uncracked_instance = Uncracked_stress(self.material_instance, self.cross_section_instance, self.load_instance)
                self.time_effect_instance = time_effects(self.material_instance, self.cross_section_instance, self.creep_instance, self.stress_uncracked_instance, self.deflection_instance_1, self.load_instance)
                self.deflection_instance = Deflection_prestressed(self.cross_section_instance, self.material_instance, self.load_instance, self.creep_instance, input.percent_longlasting_liveload,
                                                                  input.beam_length, input.relative_humidity, input.cement_class, self.time_effect_instance)
                self.stress_cracked_instance = Cracked_Stress(self.material_instance, self.cross_section_instance, self.load_instance, self.deflection_instance, self.time_effect_instance, self.creep_instance)
                self.stress_instance = Stress(self.material_instance, self.deflection_instance, self.stress_uncracked_instance, self.stress_cracked_instance, self.load_instance, self.time_effect_instance)
                self.ULS_instance = ULS_prestressed(self.material_instance, self.load_instance, self.cross_section_instance, self.time_effect_instance, input.shear_reinforcement)
                self.crack_instance = Crack_control_prestressed(self.cross_section_instance, self.load_instance, self.material_instance, input.exposure_class, self.stress_instance, input.ordinary_reinforcement_diameter)
                self.reinforcement_instance = Reinforcement_control_prestressed(self.cross_section_instance, self.material_instance, self.load_instance, self.ULS_instance, input.shear_reinforcement)
        

                self.M_control = self.control_M(self.ULS_instance)
                self.V_control = self.control_V(self.ULS_instance)
                self.As_control = self.control_As(self.reinforcement_instance)
                self.Asw_control = self.control_Asw(self.reinforcement_instance)
                self.crack_control = self.control_crack(self.crack_instance)
                self.deflection_control = self.control_deflection(self.deflection_instance)
                self.stress_control = self.control_stress(self.stress_instance)
                self.ordinary_reinforcement_emission = self.calculate_emissions_ordinary_reinforcement(self.reinforcement_instance, 7700, input)
                self.prestressed_reinforcement_emission = self.calculate_emissions_prestressed_reinforcement(7810, self.cross_section_instance, input)
                self.total_emission = round(self.ordinary_reinforcement_emission + self.prestressed_reinforcement_emission + self.concrete_emission, 1)
                self.printed_emission = f'Total emission is {self.total_emission} kg CO2 eq.'
                self.cost_concrete = self.get_cost_concrete(input)

            # If the beam is prestressed with ordinary reinforcement in top, the following inctances and attributes apply to the beam
                
            elif input.prestressed_and_ordinary_in_top == True:
                
                self.is_the_beam_prestressed = True
                self.prestressed_and_ordinary_in_top = True
                self.stress_uncracked_instance = Uncracked_stress_prestress_and_ordinary(self.material_instance, self.cross_section_instance, self.load_instance,input.shear_reinforcement_diameter,input.ordinary_reinforcement_diameter)
                self.time_effect_instance = time_effects(self.material_instance, self.cross_section_instance, self.creep_instance, self.stress_uncracked_instance, self.deflection_instance_1, self.load_instance)
                self.ULS_instance = ULS_prestress_and_ordinary(self.material_instance, self.load_instance, self.cross_section_instance, self.time_effect_instance, input.shear_reinforcement)
                self.M_control = self.control_M(self.ULS_instance)
                self.V_control = self.control_V(self.ULS_instance)
                self.ordinary_reinforcement_emission = self.calculate_emissions_ordinary_reinforcement(self.cross_section_instance, 7700, input)
                self.prestressed_reinforcement_emission = self.calculate_emissions_prestressed_reinforcement(7810, self.cross_section_instance, input)
                self.total_emission = round(self.ordinary_reinforcement_emission + self.prestressed_reinforcement_emission + self.concrete_emission, 1)
                self.printed_emission = f'Total emission is {self.total_emission} kg CO2 eq.'
                self.cost_concrete = self.get_cost_concrete(input)
    
        # If the beam is NOT prestressed, the following inctances and attributes apply to all ordinary reinforced beams 
                  
        else:
            self.is_the_beam_prestressed = False
            self.prestressed_and_ordinary_in_top = False
            self.ULS_instance = ULS(self.cross_section_instance, self.material_instance, self.load_instance, input.shear_reinforcement)
            self.reinforcement_instance = Reinforcement_control(self.cross_section_instance, self.material_instance, self.load_instance, self.ULS_instance, input.shear_reinforcement)
            self.crack_instance= Crack_control(self.cross_section_instance, self.load_instance, self.material_instance, input.exposure_class, self.creep_instance, input.ordinary_reinforcement_diameter)
            self.deflection_instance = self.deflection_instance_1

            self.M_control = self.control_M(self.ULS_instance)
            self.V_control = self.control_V(self.ULS_instance)
            self.As_control = self.control_As(self.reinforcement_instance)
            self.Asw_control = self.control_Asw(self.reinforcement_instance)
            self.crack_control = self.control_crack(self.crack_instance)
            self.deflection_control = self.control_deflection(self.deflection_instance)
            self.concrete_emission = self.calculate_emissinos_concrete(input)
            self.ordinary_reinforcement_emission = self.calculate_emissions_ordinary_reinforcement(self.cross_section_instance, 7700, input)
            self.total_emission = round(self.ordinary_reinforcement_emission + self.concrete_emission, 1)
            self.printed_emission = f'Total emission is {self.total_emission} kg CO2 eq.'
            self.cost_concrete = self.get_cost_concrete(input)
            self.cost_reinforcement = self.get_cost_ordinary_reinforcement(input, self.cross_section_instance, 7700)
            self.total_cost = round(self.cost_concrete + self.cost_reinforcement, 1)
            self.printed_cost = f'Total cost is {self.total_cost} NOK'



    def control_M(self, ULS):
        '''Control of moment capacity for the beam
        Args:
            ULS:  Instance for the ULS calculations based on the inputs
        Returns:
            A string sentence saying if the capacity is suifficient or not, and the safety degree
        '''
        if ULS.M_control == True:
            return f'Moment capacity is suifficient and the safety degree is {ULS.M_safety} %'
        else:
            return f'Moment capacity is not suifficient since safety degree is {ULS.M_safety} %'
        
    def control_V(self, ULS):
        '''Control of shear capacity for the beam
        Args:
            ULS:  Instance for the ULS calculations based on the inputs
        Returns:
            A string sentence saying if the capacity is suifficient or not, and the safety degree
        '''
        if ULS.V_control == True:
            return f'Shear capacity is suifficient and the safety degree is {ULS.V_safety} %'
        else:
            return f'Shear capacity is not suifficient since the safety degree is {ULS.V_safety} %'
        
    def control_As(self, reinforcement):
        '''Control of reinforcement area for the beam
        Args:
            reinforcement:  Instance for the reinforcment based on the inputs 
        Returns:
            A string sentence saying if the reinforcement area is suifficient or not, and the safety degree
        '''
        if reinforcement.control == True:
            return f'Reinforcement area is suifficient and the safety degree is {reinforcement.safety} %'
        else:
            return f'Reinforcement area is not suifficient since the safety degree is {reinforcement.safety} %'

    def control_Asw(self, reinforcement):
        '''Control of shear reinforcement area for the beam
        Args:
            reinforcement:  Instance for the shear reinforcment based on the inputs 
        Returns:
            A string sentence saying if the shear reinforcement area is suifficient or not, and the safety degree
        '''
        if reinforcement.Asw_control == True:
            return f'Shear reinforcement area is suifficient and the safety degree is {reinforcement.safety_shear} %'
        else:
            return f'Shear reinforcement area is not suifficient since the safety degree is {reinforcement.safety_shear} %'

    def control_crack(self, crack):
        '''Control of crack width for the beam
        Args:
            crack:  Instance for the crack width based on the inputs
        Returns:
            A string sentence saying if the crack width is suifficient or not, and the safety degree
        '''
        if crack.control_bar_diameter == True:
            return f'Crack width is suifficient and the utiliation degree is {crack.safety} %'
        else:
            return f'Crack width is not suifficient since the safety degree is {crack.safety}'

    def control_deflection(self, deflection):
        '''Control of deflection for the beam
        Args:
            deflection:  Instance for the deflection based on the inputs  
        Returns:
            A string sentence saying if the deflection is suifficient or not, and the safety degree
        '''
        if deflection.control == True:
            return f'Deflection is suifficient and the safety degree is {deflection.safety} %'
        else:
            return f'Deflection is not suifficient since the safety degree is {deflection.safety} %'
   
    def control_stress(self, stress):
        '''Control of stress for the prestressed beam
        Args:
            stress:  Instance for the stress for prestressed cross section based on the inputs
        Returns:
            A string sentence saying if the stress is suifficient or not, and the safety degree
        '''
        if stress.control == True:
            return f'Stress is suifficient'
        else:
            return f'Stress is not suifficient'

    def calculate_emissinos_concrete(self, input) -> float:
        ''' Calculates kg CO2 equivalents for the beam from concrete
        Args:
            input:  Instance with all input defined by the user in the Input script
        Returns:
            emissions from concrete [kg CO2 eq.]
        '''
        if input.concrete_class in ['C20','C25','C30','C35','C45','C55','C65']:
            match input.concrete_class:
                case 'C20':
                    return 180 * input.width * input.height * 10 ** -6 * input.beam_length
                case 'C25':
                    return 190 * input.width * input.height * 10 ** -6 * input.beam_length
                case 'C30':
                    return 225 * input.width * input.height * 10 ** -6 * input.beam_length
                case 'C35':
                    return 240 * input.width * input.height * 10 ** -6 * input.beam_length
                case 'C45':
                    return 270 * input.width * input.height * 10 ** -6 * input.beam_length
                case 'C55': 
                    return 280 * input.width * input.height * 10 ** -6 * input.beam_length
                case 'C65':
                    return 300 * input.width * input.height * 10 ** -6 * input.beam_length
        else: 
            return 0
            
    def calculate_emissions_ordinary_reinforcement(self, reinforcement, density_ordinary: int, input) -> float:
        ''' Calculates kg CO2 equivalents for the beam from ordinary reinforcement
        Args:
            reinforcement:  Instance for the reinforcment based on the inputs 
            density_ordinary(float):  Density for ordinary reinforcement steel [kg/m3]
            input:  Instance with all input defined by the user in the Input script
        Returns:
            emissions from ordinary reinfrocement[kg CO2 eq.]
        '''
        emission = reinforcement.As * 10 ** -6 * density_ordinary * input.beam_length * 0.34
        return emission
    
    def calculate_emissions_prestressed_reinforcement(self, density_prestressed: int, cross_section, input) -> float:
        ''' Calculates kg CO2 equivalents for the beam from prestressed reinforcment
        Args:
            density_ordinary(float):  Density for prestressed reinforcement steel [kg/m3]
            cross_section:  Instance for the cross section based on the inputs  
            input:  Instance with all input defined by the user in the Input script
        Returns:
            emissions from prestressed reinforcment steel [kg CO2 eq.]
        '''
        emission_prestress = cross_section.Ap * 10 ** -6 * input.beam_length * density_prestressed * 1.86
        return emission_prestress 
    
    def get_cost_concrete(self, input) -> float:
        ''' Calculates cost for the beam from concrete
        Args:
            input:  Instance with all input defined by the user in the Input script
        Returns:
            cost of concrete [NOK]
        '''
        if input.concrete_class in ['C20','C30','C35','C45']:
            match input.concrete_class:
                case 'C20':
                    return 1613 * input.width * input.height * 10 ** -6 * input.beam_length
                case 'C25':
                    return 1668 * input.width * input.height * 10 ** -6 * input.beam_length
                case 'C30':
                    return 1723 * input.width * input.height * 10 ** -6 * input.beam_length
                case 'C35':
                    return 1887.8 * input.width * input.height * 10 ** -6 * input.beam_length
                case 'C45':
                    return 1973 * input.width * input.height * 10 ** -6 * input.beam_length
        else:
            return 0
            
    def get_cost_ordinary_reinforcement(self, input, reinforcement, density_ordinary: int) -> float:
        ''' Calculates cost for the beam from ordinary reinfrocement
        Args:
            input:  Instance with all input defined by the user in the Input script
            reinforcement:  Instance for the reinforcment based on the inputs 
            density_ordinary(float):  Density for ordinary reinforcement steel [kg/m3]
        Returns:
            cost of ordinary reinforcement [NOK]
        '''
        if input.ordinary_reinforcement_diameter in [8,10,12,16,20,25]:
            match input.ordinary_reinforcement_diameter:
                case 8:
                    return reinforcement.As * 10 ** -6 * density_ordinary * input.beam_length * 27.92
                case 10: 
                    return reinforcement.As * 10 ** -6 * density_ordinary * input.beam_length * 27.92
                case 12:
                    return reinforcement.As * 10 ** -6 * density_ordinary * input.beam_length * 28.72
                case 16:
                    return reinforcement.As * 10 ** -6 * density_ordinary * input.beam_length * 27.84
                case 20:
                    return reinforcement.As * 10 ** -6 * density_ordinary * input.beam_length * 27.84
                case 25:
                    return reinforcement.As * 10 ** -6 * density_ordinary * input.beam_length * 27.84      
        else:
            return 0


# Define the input instance from the Input class
my_input = Input()

# Define the beam instance from the Beam class
my_beam = Beam(my_input)

# If the beam is prestressed the following will run:
if my_beam.is_the_beam_prestressed == True:

    # If the beam also contain ordinary reinforcment, the next three lines will be printed
    if my_beam.prestressed_and_ordinary_in_top == True:

        print(my_beam.M_control)
        print(my_beam.V_control)
        print(my_beam.printed_emission)
    # If the beam do not contain ordinary reinforcement, only prestressed, the next lines will be printed
    else:
        print(my_beam.M_control)
        print(my_beam.V_control)
        print(my_beam.As_control)
        print(my_beam.Asw_control)
        print(my_beam.crack_control)
        print(my_beam.deflection_control)
        print(my_beam.stress_control)
        print(my_beam.printed_emission)

# If the beam is NOT prestressed, the follwing lines will be printed
else:
    print(my_beam.M_control)
    print(my_beam.V_control)
    print(my_beam.As_control)
    print(my_beam.Asw_control)
    print(my_beam.crack_control)
    print(my_beam.deflection_control)
    print(my_beam.printed_emission)
    print(my_beam.printed_cost)


