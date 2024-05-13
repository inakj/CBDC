# Import module numpy as np
import numpy as np

''' This script contain the Cracked stress class that apply for prestressed reinforced cross section.
'''
class Cracked_Stress:
    '''Class to contain calculation of cracked prestressed cross section. 
    All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the 
    book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Svein Ivar Sørensen.
    '''

    def __init__(self, material, cross_section, load, deflection, time_effect, creep_number):
        '''Args:
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
        '''
        self.Ec_middle = self.calculate_Ec_middle(material.Ecm, creep_number.phi_selfload, creep_number.phi_liveload, load.Mg_d, load.Mp_d, load.M_prestress, time_effect.loss_percentage)
        self.netta = self.calculate_netta(material.Es, self.Ec_middle)
        self.ro_l = self.calculate_ro(cross_section.Ap, cross_section.width, cross_section.d_2)
        self.Ns = self.calculate_axial_force(deflection.eps_cs, material.Ep, cross_section.Ap)
        self.a = self.calculate_a(load.Mg_d, load.Mp_d, load.P0_d, load.M_prestress, time_effect.loss_percentage, cross_section.e, self.Ns)
        self.alpha = self.calculate_alpha(cross_section.d_2, cross_section.e, self.a, self.netta, self.ro_l)
        self.sigma_c_cracked = self.calculate_concrete_stress_cracked(cross_section.d_2, cross_section.width, self.alpha, self.netta, self.ro_l)
       
    def calculate_Ec_middle(self, Ecm: int, phi_selfload: float, phi_liveload: float,
                           Mg_d: float, Mp_d: float, M_p: float, loss: float) -> float:
        ''' Function that calculates Ec_middle, based on effective elasticity modulus according to EC2 7.4.3(5)
        Args:
            Ecm(int):  elasticity modulus for concrete, from Material class [N/mm2]
            phi_selfload(float):  creep number for self-load, from Creep number class
            phi_liveload(float):  creep number for live-load, from Creep cnumber class
            Mg_d(float):  self-load moment, from Load properties class[kNm]
            Mp_dfloat):  live-load moment, from Load properties class[kNm]
            M_prestress(float):  moment because of prestressing [kNm]
            loss(float):  loss of prestress because of time effects [%]
        Returns:
            E_middle(float):  middle elasticity modulus [N/mm2]
        '''
        Ec_eff_selfload = Ecm / (1 + phi_selfload) # Effective elasticity modulus for self-load from EC2 (7.20)

        Ec_eff_liveload = Ecm / (1 + phi_liveload) # Effective elasticity modulus for live-load from EC2 (7.20)
        
        M_prestress = M_p * (1 - loss / 100) # Moment because of prestresseding force including losses

        Ec_middle = (abs(M_prestress) + Mg_d + Mp_d) / ( (abs(M_prestress) + Mg_d) / Ec_eff_selfload + Mp_d / Ec_eff_liveload) # Based on Sørensen (5.25)
        return Ec_middle
        
    def calculate_netta(self, Ep: int, Ec_middle: float) -> float:
        ''' Function that calculates matierial stiffness ratio netta
        Args:
            Ep(int):  elasiticity modulus for prestressed steel, from Input class [N/mm2]
            Ec_middle(float):  middle elasticity modulus [N/mm2]
        Returns:
            netta(float): material stiffness ratio
        '''
        netta = Ep / Ec_middle 
        return netta
    
    def calculate_ro(self, Ap: float, width: float, d: float) -> float:
        ''' Function that calculates reinforcement ratio ro
        Args:
            As(float):  reinforcement area, from Cross section class[mm2]
            width(float): width, from Cross section class [mm]
            d(float):  effective height, from Cross section class[mm]
        Returns:
            ro_l(float): reinforcement ratio
        '''
        ro_l = Ap / (width * d) 
        return ro_l

    def calculate_axial_force(self, eps_cs: float, Ep: int, Ap: float) -> float:
        ''' Function that calculates acial force in prestress because of free shrink
        Args:
            eps_cs(float):  total shrinkage strain, from Deflection class
            Ep(int):  elasticity moduls for prestressed reinforcement, from Material class [N/mm2]
            Ap(float):  area of prestressed reinforcement, from Cross section [mm2]
        Returns:
            Ns(float):  axial force in prestress because of free shrink [kN]
        '''
        Ns = eps_cs * Ep * Ap * 10 ** -3 # From Sørensen (6.15) 
        return Ns
    
    def calculate_a(self, Mg_d: float, Mp_d: float, P0: float, M_p: float, loss: float, e: float, Ns: float) -> float:
        ''' Function that calculates distance 'a' equal to relation M/N 
        Args:
            Mg_d(float):  selfload moment, from Load properties class [kNm]
            Mp_d(float):  liveload moment, from Load properties class [kNm]
            P0(float):   design value of prestressign force, from Cross sectino class [N]
            M_p(float):   moment because of prestressing included losses, from Load properties class [kNm]
            loss(float):  loss of prestress, from Time effects class[%]
            e(float):  distance from bottom to prestressed reinforcement, from Cross section class[mm]
            Ns(float):  axial force in prestress because of free shrink [kN]
        Returns:
            a(float):  ratio between moment and axial force [mm]
        '''
        self.N = P0 * 10 ** -3 - Ns # From Sørensen fig. 6.8 

        self.M_prestress = M_p * (1 - loss/100) # Moment because of prestress force with losses

        self.M = Mg_d + Mp_d + self.M_prestress + (Ns * e * 10 ** -3) # Total moment in cross section

        a = 1000 * self.M/self.N  # From Sørensen fig. 6.8
        return a 
    
    def calculate_alpha(self, d :float, e: float, a: float, netta: float, ro_l: float) -> float:
        ''' Function that calculates factor alpha, using a function to calculate
        a third degree equation, from Sørensen (6.24)
        Args:
            d(float):  effective height, from Cross section class[mm]
            e(float):  distance to reinforcement, from Cross section class [mm]
            a(float):  factor [mm]
            netta(float): material stiffness ratio
            ro_l(float): reinforcement ratio
        Returns:
            alpha(float):  factor
        '''
        coefficients = [d / (6 * (e + a)), 0.5 * (1 - d / (e + a)), netta * ro_l, - netta * ro_l] 

        roots = np.roots(coefficients)

        for num in roots:
            if 0 < num < 1:            
                alpha = float(num)
                return alpha
    
    def calculate_concrete_stress_cracked(self, d: float, width: float, alpha: float, netta: float, ro_l: float) -> float:
        ''' Function that calculates concrete stress in top of cross section, sørensen (6.25)
        Args:
            d(float):  effective height, from Cross section class[mm]
            width(float):  width of cross section, from Input class [mm]
            alpha(float):  factor
        Returns:
            sigma_c(float):  concrete stress in top [N/mm2]
        '''
        sigma_c_cracked = (-self.N * 10 ** 3) / (width * d * (0.5 * alpha - netta * ro_l * ((1 - alpha) / alpha)))
        return sigma_c_cracked
    
   
   
