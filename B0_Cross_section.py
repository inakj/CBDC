
# Import module numpy as np
import numpy as np

''' This script contain the Cross section class that apply for all reinforcement cases.
'''

class Cross_section:
    '''Class to contain cross section properties used in calculations.
    All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2)
    '''
    def __init__(self, width: float, height: float, nr_bars: int, bar_diameter: float, 
                 stirrup_diameter: float, exposure_class: str, prestress_diameter: float,
                 nr_prestressed_bars: int, material):
        '''Args:
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
        '''
        self.width = width
        self.height = height
        self.Ac = self.calculate_Ac(self.width, self.height)
        self.Ic = self.calculate_Ic(self.width, self.height)
        self.c_min_b = self.get_c_min_b(bar_diameter)
        self.c_min_dur = self.get_c_min_dur(exposure_class, self.c_min_b)
        self.cnom = self.calculate_cnom(self.c_min_b, self.c_min_dur)
        self.As = self.calculate_As(bar_diameter, nr_bars)
        self.d_1 = self.calculate_d(height, self.cnom, bar_diameter, stirrup_diameter)
        self.d_2 = self.calculate_d(height, self.cnom, prestress_diameter, stirrup_diameter)
        self.e = self.calculate_e(self.cnom, stirrup_diameter, prestress_diameter, height)
        self.Ap = self.calculate_Ap(nr_prestressed_bars, material.Ap_strand)
        
    def calculate_Ac(self, width: float, height: float) -> float:
        ''' Function that calculates concrete cross section area, Ac
        Args:
            width(float):  width of cross-section as attribute[mm]
            height(float):  height of cross-section as attribute [mm]
        Returns:
            Ac(float):  concrete area [mm2]
        '''
        Ac = width * height
        return Ac
    
    def calculate_Ic(self, width: float, height: float) -> float:
        ''' Function that calculates second moment of inertia, Ic
        Args:
            width(float):  width of cross-section as attribute[mm]
            height(float):  height of cross-section as attribute [mm]
        Returns:
            Ic(float):  second moment of inertia [mm4]
        '''
        Ic = (width * height ** 3) / 12
        return Ic

    def get_c_min_b(self, bar_diameter: float) -> float:
        ''' Function that finds c_min_b accordning to EC2 table NA.4.2, assumed only simple bars.
        Args:
            bar_diameter(float):  diameter of each reinforcement bar, defined by user [mm]
        Returns:
            c_min_b(float): smallest nominal cover because of bonding [mm]
        '''
        c_min_b = max(bar_diameter,10) 
        return c_min_b

    def get_c_min_dur(self, exposure_class: int, c_min_b: float) -> float:
        ''' Function that finds c_min_dur according to EC2 table NA.4.4N, assumed 50 years.
        Args:
            exposure_class(string):  exposure class, defined by user
            c_min_b(float):  smallest nominal cover because of bonding [mm]
        Returns:
            c_min_dur(float): smallest nominal cover because of environmental effects [mm]
        '''
        if exposure_class == 'X0':
            c_min_dur = c_min_b
        elif exposure_class == 'XC1':
            c_min_dur = 15
        elif exposure_class in ['XC2','XC3','XC4']:
            c_min_dur = 25
        elif exposure_class in ['XD1','XS1','XD2','XD3','XS2']:
            c_min_dur = 40
        elif exposure_class == 'XS3':
            c_min_dur = 50
        else:
            raise ValueError (f'There is no exposure class called{exposure_class} and therefor no value for c.min.dur')
        
        return c_min_dur


    def calculate_cnom(self, c_min_b: float, c_min_dur: float) -> float:
        ''' Function that finds cnom according to EC2 4.4.1.1, 4.4.1.2 and 4.4.1.3. 
        Args:
            c_min_b(float):  smallest nominal cover because of bonding [mm]
            c_min_dur(float):  smallest nominal cover because of environmental effects [mm]
        Returns:
            cnom(float):  nominal concrete cover [mm] 
        '''
        c_min = max(c_min_b,c_min_dur,10) # From 4.4.1.2(2)
        delta_c_dev = 10 # From 4.4.1.3(1)
        cnom = c_min + delta_c_dev # From 4.4.1.1(2)
        return cnom 

    def calculate_As(self, bar_diameter: float, nr_bars: int) -> float: 
        ''' Function that calculates As by taking area of one bare and multiplying it 
        by number of bars
        Args:  
            bar_diameter(float):  diameter of each reinforcement bar, defined by user [mm]
            nr_bars(int):  numbers of reinforcement bars in longitudinal direction, defined by user
        Returns:
            As(float):  area of longitudinal reinforcement in cross section [mm2]
        '''
        As = (0.5 * bar_diameter) ** 2 * np.pi * nr_bars
        return As 

    
    def calculate_d(self, height: float, cnom: float, bar_diameter: float,
                    stirrup_diameter: float) -> float: 
        ''' Function that calculates the distance d
        Args: 
            height(float):  height of cross-section, defined by user [mm]
            cnom(float):  nominal concrete cover [mm]
            bar_diameter(float):  diameter of longitudinal reinforcement [mm]
            stirrup_diameter(float):  diameter of stirrup reinforcement [mm]
        Returns:
            d(float):  distance from top to reinforcement, or opposite, depending on the reinforcement placement [mm]
        '''
        d = height - cnom - 0.5 * bar_diameter - stirrup_diameter
        return d 
 
    def calculate_e(self, cnom: float, stirrup_diameter: float, prestress_diameter: float, height: float) -> float:
        ''' Function that calculates the distance e
        Args:
            cnom(float):  nominal concrete cover [mm]
            stirrup_diameter(float):  diameter of stirrup reinforcement [mm]
            prestress_diameter(float):  diameter of one prestressing strand [mm2]
        Returns:
            e(float):  distance from bottom to prestressed reinforcement [mm]
        '''
        e = height / 2 - cnom + stirrup_diameter + prestress_diameter / 2
        return e
    
    def calculate_Ap(self, nr_prestressed_bars: int, Ap_strand: float) -> float:
        ''' Function that calculate Ap
        Args:   
            nr_prestressed_bars(int):  number of prestressed reinforcement bars, defined by user
            Ap_strand(float):  area of one prestressed strand from material class [mm2]
        Returns:
            Ap(float):  total area of prestressed steel in cross section [mm2]
        '''
        Ap = nr_prestressed_bars * Ap_strand
        return Ap
