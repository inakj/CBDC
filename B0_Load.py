
''' This script contain the Load properties class that apply for all reinforcement cases.
'''

class Load_properties:
    '''Load class to contain load properties used in calculations. 
    All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2)
    '''
    def __init__(self, selfload: float, liveload: float, length: float, material, cross_section):
        '''Args:
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

        '''
        self.g_k: float = selfload
        self.p_k: float = liveload
        self.q_k = self.calculate_q_k(self.g_k, self.p_k)
        self.g_d = self.calculate_design_values_of_load(self.g_k, self.p_k, material.gamma_selfload, material.gamma_liveload)[0]
        self.p_d = self.calculate_design_values_of_load(self.g_k, self.p_k, material.gamma_selfload, material.gamma_liveload)[1]
        self.q_d = self.calculate_design_values_of_load(self.g_k, self.p_k, material.gamma_selfload, material.gamma_liveload)[2]
        self.Mg_k = self.calculate_Mg_k(self.g_k, length)
        self.Mp_k = self.calculate_Mp_k(self.p_k, length)
        self.M_k = self.calculate_M_k(self.Mg_k, self.Mp_k)
        self.Mg_d = self.calculate_Mg_d(self.g_d, length)
        self.Mp_d = self.calculate_Mg_d(self.p_d, length)
        self.M_Ed = self.calculate_M_Ed(self.Mg_d, self.Mp_d)
        self.V_k = self.calculate_V_k(self.q_k, length)
        self.V_Ed = self.calculate_V_Ed(self.q_d, length)
        self.sigma_p_max = self.calculate_sigma_p_max(material.fpk, material.fp01k)
        self.P0_d = self.calculate_P0_max(self.sigma_p_max, cross_section.Ap)
        self.M_prestress = self.calculate_M_prestressed(self.P0_d, cross_section.e)

    def calculate_q_k(self, g_k: float, p_k: float) -> float:
        '''Calculate the total characteristic load
        Args:
            g_k(float):  characteristic selfload [kN/m]
            p_k(float):  characteristic liveload [kN/m]
        Returns:
            q_k(float):  characteristic load [kN/m]
        '''
        q_k = g_k + p_k
        return q_k


    def calculate_design_values_of_load(self, g_k: float, p_k: float, gamma_selfload: float, gamma_liveload: float) -> float:
        '''Calculate the design values for self-load, live-load and total design load based on characteristic values
        Args:
            g_k(float):  characteristic selfload [kN/m]
            p_k(float):  characteristic liveload [kN/m]
            q_k(float):  characteristic load [kN/m]
            gamma_selfload(float):  loadfactor for self-load
            gamma_liveload(float):  loadfactor for live-load
        Returns:
            design_loads = [g_d, p_d, q_d]
            where:
            g_d(float):  design selfload, including load factor [kN/m]
            p_d(float):  design liveload, including load factor [kN/m]
            q_d(float):  design load, including load factor [kN/m]
        '''
        g_d = g_k * gamma_selfload
        p_d = p_k * gamma_liveload
        q_d = g_d + p_d
        design_loads = [g_d, p_d, q_d]
        return design_loads

    def calculate_Mg_k(self ,g: float, length: float) -> float:
        ''' Function that calculates characteristic moment because of selfload
        Args:
            g(float):  characteristic selfload [kN/m]
            length(float): length of beam [m]
        Returns:
            Mg_k(float):  moment because of characteristic selfload [kNm]
        '''
        Mg_k = (g * length ** 2) / 8
        return Mg_k
    
    def calculate_Mp_k(self, p: float, length: float) -> float:
        '''Function that calculates characteristic moment because of liveload

        Args:
            p(float):  characteristic liveload [kN/m]
            length(float): length of beam [m]
        Returns:
            Mp_k(float):  moment because of characteristic liveload [kNm]
        '''
        Mp_k = (p * length ** 2) / 8
        return Mp_k
    

    def calculate_M_k(self, Mg_k: float, Mp_k: float) -> float:
        ''' Function that calculates SLS moment
        Args:
            Mg_k(float):  moment because of characteristic selfload [kNm]
            Mp_k(float):  moment because of characteristic liveload [kNm]
        Returns:
            M_k(float):  total moment because of characteristic load [kNm]
        '''
        M_k = Mg_k + Mp_k
        return M_k
    
    def calculate_Mg_d(self, g: float, length: float) -> float:
        '''Function that calculates design moment because of selfload

        Args:
            g(float):  design selfload [kN/m]
            length(float): length of beam [m]
        Returns:
            Mg_d(float):  moment because of design selfload [kNm]
        '''
        Mg_d = (g * length ** 2) / 8
        return Mg_d

    def calculate_Mp_d(self, p: float, length: float) -> float:
        '''Function that calculates design moment because of liveload

        Args:
            p(float):  design liveload [kN/m]
            length(float): length of beam [m]
        Returns:
            Mp_d(float):  moment because of design liveload [kNm]
        '''
        Mp_d = (p * length ** 2) / 8
        return Mp_d

    def calculate_M_Ed(self, Mg_d: float, Mp_d: float) -> float:
        ''' Function that calculates ULS moment
        Args:
            Mg_d(float):  moment because of design selfload [kNm]
            Mp_d(float):  moment because of design liveload [kNm]
        Returns:
            M_Ed(float):  total moment because of design load [kNm]
        '''
        M_Ed = Mg_d + Mp_d
        return M_Ed

    def calculate_V_k(self, q: float, length: float) -> float:
        ''' Function that calculates shear force
        Args:
            q(float):  total characteristic load [kN/m]
            length(float): length of beam [m]
        Returns:
            V_k(float):  shear force because of characteristic load [kN]
        '''
        V_k = q * length / 2 
        return V_k
    
    def calculate_V_Ed(self, q: float, length: float) -> float:
        ''' Function that calculates shear force
        Args:
            q(float):  total design load [kN/m]
            length(float): length of beam [m]
        Returns:
            V_Ed(float):  shear force because of design load [kN]
        '''
        V_Ed = q * length / 2 
        return V_Ed 
    
# ---------------- PRESTRESS VALUES --------------------------------------------

    def calculate_sigma_p_max(self, fpk: float, fp01k: float) -> float:
        ''' Functon that calculates sigma_p_max according to EC2 5.10.2.1(1)
        Args: 
            fpk(int):  tensile strength for prestress from material class [N/mm2]
            fp01k(float):  characteristic 0.1% proof force from material class [N/mm2]
        Returns:
            sigma_p_max(float):  design value of prestressing stress [N/mm2]
        '''
        sigma_p_max = min(0.8 * fpk, 0.9 * fp01k)
        return sigma_p_max 
    
    def calculate_P0_max(self, sigma_p_max: float, Ap: float) -> float:
        ''' Function that calculates P0_max according to EC2 5.10.2.1(1)
        Args: 
            sigma_p_max(float):  design value of prestressing stress [N/mm2]
            Ap(float):  prestressed reinforcement area in cross section [mm2]
        Returns:
        P0_max(float): design value of prestressign force [N]
        '''
        P0_max = sigma_p_max * Ap 
        return P0_max 
   
    def calculate_M_prestressed(self, P0: float, e: float) -> float:
        ''' Function that calculates moment because of prestressing 
        Args:
            P0(float):  inital prestressing force [kN]
            e(float):  distance from bottom to middle of prestressed reinforcement [mm]
        Returns:
            M_prestress(float):  moment because of prestressing [kNm]
        '''
        M_prestress = - P0 * e * 10 ** -6
        return M_prestress