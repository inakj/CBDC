
''' This script contain the Uncracked stress class that apply for prestressed reinforced cross section.
'''

class Uncracked_stress:
    '''Class to contain calculation of uncracked prestressed
    cross section. All calculations are done according to the standard NS-EN 1992-1-1:2004 (abbreviated to EC2) and the 
    book "Betongkonstruksjoner; beregning og dimensjonering etter Eurocode 2" by Svein Ivar Sørensen.
    '''

    def __init__(self, material, cross_section, load):
        '''Args:
            cross_section:  instance from Cross section class that contain all cross-section properties
            material:  instance from Material class that contain all material properties
            load:  instance from Load properties class that contain all load properties 
        Returns:    
            netta(float):  material stiffness ratio 
            At(float):  transformed cross section area [mm2]
            yt(float):  distance between reinforced gravity axis and concrete gravity axis [mm]
            It(float):  moment of inertia for tranforsmed cross section [mm4]
            sigma_c_uncracked(float):  concrete stress for uncracked cross section [N/mm2]
        '''
        self.netta = self.calculate_netta(material.Ep, material.Ecm)
        self.At = self.calculate_At(cross_section.Ac, self.netta, cross_section.Ap)
        self.yt = self.calculate_yt(self.netta, cross_section.Ap, cross_section.e, self.At)
        self.It = self.calculate_It(cross_section.width, cross_section.height, self.yt, self.netta, cross_section.Ap, cross_section.e)
        self.sigma_c_uncracked = self.calculate_concrete_stress_uncracked(cross_section.height, load.P0_d, self.At, self.It, self.yt, cross_section.e)
       
    def calculate_netta(self, Ep: int, Ecm: float) -> float:
        ''' Function that calculates matierial stiffness ratio netta
        Args:
            Ep(int):  elasiticity modulus for prestressed steel, from Input class [N/mm2]
            Ecm(float):  elasticity modulus for concrete[N/mm2]
        Returns:
            netta(float): material stiffness ratio
        '''
        netta = Ep / Ecm 
        return netta
    
    def calculate_At(self, Ac: float, netta: float, Ap: float) -> float:
        ''' Function that calculates transformed cross section
        Args:
            Ac(float):  concrete area, from Cross section class [mm2]
            netta(float):  material stiffness ratio 
            Ap(float):  area of prestress reinforcement, from Cross section class [mm2]
        Returns:
            At(float):  transformed cross section area [mm2]
        '''
        At = Ac + (netta - 1) * Ap # From Sørensen (6.6)
        return At
    
    def calculate_yt(self, netta: float, Ap: float, e: float, At: float) -> float:
        ''' Function that calculates distance yt
        Args: 
            netta(float):  material stiffness ratio 
            Ap(float):  area of prestress reinforcement, from Cross section class [mm2] 
            e(float):  distance from bottom to prestressed reinforcement, from Cross section class [mm]
            At(float):  transformed cross section area [mm2]
        Returns:
            yt(float):  distance between reinforced gravity axis and concrete gravity axis [mm]
        '''
        y_t = ((netta - 1) * Ap * e) / At # From Sørensen (6.7)
        return y_t
    
    def calculate_It(self, width: float, height: float, yt: float, netta: float, Ap: float, e: float) -> float:
        ''' Function that calculates moment of inertia 
        Args: 
            width(float):  width of cross section, from Cross section class [mm]
            height(float):  height of cross section, from Cross section class [mm]
            yt(float):  distance between reinforced gravity axis and concrete gravity axis [mm]
            netta(float):  material stiffness ratio
            Ap(float):  area of prestress reinforcement, from Cross section class [mm2] 
            e(float):  distance from bottom to prestressed reinforcement, from Cross section class [mm]
        Returns:
            It(float):  moment of inertia for transformed cross section [mm4]
        '''
        It = (width * height ** 3) / 12 + width * height * yt ** 2 + (netta - 1) * Ap * (e - yt) ** 2 # From Sørensen (6.8)
        return It

    def calculate_concrete_stress_uncracked(self, height: float, P0: float, At: float, It: float, yt: float,
                                  e: float) -> float:
        ''' Funtion that calculates concrete stress because of prestress 
        Args:
            height(float):  height of cross section, from Cross section class [mm]
            P0(float):  prestress force, from Load properties class [kN]
            At(float):  transformed cross section area [mm2]
            It(float):  moment of inertia for tranforsmed cross section [mm4]
            yt(float):  distance between reinforced gravity axis and concrete gravity axis [mm]
            e(float):  distance from bottom to prestressed reinforcement, from Cross section class [mm]
        Returns: 
            sigma_c_uncracked = [sigma_c_under,sigma_c_over,sigma_c_prestress]
            where: 
            sigma_c_under:  concrete stress i top of beam [N/mm2]
            sigma_c_over:  concrete stress in bottom of beam [N/mm2]
            sigma_c_prestress:  concrete stress in line with prestress [N/mm2]
        '''
        N = - P0 # From Sørensen (6.10a)

        Mt =  N * (e - yt) # From Sørensen (6.10b)

        y = height / 2 # in the bottom of the cross section
        sigma_c_under = N / At + Mt / (It / (y-yt)) # From Sørensen (6.11)

        y = - height / 2 # in the top of the cross section
        sigma_c_over = N / At + Mt / (It / (y-yt)) # From Sørensen (6.11)

        y = e # at the height of the prestressed reinforcement
        sigma_c_prestress = N / At + Mt / (It / (y-yt)) # From Sørensen (6.11)

        sigma_c_uncracked = [sigma_c_under,sigma_c_over,sigma_c_prestress]
        return sigma_c_uncracked

    
