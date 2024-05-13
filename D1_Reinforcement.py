# Import module numpy as np
import numpy as np

''' This script contain the reinforcement classs that apply for ordinary reinforced cross section.
'''

class Reinforcement_control:
    ''' Class to contain all reinforcement controls for ordinary reinforced cross section
    All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the 
    book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Svein Ivar Sørensen.
    '''
    def __init__(self, cross_section, material, load, ULS_nonprestressed, Asw: float):
        '''Args: 
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
        '''
        self.As_necessary = self.calculate_necessary_reinforcement(load.M_Ed, cross_section.d_1, material.fyd, material.lambda_factor, ULS_nonprestressed.alpha)
        self.As_min = self.calculate_As_min(material.fctm, material.fyk, cross_section.width, cross_section.d_1)
        self.As_max = self.calculate_As_max(cross_section.Ac)
        self.control = self.control_reinforcement(cross_section.As, self.As_necessary, self.As_max, self.As_min)
        self.Asw_control = self.control_reinforcement_shear(material.fck, material.fyk, cross_section.width, Asw)
        self.utilization = self.calculate_utilization_degree_As(self.As_necessary, cross_section.As)
        self.utilization_shear = self.calculate_utilization_degree_Asw(Asw)


        
    
    def calculate_necessary_reinforcement(self, M_Ed: float, d: float, fyd: float, lambda_factor: float, alpha: float) -> float:
        ''' Function that calculates necessary reinforcement
        Args: 
            M_Ed(float):  design moment, from Load properties class [kNm]
            d(float):  effective height, from Cross section class [mm]
            fyd(float):  design tension strength in reinforcement, from Material class [N/mm2]
            lambda_factor(float):  factor for effective height 
            alpha(float):  compression-zone-height factor, from ULS class
        Returns:
            As_necessary(float):  Necessary reinforcement [mm2]
        '''
        z = (1 - 0.5 * lambda_factor * alpha) * d # From Sørensen (4.13)

        As_necessary = (M_Ed * 10  ** 6) / ( z * fyd) # From Sørensen (4.26)

        return As_necessary

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
    
    def calculate_As_max(self, Ac: float) -> float:
        '''Function that calculates As maximum according EC2 9.2.1.1(3)
        Args:
            Ac(float):  concrete area, from Cross section class [mm2]
        Returns:
            As_max(float):  Maximum reinforcement [mm2]
        '''
        As_max = 0.04 * Ac
        return As_max
    
    def control_reinforcement(self, As: float, As_necessary: float, As_max: float, As_min: float) -> bool:
        ''' Control of reinforcement area. The area As must be smaller than the maximum, larger than the minimum, 
        and larger than the necessary area to satisfy for the design moment. 
        Args:
            As(float):  reinforcement area, from Cross section class [mm2]
            As_necessary(float):  necessary reinforcement [mm2]
            As_min(float):  minimum reinforcement [mm2]
            As_max(float): maximum reinforcement [mm2]
        Returns:
            As_control(bool):  Return True if area is suifficent or False if its not suifficent
        '''
        if As > As_max or As < As_min or As < As_necessary:
            return False
        else: 
            return True
        
    def control_reinforcement_shear(self, fck: float, fyk: float, width: float, Asw: float) -> bool:
        ''' Control of shear reinforcement area according to EC2 9.2.2(5)
        Args:
            fck(int):  cylinder compression strength, from Material class [N/mm2]
            fyk(int):  steel tensions characteristic strength, from Material class [N/mm2]
            width(float):  width of beam, from Input class [mm]
            Asw(float):  area of shear reinforcement per meter, from Input class [mm2/mm] 
        Returns:
            Asw_control(bool):  Control of shear reinforcement, return True or False
        '''
        self.ro_w_min = 0.1  * np.sqrt(fck) / fyk # From EC2 (9.5N)

        alpha = np.pi/2  # vertical bars, 90 degrees

        self.b_w = width # flange width = cross section width

        self.Asw_min = self.ro_w_min * self.b_w * np.sin(alpha) # From EC2 (9.4)

        if self.Asw_min < Asw:
            return True
        else:
            return False
        
    
    def calculate_utilization_degree_As(self, As_necessary: float, As: float) -> float:
        ''' Calculate utilization degree for ordinary reinforcement
        Args:
            As_necessary(float):  Necessary ordinary reinforcement [mm2]
            As(float):  Area of reinforcement, from Cross section class [mm2]
        Returns:
            Utilization(float):  utilization degree for ordinary reinforcement [%]
        '''
        utilization = (As / As_necessary) * 100 
        return round(utilization,1)
    
    def calculate_utilization_degree_Asw(self, Asw: float) -> float:
        ''' Calculate utilization degree for shear reinforcement
        Args:
            Asw(float):  area of shear reinforcement per meter, from Input class [mm2/mm] 
        Returns:
            Utilization(float):  utilization degree for shear reinforcement [%]
        '''
        utilization = (Asw / self.Asw_min) * 100 
        return round(utilization,1)



