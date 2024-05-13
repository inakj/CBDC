# Import module numpy as np
import numpy as np

''' This script contain the ULS class that apply for ordinary reinforced cross section.
'''

class ULS:
    ''' Class to contain all relevant ultimate limit state (ULS) controls. 
    Calculations are based on following assumptions from EC2 6.1(2)P:
    - Full bond between concrete and reinforcement
    - Naviers hypothesis
    - Stress-strain properties from EC 3.1.7, figure 3.5
    - Ignore concrete tension strength 
    Assumed that the ultimate failure criterion is compression failure in concrete. 
    All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the 
    book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Sørensen. 
    '''
    def __init__(self, cross_section, material, load, Asw: float):
        '''Args:
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
        
        '''
        self.alpha = self.calculate_alpha(material.eps_cu3, material.eps_yd, cross_section.As,
            material.Es, material.fcd, cross_section.width, cross_section.d_1, material.fyd, material.lambda_factor, material.netta)
        self.M_Rd = self.calculate_M_Rd(self.alpha, material.fcd, cross_section.width, cross_section.d_1, material.lambda_factor, material.netta) 
        self.V_Rd = self.calculate_V_Rd(cross_section.d_1, cross_section.As, cross_section.width, material.fcd, material.gamma_concrete, material.fck) 
        self.M_control = self.control_of_M_cap(self.M_Rd, load.M_Ed)
        self.V_control = self.control_of_V_cap(self.V_Rd, load.V_Ed, Asw, cross_section.d_1, material.fyd, material.fcd, cross_section.width, material.fck)
        self.M_utilization = self.calculate_utilization_M(self.M_Rd, load.M_Ed)
        self.V_utilization = self.calculate_utilization_V(self.V_Rd, load.V_Ed)
    
    def calculate_alpha(self, eps_cu3: float, eps_yd: float, As: float, Es: float, fcd: float,
                        width: float, d: float, fyd: float, lambda_factor: float, netta: float) -> float:
        ''' Function that calculate factor alpha to decide if cross section is under-reinforced or 
        over-reinforced. 
        Args:
            eps_cu3(float):  concrete strain for bilinear/rectangular analysis, from Material class
            eps_yd(float):  design yeild strain for reinforcement, from Material class
            As(float):  area of reinforcement, from Cross section class[mm2]
            Es(int):  elasticity modulus for reinforcement, from Material class [N/mm2]
            fcd(float):  design compression strength in concrete, from Material class [N/mm2]
            width(float):  width of beam, from Cross section class [mm]
            d(float):  effective height, from Cross section class [mm]
            fyd(float):  design tension strength in reinforcement, from Material class [N/mm2]
            lambda(float):  factor for the effective height from Material class
            netta(float):  factor for the effective strength, from Material class
        Returns:
            alpha(float):  Compression-zone-height factor
        '''
        alpha_bal = eps_cu3 / (eps_cu3 + eps_yd) # from Sørensen (4.20)

        As_balanced = lambda_factor * netta * alpha_bal * width * d * fcd / fyd # from Sørensen (4.21)

        if As <= As_balanced:  # --> Under-reinforced
            alpha = (fyd * As)/ (lambda_factor * netta * fcd * width * d) # from Sørensen (4.19)
        elif As > As_balanced:  # --> Over-reinforced
            # Using abc-formula
            a = lambda_factor * netta * fcd * width * d
            b = eps_cu3 * Es * As
            c = - eps_cu3 * Es * As
            alpha = max((- b + np.sqrt(b ** 2 - 4 * a * c)) / (2 * a),
                        (- b - np.sqrt(b ** 2 - 4 * a * c)) / (2 * a)) # from Sørensen (4.18)
            
        return alpha

    def calculate_M_Rd(self, alpha: float, fcd: float, width: float, d: float, lambda_factor: float,
                       netta: float) -> float:
        ''' Function that calculates M_Rd based on calculated alpha
        Args:
            alpha(float):  Compression-zone-height factor 
            fcd(float):  design compression strength in concrete, from Material class [N/mm2]
            width(float):  width of beam, from Cross section class [mm]
            d(float):  effective height from Cross section class [mm]
            lambda(float):  factor for the effective height from Material class
            netta(float):  factor for the effective strength, from Material class
        Returns: 
            M_Rd(float):  moment capacity [kNm]
        '''
        M_Rd = lambda_factor * netta * alpha * (1 - 0.5 * lambda_factor * alpha) * fcd * width * d ** 2 # from Sørensen (4.14)
        return M_Rd *  10 ** -6
    
    
    def calculate_V_Rd(self, d: float, As: float, width: float, fcd: float, gamma_concrete: float, 
                       fck: int) -> float:
        ''' Function that calculate V_Rd according to EC2 6.2.2(1), when there is assumed no 
        calculation based need for shear reinforcement.
        Args:
            d(float):  effective height, from Cross section class [mm]
            As(float):  area of reinforcement, from Cross section class[mm2]
            width(float):  width of beam, from Input class [mm]
            fcd(float):  design compression strength in concrete, from Material class [N/mm2]
            gamma_concrete(float):  materialfactor for concrete, from Material class
            fck(int):  cylinder compression strength, from Material class [N/mm2]
        Returns:
            V_Rd(float):  Shear force capacity [kN]
        '''
        k = min(1 + np.sqrt(200 / d), 2)

        ro_l = min(As / (width * d), 0.02)

        sigma_cp = 0.2 * fcd 

        CRd_c = 0.18 / gamma_concrete # from EC2 NA.6.2.2(1)

        k_1 = 0.15

        v_min = 0.035 * k ** (3/2) * fck ** (0.5) # from EC2 (6.3N)

        V_Rd_c = (CRd_c * k * (100 * ro_l * fck) ** (1/3) + k_1 * sigma_cp) * width * d # from EC2 (6.2.a)

        V_Rd_min = (v_min + k_1 * sigma_cp) * width * d # from EC2 (6.2.b)

        V_Rd = max(V_Rd_c, V_Rd_min) * 10 ** -3

        return V_Rd 
    
    def control_of_M_cap(self, M_Rd: float, M_Ed: float) -> bool:
        ''' Function that control moment capacity compared with design moment
        Args:
            M_Rd(float):  Moment capacity [kNm]
            M_Ed(float):  Design moment, from Load properties class [kNm]
        Returns:
            "True" if the moment capacity is suifficent and "False" if its not suifficent
        '''
        if M_Rd >= M_Ed:
            return True
        else: 
            return False
    
    def control_of_V_cap(self, V_Rd: float, V_Ed: float, Asw: float, d: float, fyd: float, fcd: float, width: float, fck: float) -> bool:
        ''' Function that control shear capacity compared with design shear force. Also, if the 
        capacity is not suifficent, the function checks if the shear capacity is good enough according 
        to EC2 6.2.3(3) where there is calculation-based need for shear reinforcement. 
        Args:
            V_Rd(float):  Shear capacity [kNm]
            V_Ed(float):  Design shear force, from Load properties class [kNm]
            Asw(float):  area of shear reinforcement per meter, from Input class[mm2/mm] 
            d(float):  effective height, from Cross section class [mm]
            fyd(float): design tension strength in reinforcement, from Material class [N/mm2]
            fcd(float):  design compression strength in concrete, from Material class [N/mm2]
            width(float):  width of beam, from Input class [mm]
            fck(int):  cylinder compression strength, from Material class [N/mm2]
        Returns:
            "True" if the shear capacity is suifficient and "False" if its not 
        '''
        if V_Rd >= V_Ed:
            return True
        else:
            alpha_cw = 1 # from EC2 (NA.6.11N)
            v = 0.6 * (1 - fck / 250) # from EC2 (6.6N)

            #  Shear capacity if there is calculation-based need for shear reinforcement: 
            self.V_Rds = min(Asw * 0.9 * d * fyd * 10 ** -3, alpha_cw * v * width * 0.9 * d * fcd * 10 ** -3) # from EC2 (6.8)

            if self.V_Rds >= V_Ed:
                return True 
            else:
                return False
    
    def calculate_utilization_M(self, M_Rd: float, M_Ed: float) -> float:
        ''' Calculation of utilization degree for moment capacity.
        Args:
            M_Rd(float):  Moment capacity [kNm]
            M_Ed(float):  Design moment, from Load properties class [kNm]
        Returns:
            M_utilization(float):  utilization degree for moment capacity [%]
        '''
        utilization = (M_Rd / M_Ed) * 100
        return round(utilization,1)
    
    def calculate_utilization_V(self, V_Rd: float, V_Ed: float) -> float:
        ''' Calculation utilization degree for shear capacity. Use the shear capacity V_Rds for calculation-based 
        need for shear reinforcement instead of the ordinary shear capacity if the capacity is not suifficent.
        Args: 
            V_Rd(float):  Shear capacity [kNm]
            V_Ed(float):  Design shear force, from Load properties class [kNm]
        Returns:
            V_utilization(float):  utilization degree for shear capacity [%]
        '''
        if V_Rd < V_Ed:
            utilization = (self.V_Rds / V_Ed) * 100
        else:
            utilization = (V_Rd / V_Ed) * 100
        return round(utilization,1)
    