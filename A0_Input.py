#---------------------------INPUT-------------------------------------

class Input:
    def __init__(self):
        '''
        All input for the script is given here by the user. 
        The code works for a one span, simply supported beam, with distributed self- and live-load. The cross section must be rectangular. 
        The ordinary reinforcent must be in one layer. The prestressed reinforcement must also be in one layer.
        All values with a comment are where your input should be. Do not change the code or write something where there is no comments.

        Returns:

        - Material -

        concrete_class(str):  concrete class, characteristic strength of concrete 
        steel_class(str):  steel class, characteristic strenght of steel
        cement_class(str):  cement class
        relative_humidity(int):  relative humidity around beam
        exposure_class(str):   exposure class

        - Geometry -

        width(float):  width [mm]
        height(float):  height [mm]
        beam_length(float): length [m]

        - Reinforcement -

        nr_ordinary_reinforcement_bars(int):  nr of ordinary reinforcement bars
        ordinary_reinforcement_diameter(float):  ordinary reinforcement diameter mm]
        shear_reinforcement_diameter(float):  diameter of stirrup diameter / shear reinforcement [mm]
        shear_reinforcement(float):  shear reinforcement / stirrup reinforcement [mm2] / [mm]

        - Load -

        distributed_selfload(float):  characteristic selfload [kN/m]
        selfload_application(int):  when self-load is applied[days]
        distributed_liveload(float): characteristic liveload [kN/m]
        liveload_application(int):  when live-load is applied [days]
        percent_longlasting_liveload(int):  longlasting live-load [%]

        - Prestress - 

        is_the_beam_prestressed(bool):  True or False
        
        nr_prestressed_bars(int):  nr of prestressed reinforcement bars
        prestressed_reinforcment_diameter(float):  prestressed reinforcement diameter [mm]
        prestressed_reinforcment_name(str):  name of prestressed reinforcement
       
        - Prestress and ordinary -

        prestressed_and_ordinary_in_top(bool):  True or False 
        '''
       # Material attributes
        self.concrete_class: str    = 'C30'   # must be given with 'C + number' between 12 and 90
        self.steel_class: str       = 'B500NC' # must be given in this exact format 
        self.cement_class: str      = 'R'      # must be 'R', 'S' or 'N'
        self.relative_humidity: int  = 40      # relative humidity around beam, from 1 - 100[%]
        self.exposure_class: str    = 'XC1'  # must be one of the following 
                                               # ['X0','XC1','XC2','XC3','XC4','XD1','XS1','XD2','XD3','XS2','XS3']
        
        # Geometry attributes
        self.width: float        = 300 # width of cross section [mm]
        self.height: float       = 800 # height of cross section [mm]
        self.beam_length: float  = 10 # total length of beam [m]

        # Reinforcement attributes
        self.nr_ordinary_reinforcement_bars: int    = 4 # number of ordinary reinforcement bars in longitudinal direction
        self.ordinary_reinforcement_diameter: float = 20 # diameter of ordinary reinforcement bars in longitudinal direction [mm]
        self.shear_reinforcement_diameter: float                = 10 # diameter of stirrup diameter / shear reinforcement around the longitudinal bars [mm]
        self.shear_reinforcement: float             = 200 / 220 # shear reinforcement / stirrup reinforcement given as area of 
                                                         # reinforcement divided on distance between stirrups [mm2] / [mm]

        # Load attributes
        self.distributed_selfload: float        = 5 # evenly distributed characteristic selfload [kN/m]
        self.selfload_application: int          = 7 # days after casting when selfload is applied as load in calculation [days]
        self.distributed_liveload: float        = 30 # evenly distributed characteristic liveload [kN/m]
        self.liveload_application: int          = 90 # days after casting when liveload is applied as load in calculation [days]
        self.percent_longlasting_liveload: int  = 40 # part of liveload that is assumed to be longlasting [%]
            
        # Prestressed attributes    
        self.is_the_beam_prestressed: bool            =  False # if the beam is prestressed, write True here. If not, write False.
        if self.is_the_beam_prestressed              == True:
            # If the beam is prestressed, only change these the first three inputs insice the if-sentence
            # If the beam is not prestressed, do not change any of the values within this if-else sentence
            self.nr_prestressed_bars: int                 = 4 # number of prestressed reinforcement bars in longitudinal direction
            self.prestressed_reinforcment_diameter: float = 15.2 # diameter of prestressed reinforcement bars in longitudinal direction [mm]
            self.prestressed_reinforcment_name: str       = 'Y1770S7' # name of prestressed reinforcement, if not prestressed, type None
        else:
            self.nr_prestressed_bars: int                 = 0 # dont change this 
            self.prestressed_reinforcment_diameter: float = 0 # dont change this
            self.prestressed_reinforcment_name: str       = None # dont change this
       
        self.prestressed_and_ordinary_in_top: bool = False # if the beam is prestressed, but also have ordinary reinforcement in top, write True here, if not, write False)

#----------------------------------------------------------------------------
