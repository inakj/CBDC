
# Import module numpy as np
import numpy as np

''' This script contain the ULS class that apply for prestressed reinforced cross section with ordinary reinforcement in top.
'''

class ULS_prestress_and_ordinary:
    ''' Class to contain all relevant ultimate limit state (ULS) controls for prestressed cross section 
    with ordinary reinforcement in top. All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the 
    book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Sørensen. 
    '''

    def __init__(self, material, load, cross_section, time_effect, Asw: float):
        '''Args:
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
            M_safety(float):  safety degree for moment capacity [%]
            V_safety(float):  safety degree for shear capacity [%]
            
        '''
        self.eps_diff = self.calculate_strain_diff(load.sigma_p_max, material.Ep, time_effect.loss_percentage)
        self.alpha = self.calculate_alpha(material.eps_cu3, cross_section.Ap, material.Ep, material.fcd, self.eps_diff, cross_section.width, cross_section.d_2, material.fpd, material.lambda_factor,
                                          material.netta, material.fyd, cross_section.As)
        self.M_Rd = self.calculate_moment_capacity(self.alpha, material.fcd, cross_section.width, cross_section.d_2, material.lambda_factor, material.netta, material.fyd, cross_section.As, cross_section.cnom)
        self.M_control = self.control_moment(load.M_Ed, load.M_prestress, self.M_Rd)
        self.V_Rd = self.calc_shear_capacity(cross_section.d_2, cross_section.Ac, cross_section.width, cross_section.Ap, material.fcd, material.gamma_concrete, material.fck, load.P0, 
                                             material.gamma_prestressed_reinforcement, time_effect.loss_percentage)
        self.V_control = self.control_V(self.V_Rd, load.V_Ed, Asw, cross_section.d_2, material.fyd, material.fck, cross_section.width, material.fcd)
        self.M_safety = self.calculate_safety_M(self.M_Rd)
        self.V_safety = self.calculate_safety_V(self.V_Rd, load.V_Ed)
    
    def calculate_strain_diff(self, sigma_p: float, Ep: int, loss: float) -> float:
        ''' Function that calculates difference in strain because of losses. Based on Sørensen (6.4).
        Args:
            sigma_p(float):  design value of prestressing stress, from Load properties class [N/mm2]
            Ep(int):  elasticity modulus for steel, from Material class [N/mm2]
            loss(float):  loss in capacity because of time effects, from Time effect class [%]
        Returns:
            eps_diff(float):  effective strain difference 
        '''
        eps_p0 = sigma_p / Ep  # Initial strain
        eps_loss = (loss / 100) * eps_p0 # Reduction in strain because of losses
        eps_diff = eps_p0 - eps_loss # Effective strain
        return eps_diff

    def calculate_alpha(self, eps_cu3: float, Ap: float, Ep: float, fcd: float, eps_diff: float,
                        width: float, d: float, fpd: float, lambda_factor: float, netta: float, fyd: int, As: float) -> float:
        ''' Function that calculate factor alpha to decide if cross section is under-reinforced or 
        over-reinforced. The formulas are derivated from formulas from the book by Sørensen to fit for a prestressed reinforcemed 
        cross-section with ordinary reinforcement in top.
        Args:
            eps_cu3(float):  concrete strain for bilinear/rectangular analysis, from Material class
            Ap(float):  area of prestressed reinforcement, from Cross section class[mm2]
            Ep(int):  elasticity moduls for prestressed reinforcement, from Material class [N/mm2]
            fcd(float):  design compression strength in concrete, from Material class [N/mm2]
            eps_diff(float):  effective strain difference 
            width(float):  width of beam, from Input class [mm]
            d(float):  effective height, from Cross section class [mm]
            fpd(float):  design prestressed strength in reinforcement, from Material class [N/mm2]
            lambda_factor(float):  factor for effective height, from Material class
            netta(float):  factor for effective strength, from Material class
            fyd(int):  tensile strength in ordinary reinforcement, from Material class [N/mm2]
            As(float):  ordinary reinforcement area, from Cross section class [mm2]

        Returns:
            alpha(float):  Compression-zone-height factor 
        '''
        alpha_b = eps_cu3 / (eps_cu3 + fpd / Ep - eps_diff) # Sørensen (7.7)

        Apb = (netta * lambda_factor * alpha_b * width * d * fcd + fyd * As)/ fpd # Derivated from Sørensen (7.8)

        if Ap <= Apb: # -> under-reinforced
            alpha = (fpd * Ap - fyd * As)/ (netta * lambda_factor * fcd * width * d) # Derivated from Sørensen (7.9)
        elif Ap > Apb: # -> over-reinforced
            # using abc-formula for quadratic equation
            a = netta * lambda_factor * fcd * width * d
            b = fyd * As + (eps_cu3 - eps_diff) * Ep * Ap
            c = - eps_cu3 * Ep * Ap
            alpha = max((- b + np.sqrt(b ** 2 - 4 * a * c)) / (2 * a), (- b - np.sqrt(b ** 2 - 4 * a * c)) / (2 * a))  # Derivated from Sørensen (7.10)

        return abs(alpha)

    def calculate_moment_capacity(self, alpha: float, fcd: float, width: float, d: float, lambda_factor: float,
                       netta: float, fyd: int, As: float, cnom: float) -> float:
        ''' Function that calculates M_Rd based on calculated alpha. The formula are derivated from formulas from the book 
        by Sørensen to fit for a prestressed reinforcemed cross-section with ordinary reinforcement in top.
        Args:
            alpha(float):  Compression-zone-height factor 
            fcd(float):  design compression strength in concrete, from Material class [N/mm2]
            width(float):  width of beam, from Input class [mm]
            d(float):  effective height, from Cross section class [mm]
            lambda_factor(float):  factor for effective height, from Material class
            netta(float):  factor for effective strength, from Material class
            fyd(int):  tensile strength in ordinary reinforcement, from Material class[N/mm2]
            As(float):  ordinary reinforcement area, from Cross section class[mm2]
            cnom(float):  nominal cover, from Cross section class [mm]
        Returns: 
            M_Rd(float):  moment capacity [kNm]
        '''
        M_Rd = netta * lambda_factor * alpha * (1 - 0.5 * lambda_factor * alpha) * fcd * width * d ** 2 + fyd * As * (d - cnom)  # Derivated from Sørensen (4.14)
        return M_Rd *  10 ** -6
    
    def control_moment(self, M_Ed: float, M_p: float, M_Rd: float) -> bool:
        ''' Function that control moment capacity 
        Args:   
            M_Ed(float):  design moment, from Load properties class [kNm]
            M_p(float):  moment because of prestressing, from Load properties class [kNm]
            M_Rd(float):  moment capacity [kNm]
        Returns:
            True or False(boolean):  True if capacity is suifficient, False if not
        '''
        # Moment from load and prestress force: 
        self.M_Ed = M_Ed + M_p

        if M_Rd >= self.M_Ed:
            return True
        else: 
            return False
        

    def calc_shear_capacity(self, d: float, Ac: float, width: float, Ap: int, fcd: float, 
                            gamma_concrete: float, fck: int, P0: float, gamma_prestress: float, loss: float) -> float:
        '''Args:
            d(float):  effective height, from Cross section class [mm]
            Ac(float):  area of concrete, from Cross section class [mm2]
            width(float):  width of beam, from Input class [mm]
            Ap(float):  area of prestressed reinforcement, from Cross section class[mm2]
            fcd(float):  design compression strength in concrete, from Material class [N/mm2]
            gamma_concrete(float):  materialfactor for concrete, from Materal class
            fck(int):  cylinder compression strength, from Material class [N/mm2]
            P0(float):   design value of prestressign force, from Load properties class [N]
            gamma_prestresss(float):  loadfactor for prestressing, from Material class
            loss(float): loss in capacity because of time effects, from Time effect class[%]
        Returns:
            V_Rd(float):  shear capacity [kN]
        '''
        k = min(1 + np.sqrt(200 / d),2)

        ro_l = min(Ap / (width * d),0.02)

        N_Ed = abs(P0) * gamma_prestress * (1 - loss/100) # Axial force because of prestress force

        self.sigma_cp = min(N_Ed / Ac, 0.2 * fcd)

        CRd_c = 0.18 / gamma_concrete # from EC2 NA.6.2.2(1)

        k_1 = 0.15 

        v_min = 0.035 * k ** (3/2) * fck ** (0.5)  # from EC2 (6.3N)

        V_Rd_c = (CRd_c * k * (100 * ro_l * fck) ** (1/3) + k_1 * self.sigma_cp) * width * d # from EC2 (6.2.a)

        V_Rd_min = (v_min + k_1 * self.sigma_cp) * width * d # from EC2 (6.2.b)

        V_Rd = max(V_Rd_c,V_Rd_min) * 10 ** -3

        return V_Rd 
        
    def control_V(self, V_Rd: float, V_Ed: float, Asw: float, d: float, fyd: float, fck: float, width: float, fcd: float) -> bool:
        ''' Function that control shear capacity compared with design shear force. Also, if the 
        capacity is not suifficent, the function checks if the shear capacity is good enough according 
        to EC2 6.2.3(3) where there is calculation-based need for shear reinforcement. 
        Args:
            V_Rd(float):  Shear capacity [kNm]
            V_Ed(float):  Design shear force, from Load properties class [kNm]
            Asw(float):  area of shear reinforcement per meter, from Input class [mm2/mm] 
            d(float):  effective height, from Cross section class[mm]
            fyd(float):  design tension strength in reinforcement , from Material class [N/mm2]
        Returns:
            "True" if the shear capacity is suifficient and "False" if its not 
        '''
        if V_Rd >= V_Ed:
            return True
        else:
            if 0 < self.sigma_cp <= 0.25 * fcd:
                alpha_cw = 1 + self.sigma_cp / fcd # from EC2 (6.11.aN)
            elif 0.25 < self.sigma_cp <= 0.5 * fcd:
                alpha_cw = 1.25 # from EC2 (6.11.bN)
            else:
                alpha_cw = 2.5 * (1 - self.sigma_cp / fcd) # from EC2 (6.11.cN)

            v = 0.6 * (1 - fck / 250) # from EC2 (6.6N)

            #  Shear capacity if there is calculation-based need for shear reinforcement: 
            self.V_Rds = min(Asw * 0.9 * d * fyd * 10 ** -3, alpha_cw * v * width * 0.9 * d * fcd * 10 ** -3) # from EC2 (6.8)

            if self.V_Rds >= V_Ed:
                self.V_Rd = self.V_Rds
                return True
            else:
                return False
            
    def calculate_safety_M(self, M_Rd: float) -> float:
        ''' Calculation of safety degree for moment capacity.
        Args:
            M_Rd(float):  Moment capacity [kNm]
        Returns:
            M_safety(float):  safety degree for moment capacity [%]
        '''
        safety = (M_Rd / self.M_Ed) * 100

        return round(safety,1)
    
    def calculate_safety_V(self, V_Rd: float, V_Ed: float) -> float:
        ''' Calculation safety degree for shear capacity. Use the shear capacity V_Rds for calculation-based 
        need for shear reinforcement instead of the ordinary shear capacity if the capacity is not suifficent.
        Args: 
            V_Rd(float):  Shear capacity [kNm]
            V_Ed(float):  Design shear force, from Load properties class [kNm]
        Returns:
            V_safety(float):  safety degree for shear capacity [%]
        '''
        safety = (V_Rd / V_Ed) * 100
        return round(safety,1)


    

