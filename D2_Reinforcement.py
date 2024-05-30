# Import module numpy as np
import numpy as np

''' This script contain the reinforcement classs that apply for prestressed reinforced cross section.
'''

class Reinforcement_control_prestressed:
    ''' Class to contain all reinforcement controls for prestressed cross section
    All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the 
    book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Svein Ivar Sørensen.
    '''
    def __init__(self, cross_section, material, load, ULS_prestressed, Asw: float):
        '''Args: 
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
            safety:  safety degree for reinforcement [%]
            safety_shear:  safety degree for shear reinforcement [%]
        '''
        self.As = self.calculate_As_min(material.fctm, material.fyk, cross_section.width, cross_section.d_2)
        self.Asw_control = self.control_reinforcement_shear(material.fck, material.fyk, cross_section.width, Asw)
        self.Ap_necessary= self.calculate_prestress_reinforcement(load.M_Ed, cross_section.d_2, material.fpd, material.lambda_factor, ULS_prestressed.alpha)
        self.control = self.control_prestress_reinforcement(self.Ap_necessary, cross_section.Ap)
        self.safety = self.calculate_safety_degree_Ap(self.Ap_necessary, cross_section.Ap)
        self.safety_shear = self.calculate_safety_degree_Asw(Asw)


    def calculate_As_min(self, fctm: float, fyk: int, width: float, d: float) -> float:
        ''' Function that calculates As minimum according to EC2 9.2.1.1(1)
        Args:
            fctm(float):  middlevalue of concrete axial tension strength, from Material class [N/mm2]
            fyk(int):  steel tensions characteristic strength, from Material class[N/mm2]
            width(float):  width of beam, from Input class [mm]
            d(float):  effective height from cross section class, from Cross section class [mm]
        Returns:
            As_min(float):  Minimum reinforcement [mm2]
        '''
        As_min = max(0.26 * (fctm / fyk) * width * d, 0.0013 * width * d)
        return As_min
    
    def control_reinforcement_shear(self, fck: float, fyk: float, width: float, Asw: float) -> bool:
        ''' Control of shear reinforcement area according to EC2 9.2.2(5)
        Args:
            fck(int):  cylinder compression strength, from Material class [N/mm2]
            fyk(int):  steel tensions characteristic strength, from Material class [N/mm2]
            width(float):  width of beam, from Input class [mm]
            Asw(float):  area of shear reinforcement per meter, From Input class [mm2/mm] 
        Returns:
            Asw_control(boolean):  Control of shear reinforcement, return True or False
        '''
        ro_w_min = 0.1  * np.sqrt(fck) / fyk # From EC2 (9.5N)

        alpha =  np.pi/2  # vertical bars, 90 degress

        b_w = width # flange width = cross section width

        self.Asw_min = ro_w_min * b_w * np.sin(alpha)  # From EC2 (9.4)

        if self.Asw_min < Asw:
            return True
        else:
            return False
        
    def calculate_prestress_reinforcement(self, M_Ed: float, d: float, fpd: float, lambda_factor: float, alpha: float) -> float:
        ''' Function that calculates necessary prestress reinforcement. Assumed that prestressed reinforcement take 
        all external load.
        Args: 
            M_Ed(float):  design moment, from Load properties class [kNm]
            d(float):  effective height, from Cross section class [mm]
            fpd(float):  pretension strength, from Material class [N/mm2]
            lambda_factor(float):  factor for effective height 
            alpha(float):  compression-zone-height factor, from ULS class
        Returns:
            Ap_necessary(float):  Necessary prestress reinforcement [mm2]
        '''
        z = (1- 0.5 * lambda_factor * alpha) * d # Derivated from Sørensen (4.13) 
        Ap_necessary = (M_Ed * 10  ** 6) / ( z * fpd) # Derivated from Sørensen (4.26)
        return Ap_necessary
    
    def control_prestress_reinforcement(self, Ap_necessary: float, Ap: float) -> bool:
        ''' Control of prestress reinforcement
        Args:
            Ap_necessary(float):  Necessary prestress reinforcement [mm2]
            Ap(float):  Area of prestress reinforcement [mm2]
        Returns:
            Ap_control(bool):  Control of prestress reinforcement area, return True or False
        '''
        if Ap >= Ap_necessary:
            return True
        else:
            return False

    def calculate_safety_degree_Ap(self, Ap_necessary: float, Ap: float) -> float:
        ''' Calculate safety degree for prestressed reinforcement
        Args:
            Ap_necessary(float):  Necessary prestress reinforcement [mm2]
            Ap(float):  Area of prestress reinforcement, from Cross sectino class [mm2]
        Returns:
            safety(float):  safety degree for prestressed reinforcement [%]
        '''
        safety = (Ap / Ap_necessary) * 100 
        return round(safety,1)
    
    def calculate_safety_degree_Asw(self, Asw: float) -> float: 
        ''' Calculate safety degree for shear reinforcement
        Args:
            Asw(float):  area of shear reinforcement per meter, from Inut class [mm2/mm] 
        Returns:
            safety(float):  safety degree for shear reinforcement [%]
        '''
        safety = (Asw / self.Asw_min) * 100 
        return round(safety,1)
