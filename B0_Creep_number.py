
''' This script contain the Creep number class that apply for all reinforcement cases.
'''

class Creep_number:
    ''' Class that contain creep number calculation from EC2, annex B.
    '''
    
    def __init__(self, cross_section, material, t0_self: int, t0_live: int, RH: int, cement_class: str, t: int = 18263):
        '''Args: 
            cross_section:  instance from Cross section class that contain all cross section properties
            material:  instance from the Material class that conatin all material properties
            t0_self(int):  time of applied self load, from Input class  [days]
            t0_live(int):  time of applied live load, from Input class  [days]
            RH(int):  relative humidity, from Input class [%]
            cement_class(string):  cement class 'N','S' or 'R', from Input class 
            t(int):  concrete age at the considered time, assumed 50 years [days]
        Returns: 
            h0(float): effective cross section thickness [mm]
            beta_fcm(float):  factor that takes into account concrete strength 
            phi_RH(float):  factor that takes into account the effect of relative humidity 
            t0_adjusted_self(float):  adjusted selfload application age because of effect from cement type [days]
            t0_adjusted_live(float):  adjusted liveload application age because of effect from cement type [days]
            beta_t0_self(float):  factor that take into acount the effect of concrete age of selfload application
            beta_t0_live(float):  factor that take into acount the effect of concrete age of liveload application
            phi_0_self(float):  standardized creep number for selfload
            phi_0_live(float):  standardized creep number for liveload
            beta_c(float):  factor to describe creep development compared to time after applied load
            phi_self(float):  creep number for selfload
            phi_live(float):  creep number for liveload
        '''
        self.h0 = self.calculate_h0(cross_section.Ac, cross_section.width, cross_section.height)
        self.beta_fcm = self.calculate_beta_fcm(material.fcm)
        self.phi_RH = self.calculate_phi_RH(self.h0, material.fcm, RH)
        self.t0_adjusted_self = self.calculate_t0_adjusted(t0_self, cement_class)
        self.t0_adjusted_live = self.calculate_t0_adjusted(t0_live, cement_class)
        self.beta_t0_self = self.calculate_beta_t0(self.t0_adjusted_self)
        self.beta_t0_live = self.calculate_beta_t0(self.t0_adjusted_live)
        self.phi_0_self = self.calculate_phi_0(self.phi_RH, self.beta_fcm, self.beta_t0_self)
        self.phi_0_live = self.calculate_phi_0(self.phi_RH, self.beta_fcm, self.beta_t0_live)
        self.beta_c = self.calculate_beta_c(t0_self, t, RH, self.h0, material.fcm)
        self.phi_selfload = self.calcualte_phi(self.phi_0_self, self.beta_c)
        self.phi_liveload = self.calcualte_phi(self.phi_0_live, self.beta_c)

    def calculate_h0(self, Ac: float, width: float, height: float) -> float: 
        ''' Function that calculates effective cross section thickness 
        Args:
            Ac(float):  concrete area, from cross section class [mm2]
            width(float):  width of cross section, defined by user[mm]
            height(float):  height of cross section, defined by user [mm]
        Returns:
            h0(float): effective cross section thickness [mm]
        '''
        h0 = (2 * Ac) / (2 * (width + height)) # From (B.6)
        return h0
    
    def calculate_beta_fcm(self, fcm: int) -> float:
        ''' Function that calculates the factor beta_cm that takes into account concrete strength on the
        standardized creepnumer
        Args: 
            fcm(int):  middlevalue of cylinder compressive strength, from material class [N/mm2]
        Returns:
            beta_fcm(float):  factor that takes into account concrete strength 
        '''
        beta_fcm = 16.8 / fcm ** 0.5 # From (B.4)
        return beta_fcm
   
    def calculate_phi_RH(self, h0: float, fcm: int, RH: int) -> float: 
        ''' Function that calculates phi_RH which takes into account the effect of relative humidity on the 
        standardized creepnumer
        Args:
            h0(float): effective cross section thickness [mm]
            fcm(int):  middlevalue of cylinder compressive strength, from material class [N/mm2]
            RH(in):  relative humidity, defined by user [%]
        Returns:
            phi_RH(float):  factor that takes into account the effect of relative humidity 
        '''
        alpha_1 = (35 / fcm) ** 0.7 # From (B.8c)
        alpha_2 = (35 / fcm) ** 0.2 # From (B.8c)

        if fcm <= 35:
            phi_RH = 1 + (1 - RH / 100) / (0.1 * h0 ** (1 / 3)) # From (B.3a)
        else:
            phi_RH = (1 + ((1 - RH / 100) / (0.1 * h0 ** (1/3))) * alpha_1) * alpha_2 # From (B.3b)

        return phi_RH

    def calculate_t0_adjusted(self, t0: int, cement_class: str) -> float:
        ''' Function that calcualtes the adjusted t0 because of effect from cement type
        Args:
            t0(int):  concrete age at load application, defined by user [days]
            cement_class(str):  cement class 'N','S' or 'R', defined by user
        Returns:
            t0_adjusted(float):  adjusted application age because of effect from cement type [days]
        Raises:
            ValueError:  if cement class is not R,N or S
        '''
        if cement_class == 'S':
            alpha_cement = -1
        elif cement_class == 'N':
            alpha_cement = 0
        elif cement_class == 'R':
            alpha_cement = 1
        else: 
            raise ValueError(f'cement_class={cement_class}, expected R, N or S')
        
        t0_adjusted = max (t0 * (9 / (2 + t0 ** 1.2) + 1) ** alpha_cement, 0.5) # From (B.9)
        return t0_adjusted
    
    def calculate_beta_t0(self, t0_adjusted: float) -> float: 
        ''' Function that calculates the factor beta_t0 that take into acount the effect of concrete age 
        when load is applied
        Args:
            t0_adjusted(float):  adjusted application age because of effect from cement type [days]
        Returns:
            beta_t0(float):  factor that take into acount the effect of concrete age when load is applied 
        '''
        beta_t0 = 1 / (0.1 + t0_adjusted ** 0.20) # From (B.5)
        return beta_t0
    
    def calculate_phi_0(self, phi_RH: float, beta_fcm: float, beta_t0: float) -> float: 
        ''' Function that calculates the standardized creep number 
        Args:
            phi_RH(float):  factor that takes into account the effect of relative humidity 
            beta_fcm(float):  factor that takes into account concrete strength 
            beta_t0(float):  factor that take into acount the effect of concrete age at application
        Returns:
            phi_0(float):  standardized creep number
        '''
        phi_0 = phi_RH * beta_fcm * beta_t0 # From (B.2)
        return phi_0

    
    def calculate_beta_c(self, t0: int, t: int, RH: int, h0: int, fcm: int) -> float: 
        ''' Function that calculates the factor beta:c that describes creep development compared to time after 
        applied load
        Args:
            t0(int):  concrete age at load application, defined by user [days]
            t(int):  concrete age at the considered time [days]
            RH(int):  relative humidity, defined by user [%]
            h0(float): effective cross section thickness [mm]
            fcm(int):  middlevalue of cylinder compressive strength, from material class [N/mm2]
        Returns:    
            beta_c(float):  factor to describe creep development compared to time after applied load
        '''
        alpha_3 = (35 / fcm) ** 0.5  # From (B.8c)

        if fcm <= 35:
            beta_H = min(1.5 * (1 + (0.012 * RH) ** 18) * h0 + 250, 1500) # From (B.8a)
        else:
            beta_H = min(1.5 * (1 + (0.012 * RH) ** 18) * h0 + 250 * alpha_3, 1500 * alpha_3) # From (B.8b)

        beta_c = ((t - t0) / (beta_H + t - t0)) ** 0.3  # From (B.7)
        return beta_c

    def calcualte_phi(self, phi_0: float, beta_c: float) -> float: 
        ''' Function that calculate creep number phi
        Args:
            phi_0(float):  standardized creep number
            beta_c(float):  factor to describe creep development compared to time after applied load
        Returns:
            phi(float):  creep number 
        '''
        phi = phi_0 * beta_c # From (B.1)
        return phi
    
