# Import module numpy as np
import numpy as np

''' This script contain the Time effects class that apply for prestressed reinforced cross section.
'''

class time_effects:
    ''' Class to contain losses that is caused by time, including shrink, creep and relaxation. 
    All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the 
    book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Svein Ivar Sørensen.
    '''
    def __init__(self, material, cross_section, creep_number, stress_uncracked, deflection, load):
        '''Args:
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
        '''
        self.delta_relaxation = self.calculate_delta_sigma_pr(material.fpk, material.fp01k,500000)
        self.loss = self.calculate_stress_reduction(deflection.eps_cs, material.Ep, material.Ecm, self.delta_relaxation, creep_number.phi_selfload,
                                                    stress_uncracked.sigma_c_uncracked[2], cross_section.Ap, cross_section.Ac, cross_section.Ic, cross_section.e) 
        self.loss_percentage = self.calculate_loss_percentage(self.loss, load.sigma_p_max)
    

    def calculate_delta_sigma_pr(self, fpk: float, fp01k: float, t) -> float:
        ''' Calculation of loss in stress because of relaxation, where the steel is exposed to constant
        strain for long time, according to EC2 3.3.2(7) and 5.10.3(2). Assumed class 2: low relaxation. 
        Args:
            fpk(float):  characteristic strength for prestress, from Material class [N/mm2]
            fp01k(float):  0.1% limit of strength for prestress, from Material class [N/mm2]
            t(int):  time after stress-application, assumed t = 500 000 from EC2 3.3.2(8).[hours]
           
        Returns:
            delta_sigma_pr(float):  Absolute value of relaxation loss [N/mm2]
        '''
        sigma_pi = min(0.75 * fpk, 0.85 * fp01k) # From EC2 (5.43)

        ro_1000 = 2.5 # 3.3.2(6), assumed class 2 from 3.3.2(4)

        my = sigma_pi / fpk # From EC2 3.3.2(7)

        # Assumed class 2, from EC2 (3.29):
        delta_sigma_pr = sigma_pi * (0.66 * ro_1000 * np.e ** (9.1 * my) * ((t/1000) ** (0.75 * (1 - my))) * 10 ** (-5)) 
        return delta_sigma_pr

    def calculate_stress_reduction(self, eps_cs: float, Ep: float, Ecm: float, delta_sigma_pr: float, phi_selfload: float,
                              sigma_c_QP: float, Ap: float, Ac: float, Ic: float, zcp: float) -> float:
        '''Total time dependant stress reduction in prestress, simplfied from EC2 5.10.6(2). Since the beam have self-load and live-load, its assumed
        that this formula can be used by simply adding the stress reduction from self-load together with the reduction from live-load.
        Using creep number for self-load, assumed that the prestress is applied at the same time. 
        Args:
            eps_cs(float):  total shrinkage strain, from Deflection class
            Ep(int):  elasticity modulus for prestress, from Material class [N/mm2]
            Ecm(int):  elasticity modulus for concrete, from Material class[N/mm2]
            delta_sigma_pr(float):  stress loss because of relaxation [N/mm2]
            phi_selfload(float):  creep number for self-load, from Creep number class 
            sigma_c_QP(float):  concrete stress in line with prestress, from Uncracked stress class [N/mm2]
            Ap(float):  area of prestress, from Cross section class [mm2]
            Ac(float):  area of concrete, from Cross section class [mm2]
            Ic(float):  moment of inertia, from Cross section class [mm4]
            zcp(float):  eccentricity of prestress, same as e, from Cross section class [mm2]
        Return:
            delta_sigma_p(float):  absolute value loss in prestress because of shrink, creep and relaxation [N/mm2]
        '''
        # Stress reduction because of relaxation, creep and shrink: 
        delta_sigma_p = (eps_cs * Ep + 0.8 * delta_sigma_pr + (Ep / Ecm) * phi_selfload * abs(sigma_c_QP)) / \
                (1 + (Ep / Ecm) * (Ap / Ac) * (1 + (Ac / Ic) * zcp ** 2) * (1 + 0.8 * phi_selfload))
         
        return abs(delta_sigma_p)
    
    def calculate_loss_percentage(self, delta_sigma_p: float, sigma_p_max: float) -> float:
        ''' Function that calculate percentage loss because of time effects
        Args: 
            delta_sigma_p(float):  reduction in stress [N/mm2]
            sigma_p_max(float):  design value of prestressing stress, from Load properties class [N/mm2]
        Returns:
            loss(float):  precentage loss because of shrink, creep and relaxation [%]
        '''
        loss_percentage = (delta_sigma_p * 100) / sigma_p_max
        return loss_percentage