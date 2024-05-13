
''' This script contain the Material class that apply for all reinforcement cases.
'''

class Material: 
    '''Material class to contain material properties used in calculations.
    All calculations are done according to the standards
    NS-EN 1992-1-1:2004 (abbreviated to EC2), NS-EN 1990:2002 and EN10138-3.
    '''
    def __init__(self, concrete_class: str, steel_class: str,
                 prestress_name: str, prestress_diameter: float):  
        '''Args:
            concrete_class (str): concrete class, from Input class 
            steel_class (str): steel class, from Input class 
            prestress_name (str): name of prestress type, from Input class , according to table 2 in EN10138-3
            prestress_diameter (float): diameter of prestressed reinforcement, from Input class , according to table 2 in EN10138-3
        Returns:
            - Load- and materialfactor attributes -

            gamma_shrinkage(float):  loadfactor for shrink
            gamma_0_9(float):  loadfactor for prestressing
            gamma_1_1(float):  loadfactors for prestressing
            gamma_selfload(float):  loadfactor for self-load
            gamma_liveload(float):  loadfactor for live-load
            gamma_concrete(float):  materialfactor for concrete
            gamma_reinforcement(float):  materialfactor for ordinary reinforcement steel
            gamma_prestressed_reinforcement(float):  materialfactor for prestressed reinforcement steel 

            - Concrete attributes - 

            fck(int):  cylinder compression strength [N/mm2] 
            fck_cube(int):  Cubic compressive strength [N/mm2]
            fcm(int):  middlevalue of cylinder compressive strength [N/mm2]
            fctm(float):  middlevalue of concrete axial tension strength [N/mm2]
            fctk_005(float):  0.05 % concrete characteristic axial tension strength [N/mm2]
            fctk_095(float):  0.95 % concrete characteristic axial tension strenght [N/mm2]
            Ecm(int):  Elasticity modulus for concrete [N/mm2]
            eps_c1(float):  compression strain for biggest stress 
            eps_cu1(float):  strain limit for compression
            eps_c2(float):  compression strain for biggest stress 
            eps_cu2(float):  strain limit for compression
            n(float):  exponent
            eps_c3(float):  compression strain for biggest stress 
            eps_cu3(float):  strain limit for compression 
            lambda_factor(float):  factor for effective height
            netta(float):  factor for effective strength
            alfa_cc(float):  design compressive strength coefficient
            alfa_ct(float):  design tensile strength coefficient 
            fcd(float):  design compressive strength [N/mm2]
            fctd(float):  design tensile strength [N/mm2]

            - Ordinary reinforcement attributes -

            fyk(int):  steel tensions characteristic strength [N/mm2]
            Es(int):  elasiticity modulus for steel [N/mm2]
            eps_yk(float):  characteristic yield strain
            fyd(float):  design tensile strength
            eps_yd(float):  design yield strain

            - Prestressed reinforcement attributes -

            Ep(int):  elasticity moduls for prestensioned steel [N/mm2]
            fpk(int):  tensile strength for prestress [N/mm2]
            Ap(float):  cross sectional area for prestress [mm2] 
            Fpk(float):  characteristic maximum force for prestressing [kN] 
            Fp01k(float):  characteristic 0.1% proof force [kN] 
            fp01k(float):  characteristic 0.1% proof stress [N/mm2] 
            fpd(float):  design 0.1% proof stress [N/mm2] 
        '''

    # LOAD- AND MATERIALFACTORS
        
        # Loadfactor for shrink calculation according to EC2 NA.2.4.2.1
        self.gamma_shrinkage: float = 1 
        # Loadfactors for prestressing, using the most unfavorable one according to EC2 NA.2.4.2.2(1) 
        self.gamma_0_9: float = 0.9 
        self.gamma_1_1: float = 1.1 
        # Loadfactors for external load
        # For simplicity chosen unfavorable values from NS-EN 1992-1-1:2004 table NA.A1.2(A)
        self.gamma_selfload: float = 1.2 
        self.gamma_liveload: float = 1.5
        # Materialfactors according to EC2 NA.2.4.2.4(1)
        self.gamma_concrete: float = 1.5
        self.gamma_reinforcement: float = 1.15
        self.gamma_prestressed_reinforcement: float = 1.15

    
    # CONCRETE PARAMETERS
        
        index = self.get_index(concrete_class)
        self.fck = self.get_fck(index)
        self.fck_cube = self.get_fck_cube(index)
        self.fcm = self.get_fcm(index)
        self.fctm = self.get_fctm(index)
        self.fctk_005 = self.get_fctk_005(index)
        self.fctk_095 = self.get_fctk_095(index)
        self.Ecm = self.get_Ecm(index)
        self.eps_c1 = self.get_eps_c1(index)
        self.eps_cu1 = self.get_eps_cu1(index)
        self.eps_c2 = self.get_eps_c2(index)
        self.eps_cu2 = self.get_eps_cu2(index)
        self.n = self.get_n(index)
        self.eps_c3 = self.get_eps_c3(index)
        self.eps_cu3 = self.get_eps_cu3(index)
        self.lambda_factor = self.calculate_lambda(self.fck)
        self.netta_factor = self.calculate_netta(self.fck)

        # Design compressive- and tension strength coefficients fraccording to EC2 NA.3.1.6
        self.alfa_cc: float = 0.85 
        self.alfa_ct: float = 0.85  
        # Design compression strength according to EC2 3.1.6(1)
        self.fcd: float = self.fck * self.alfa_cc / self.gamma_concrete 
        # Design tension strength according to EC2 3.1.6(2)
        self.fctd: float = self.fctk_005 * self.alfa_ct / self.gamma_concrete 
    
    # ORDINARY REINFORCEMENT PARAMETERS
        
        self.fyk = self.get_fyk(steel_class)
        self.Es = self.get_Es()

        # Characteristic yield strain
        self.eps_yk: float = self.fyk / self.Es

        # Design tension strength according to EC2 3.2.7(2)
        self.fyd: float = self.fyk / self.gamma_reinforcement

        # Design yield strain
        self.eps_yd: float = self.fyd / self.Es 
    
    # PRESTRESSED REINFORCEMENT PARAMETERS
       
        self.Ep = self.get_Ep()
        index_prestress = self.get_index_prestress(prestress_name, prestress_diameter)   
        self.fpk = self.get_fpk(index_prestress)
        self.Ap_strand = self.get_Ap(index_prestress)
        self.Fpk = self.get_Fpk(index_prestress)
        self.Fp01k = self.get_Fp01k(index_prestress)
        self.fp01k = self.calculate_fp01k(self.Fp01k, self.Ap_strand, index_prestress)
        self.fpd = self.calculate_fpd(self.fp01k, index_prestress)
        
       
#-------------CONCRETE PARAMETERS---------------------------------------------------------------------
        
    def get_index(self, concrete_class: str) -> int: 
        ''' Get index to decide concrete parameters according to concrete class and table 3.1 in EC2.
        Args:
            concrete_class(string):  defined by user
        Returns:
            index(int):  for defining parameters from table 3.1
        Raises:
            ValueError:  If the concrete class do not exist
        '''
        match concrete_class:
            case 'C12':
                return 0
            case 'C16':
                return 1
            case 'C20':
                return 2
            case 'C25':
                return 3
            case 'C30':
                return 4
            case 'C35':
                return 5
            case 'C40':
                return 6
            case 'C45':
                return 7
            case 'C50':
                return 8
            case 'C55':
                return 9
            case 'C60':
                return 10 
            case 'C70':
                return 11
            case 'C80':
                return 12
            case 'C90':
                return 13
            case _:
                raise ValueError(f'Concrete class {concrete_class} do not exist')
    
    def get_fck(self, index: int) -> int:
        ''' Get compression strength fck based on index number and table 3.1 in EC2.
        Args:
            index(int):  for defining parameters from table 3.1
        Returns:
            fck(int):  cylinder compression strength [N/mm2]
        '''
        fck_vektor = [12, 16, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80, 90]
        return fck_vektor[index]
    
    def get_fck_cube(self, index: int) -> int:
        ''' Get compressive strength fck_cube based on index number and table 3.1 in EC2.
        Args:
            index(int):  for defining parameters from table 3.1
        Returns:
            fck_cube(int):  Cubic compressive strength [N/mm2]
        '''
        fck_cube_vektor = [15, 20, 25, 30, 37, 45, 50, 55, 60, 67, 75, 85, 95, 105]
        return fck_cube_vektor[index]
    
    def get_fcm(self, index: int) -> int:
        ''' Get compressive strength fcm based on index number and table 3.1 in EC2.
        Args:
            index(int):   for defining parameters from table 3.1
        Returns:
            fcm(int):  middlevalue of cylinder compressive strength [N/mm2]
            '''
        fcm_vektor = [20, 24, 28, 33, 38, 43, 48, 53, 58, 63, 68, 78, 88, 98]
        return fcm_vektor[index]

    def get_fctm(self, index: int) -> float:
        ''' Get tension strength fctm based on index number and table 3.1 in EC2.
        Args:
            index(int):  for defining parameters from table 3.1
        Returns:
            fctm(float):  middlevalue of concrete axial tension strength [N/mm2]
            '''
        fctm_vektor = [1.6, 1.9, 2.2, 2.6, 2.9, 3.2, 3.5, 3.8, 4.1, 4.2, 4.4, 4.6, 4.8, 5.0]
        return fctm_vektor[index]

    def get_fctk_005(self, index: int) -> float:
        ''' Get tension strength fct_005 based on index number and table 3.1 in EC2.
        Args:
            index(int):  for defining parameters from table 3.1
        Returns:
            fctk_005(float):  0.05 % concrete characteristic axial tension strength [N/mm2]
        '''
        fctk_005_vektor = [1.1, 1.3, 1.5, 1.8, 2.0, 2.2, 2.5, 2.7, 2.9, 3.0, 3.1, 3.2, 3.4, 3.5]
        return fctk_005_vektor[index]
        
    def get_fctk_095(self, index: int) -> float:
        ''' Get tension strength fctk_095 based on index number and table 3.1 in EC2.
        Args:
            index(int):  for defining parameters from table 3.1
        Returns:
            fctk_095(float):  0.95 % concrete characteristic axial tension strenght [N/mm2]
        '''
        fctk_095_vektor = [2.0, 2.5, 2.9, 3.3, 3.8, 4.2, 4.6, 4.9, 5.3, 5.5, 5.7, 6.0, 6.3, 6.6]
        return fctk_095_vektor[index]
    
    def get_Ecm(self, index: int) -> int:
        ''' Get elasiticty modulus Ecm based on index number and table 3.1 in EC2.
        Multiplied with 1000 to get from GPa (as its given in the table) to MPa
        Args:
            index(int):  for defining parameters from table 3.1
        Returns:
            Ecm(int):  Elasticity modulus for concrete [N/mm2]
        '''
        Ecm_vektor = [27, 29, 30, 31, 33, 34, 35, 36, 37, 38, 39, 41, 42, 44] 
        return Ecm_vektor[index] * 1000 

    def get_eps_c1(self, index: int) -> float:
        ''' Get strain eps_c1 for a non-linear analysis based on index number and table 3.1 in EC2.
        Divided on 1000 to get form percent to decimal number.
        Args:
            index(int):  for defining parameters from table 3.1
        Returns:
            eps_c1(float):  compression strain for biggest stress
        '''
        eps_c1_vektor = [1.8, 1.9, 2.0, 2.1, 2.2, 2.25, 2.3, 2.4, 2.45, 2.5, 2.6, 2.7, 2.8, 2.8]
        return eps_c1_vektor[index] / 1000

    def get_eps_cu1(self, index: int) -> float:
        ''' Get strain limit eps_cu1 for a non-linear analysis based on index number and table 3.1 in EC2.
        Divided on 1000 to get form percent to decimal number
        Args:
            index(int):  for defining parameters from table 3.1
        Returns:
            eps_cu1(float):  strain limit for compression 
        '''
        eps_cu1_vektor = [3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.2, 3.0, 2.8, 2.8, 2.8]
        return eps_cu1_vektor[index] / 1000


    def get_eps_c2(self, index: int) -> float:
        ''' Get strain eps_c2 for a parabolic analysis based on index number and table 3.1 in EC2.
        Divided on 1000 to get form percent to decimal number
        Args:
            index(int):  for defining parameters from table 3.1
        Returns:
            eps_c2(float):  compression strain for biggest stress 
        '''
        eps_c2_vektor = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.2, 2.3, 2.4, 2.5, 2.6]
        return eps_c2_vektor[index] / 1000
  
    def get_eps_cu2(self, index: int) -> float:
        ''' Get strain limit eps_cu2 for a parabolic analysis based on index number and table 3.1 in EC2.
        Divided on 1000 to get form percent to decimal number
        Args:
            index(int):  for defining parameters from table 3.1
        Returns:
            eps_cu2(float):  strain limit for compression 
        '''
        eps_cu2_vektor = [3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.1, 2.9, 2.7, 2.6, 2.6]
        return eps_cu2_vektor[index] / 1000
    
    def get_n(self, index: int) -> float:
        ''' Get exponent n based on index number and table 3.1 in EC2.
        Args:
            index(int):  for defining parameters from table 3.1
        Returns:
            n(float):  exponent
        '''
        n_vektor = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.75, 1.6, 1.45, 1.4, 1.4]
        return n_vektor[index]

    def get_eps_c3(self, index: int) -> float:
        ''' Get strain eps_c3 for a bilinear or rectangular analysis based on index number and table 3.1 in EC2.
        Divided on 1000 to get form percent to decimal number
        Args:
            index(int):  for defining parameters from table 3.1 
        Returns:
            eps_c3(float):  compression strain for biggest stress 
        '''
        eps_c3_vektor = [1.75, 1.75, 1.75, 1.75, 1.75, 1.75, 1.75, 1.75, 1.75, 1.8, 1.9, 2.0, 2.2, 2.3]
        return eps_c3_vektor[index] / 1000
    
    def get_eps_cu3(self, index: int) -> float:
        ''' Get strain limit eps_cu3 for a bilinear or rectangular analysis based on index number and table 3.1 in EC2.
        Divided on 1000 to get form percent to decimal number
        Args:
            index(int):  for defining parameters from table 3.1
        Returns:
            eps_cu3(float):  strain limit for compression 
        '''
        eps_cu3_vektor = [3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.1, 2.9, 2.7, 2.6, 2.6]
        return eps_cu3_vektor[index] / 1000
    
    def calculate_lambda(self, fck: int) -> float:
        ''' Function that calculate a factor lambda which defines the effective height for 
        compression zone in concrete, according to EC2 3.1.7(3)
        Args:
            fck(int):  cylinder compression strength [N/mm2]
        Returns:
            lambda_factor(float): factor for effective height
        '''
        if fck <= 50:
            self.lambda_factor = 0.8
        elif 50 < fck <= 90:
            self.lambda_factor = 0.8 - (fck / 50) / 400

        return self.lambda_factor 
    
    def calculate_netta(self, fck: int) -> float:
        ''' Function that calculate a factor netta which defines the effective strength, 
        according to EC2 3.1.7(3)
        Args:
            fck(int):  cylinder compression strength [N/mm2]
        Returns: 
            netta(float):  factor for effective strength
        '''
        if fck <= 50:
            self.netta = 1.0
        elif 50 < fck <= 90:
            self.netta = 1.0 - (fck / 50) / 200

        return self.netta

# ----------------------STEEL PARAMETERS---------------------------------------------------------------
    
    def get_fyk(self, steel_class: float ) -> int:
        '''Get reinforcements characteristic strength fyk based on steel class.
        Args:
            steel_class(str): defined by user
        Returns:
            fyk(int):  steel tensions characteristic strength [N/mm2]
        '''
        fyk = steel_class
        return fyk

    def get_Es(self) -> int:
        '''Get elasiticity modulus for steel Es according to EC2 3.2.7(4).
        Returns:
            Es(int):  elasiticity modulus for steel [N/mm2]
        '''
        Es = 2 * 10 ** 5
        return Es
    
    def get_Ep(self) -> int:
        '''Get elasticity modulus for prestressing according to EC2 3.3.6(3)
        Returns:
            Ep(int):  elasticity moduls for prestensioned steel [N/mm2]
        '''
        Ep = 1.95 * 10 ** 5
        return Ep

    def get_index_prestress(self, prestress_name: str, prestress_diameter: str) -> int: 
        '''Get index based on name of prestressing material from table 2 in EN10138-3.
        Args: 
            prestress_name(string):  defined by user
        Returns:
            index(int):  determining parameters for prestress or "None" if the name do not exist.
        '''
        if prestress_name == 'Y1860S3':
            match prestress_diameter:
                case 6.5:
                    return 1
                case 6.8:
                    return 2
                case 7.5:
                    return 3
        elif prestress_name == 'Y1860S7':
            match prestress_diameter:
                case 7.0:
                    return 4
                case 9.0:
                    return 5
                case 11.0:
                    return 6
                case 12.5:
                    return 7
                case 13.0:
                    return 8
                case 15.2:
                    return 9
                case 16.0:
                    return 10 
        elif prestress_name == 'Y1770S7':
            match prestress_diameter:
                case 15.2:
                    return 11
                case 16.0:
                    return 12
                case 18.0:
                    return 13
        elif prestress_name == None:
            return None
        else:
            match prestress_name:
                case 'Y19060S3':
                    return 0
                case 'Y1860S7G':
                    return 14
                case 'Y1820S7G':
                    return 15
                case 'Y1700S7G':
                    return 16
                case 'Y2160S3':
                    return 17
                case 'Y2060S3':
                    return 18
                case 'Y1960S3':
                    return 19
                case 'Y2160S7':
                    return 20
                case 'Y2060S7':
                    return 21
                case 'Y1960S7':
                   return 22
    
        
    def get_fpk(self, index_prestress: int) -> int: 
        '''Get tensile strength for prestress based on index and table 2 in EN10138-3.
        Args:
            index(int):  for determining parameters for prestress or "None" if the name do not exist
        Returns:
            fpk(int):  tensile strength for prestress [N/mm2] or 0 if the index == None
        '''
        if index_prestress == None:
            return 0
        else: 
            fpk = [1960, 1860, 1860, 1860, 1860, 1860, 1860, 1860, 1860, 1860, 1860, 1770,
             1770, 1770, 1860, 1820, 1700, 2160, 2060, 1960, 2160, 2060, 1960]
            return fpk[index_prestress]

    def get_Ap(self, index_prestress: int) -> float:
        '''Get area of each prestress strand based on index and table 2 in EN10138-3.
        Args:
            index(int):  for determining parameters for prestress or "None" if the name do not exist
        Returns:
            Ap(float):  cross sectional area for prestress [mm2] or 0 if the index == None
        '''
        if index_prestress == None:
            return 0
        else: 
            Ap = [13.6, 21.1, 23.4, 20, 30, 50, 75, 93, 100,
             140, 150, 140, 150, 200, 112, 165, 223, 13.6, 13.6, 21.2, 28.2, 30, 50]
            return Ap[index_prestress]
    
    def get_Fpk(self, index_prestress: int) -> float:
        '''Get characteristic maximum force Fm based on index and table 2 in EN10138-3.
        Args:
            index(int):  for determining parameters for prestress or "None" if the name do not exist
        Returns:
            Fpk(float):  characteristic maximum force for prestressing [kN] or 0 if the index == None
        '''
        if index_prestress == None:
            return 0
        else: 
            Fpk = [26.6, 39.2, 43.5, 54, 56, 93, 140, 173, 186, 260, 279, 248, 265, 354, 209, 300, 
                    380, 29.4, 28, 41.4, 60.9, 62, 98]
            return Fpk[index_prestress]
    
    
    def get_Fp01k(self, index_prestress: int) -> float:
        '''Get characteristic 0.1% proof force for prestress based on index and table 2 in EN10138-3.
        Args:
            index(int):  for determining parameters for prestress or "None" if the name do not exist
        Returns:
            Fp01k(float):  characteristic 0.1% proof force [kN] or 0 if the index == None
        '''
        if index_prestress == None:
            return 0
        else: 
            Fp01k = [22.9, 33.8, 37.4, 46.4, 48, 80, 120, 149, 160, 224, 240, 213, 228, 304, 180, 258, 
                     327, 26.2, 24.1, 35.6, 52.4, 53,84]
            return Fp01k[index_prestress]
    
    def calculate_fp01k(self, Fp01k: float, Ap: float, index_prestress: int)-> float:
        '''Calculate characteristic 0.1% proof tension for prestress
        Args:
            Fp01k(float):  characteristic 0.1% proof force [kN]
            Ap(float):  cross sectional area for prestress [mm2]
            index(int):  for determining parameters for prestress or "None" if the name do not exist
        Returns:
            fp01k(float):  characteristic 0.1% proof stress [N/mm2] or 0 if the index == None
        '''
        if index_prestress == None:
            return 0
        else: 
            fp01k = Fp01k * 10 ** 3 / Ap 
            return fp01k
        
    def calculate_fpd(self, fp01k: float, index_prestress: int)-> float:
        '''Calculate design c 0.1% proof tension for prestress
        Args:
            fp01k(float):  characteristic 0.1% proof stress [kN]
            index(int):  for determining parameters for prestress or "None" if the name do not exist
        Returns:
            fpd(float):  design 0.1% proof stress [N/mm2] or 0 if the index == None
        '''
        if index_prestress == None:
            return 0
        else: 
            fpd: float = fp01k / self.gamma_prestressed_reinforcement 
            return fpd
    
    
