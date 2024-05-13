
''' This script contain the Stress class that apply for prestressed reinforced cross section.
'''

class Stress:

    '''Class to contain calculation stress calculation for prestressed cross section. Include calculations from both 
    Uncracked and Cracked Stress Class. All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the 
    book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Svein Ivar Sørensen.
    '''

    def __init__(self, material, deflection, uncracked_stress, cracked_stress, load, time_effect):
        '''Args:
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
        '''
        self.sigma_p_uncracked = self.calculate_reinforcement_stress_uncracked(uncracked_stress.sigma_c_uncracked[2], material.Ecm, material.Ep, load.sigma_p_max, time_effect.loss)
        self.sigma_p_cracked = self.calculate_reinforcement_stress_cracked(deflection.eps_cs, material.Ep, time_effect.loss, cracked_stress.alpha, load.sigma_p_max, cracked_stress.sigma_c_cracked,
                                                                           cracked_stress.Ec_middle)
        self.control = self.control_stress(material.fck, material.fctm, deflection.control_of_Mcr, cracked_stress.sigma_c_cracked, uncracked_stress.sigma_c_uncracked)


    def calculate_reinforcement_stress_uncracked(self, sigma_c_prestress: float, Ecm: float, Ep: int, sigma_p_max: float, loss: float) -> float:
        ''' Function that calculates total stress in reinforcement because of reduction from
        concrete stress in line with prestress
        Args:
            sigma_c_prestress(float):  concrete stress in line with prestress, from Uncracked stress class [N/mm2]
            Ecm(float):  elasticity modulus for concrete, from Material class[N/mm2]
            Ep(int):  elasticity modulus for steel, from Material class [N/mm2]
            sigma_p_max(float):  design value of prestressing stress, from Load properties class [N/mm2]
            loss(float):  loss in prestress because of creep, shrink and relaxation, from Time effects class [N/mm2]
        Returns:
            sigma_p_uncracked(float):  total stress including all loss [N/mm2]
        '''
        delta_eps_p = abs(sigma_c_prestress) / Ecm # Strain reduction in prestressed reinforcement

        delta_sigma_p = delta_eps_p * Ep # Stress reduction in prestressed reinforcement

        sigma_p_uncracked = sigma_p_max - delta_sigma_p - loss # The total stress in prestress for uncracked cross section
        return sigma_p_uncracked
    
    def calculate_reinforcement_stress_cracked(self, eps_cs: float, Ep: int, loss: float, alpha: float,
                                               sigma_p_max: float, sigma_c_cracked: float, E_middle: float) -> float:
        ''' Function that calculates stress in prestressed reinforcement, including
        strain change and losses.
        Args:
            eps_cs(float):  total shrinkage strain, from Deflection class
            Ep(int):  elasticity modulus for prestressed reinforcement, from Material class [N/mm2]
            loss(float): reduction of stress because of shrink, creep and relaxation, from Time effects class [N/mm2]
            alpha(float):  factor for cracked cross section, M/N, from Cracked stress class [mm]
            sigma_p_max(float):  design value of prestressing stress, from Load properties class [N/mm2]
            sigma_c_cracked(float):  concrete stress for cracked cross section, from Cracked stress class [N/mm2]
            E_middle(float):  middle elasticity modulus, from Cracked stress class [N/mm2]
        Returns:
            sigma_p(float):  stress in prestressed reinforcement [N/mm2]
        '''
        eps_c = abs(sigma_c_cracked) / E_middle # Concrete strain in top 

        delta_eps_p = eps_c * (1 - alpha) / alpha # Strain near prestressed reinforcement

        delta_sigma_p = (delta_eps_p - eps_cs) * Ep # Stress reduction in prestressed reinforcement

        sigma_p_cracked = sigma_p_max - abs(delta_sigma_p) - loss # The total stress in prestress for cracked cross section
        return sigma_p_cracked
    
    
    def control_stress(self, fck: int, fctm: float, control_M_cr: bool, sigma_c_cracked: float, sigma_c_uncracked: float) -> float: 
        '''Control of biggest pressure in top/bottom and control of tension in prestress
        Args:
            fck(int):  cylinder compression strength, from Material class [N/mm2]
            fctm(float):  middlevalue of concrete axial tension strength, from Material class [N/mm2]
            control_M_cr(boolean):  return True or False
            sigma_c_cracked(float):  concrete stress for cracked cross section, from Cracked stress class [N/mm2]
            sigma_c_uncracked(float):  concrete stress for uncracked cross section, from Uncracked stress class [N/mm2]
        Returns:
            True if cracked, False if uncracked
        '''
        self.allowed_pressure = 0.6 * fck # From EC2 7.2(2)

        self.allowed_tension = fctm # From EC2 table 3.1

        if control_M_cr == True:
            if sigma_c_cracked < 0:
                if self.allowed_pressure < sigma_c_cracked: 
                    return True
                else:
                    return False
            else:
                if self.allowed_tension > sigma_c_cracked:
                    return True
                else:
                    return False
        else: 
            for i in range (0,len(sigma_c_uncracked)):
                if sigma_c_uncracked[i] < 0:
                    if self.allowed_pressure < sigma_c_uncracked[i]:
                        return True
                    else:
                        return False
                else:
                    if self.allowed_tension > sigma_c_uncracked[i]:
                        return True
                    else:
                        return False
   
        
 