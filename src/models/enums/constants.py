from enum import IntEnum, StrEnum


class Brand(StrEnum):
    TOYOTA = "Toyota"
    HONDA = "Honda"
    CHEVROLET = "Chevrolet"
    VOLKSWAGEN = "Volkswagen"
    FORD = "Ford"
    FIAT = "Fiat"
    HYUNDAI = "Hyundai"
    NISSAN = "Nissan"
    RENAULT = "Renault"
    JEEP = "Jeep"
    BMW = "BMW"
    MERCEDES_BENZ = "Mercedes-Benz"
    AUDI = "Audi"
    MITSUBISHI = "Mitsubishi"
    KIA = "Kia"
    PEUGEOT = "Peugeot"
    CITROEN = "Citroën"
    SUBARU = "Subaru"
    VOLVO = "Volvo"
    LAND_ROVER = "Land Rover"


class CarModel(StrEnum):
    COROLLA = "Corolla"
    HILUX = "Hilux"
    YARIS = "Yaris"
    SW4 = "SW4"
    RAV4 = "RAV4"
    CIVIC = "Civic"
    HR_V = "HR-V"
    FIT = "Fit"
    CR_V = "CR-V"
    ONIX = "Onix"
    TRACKER = "Tracker"
    SPIN = "Spin"
    CRUZE = "Cruze"
    GOL = "Gol"
    POLO = "Polo"
    VIRTUS = "Virtus"
    TIGUAN = "Tiguan"
    AMAROK = "Amarok"
    T_CROSS = "T-Cross"
    KA = "Ka"
    RANGER = "Ranger"
    TERRITORY = "Territory"
    BRONCO = "Bronco"
    ARGO = "Argo"
    CRONOS = "Cronos"
    PULSE = "Pulse"
    TORO = "Toro"
    STRADA = "Strada"
    MOBI = "Mobi"
    HB20 = "HB20"
    CRETA = "Creta"
    TUCSON = "Tucson"
    SANTA_FE = "Santa Fe"
    KWID = "Kwid"
    SANDERO = "Sandero"
    DUSTER = "Duster"
    LOGAN = "Logan"
    RENEGADE = "Renegade"
    COMPASS = "Compass"
    COMMANDER = "Commander"
    WRANGLER = "Wrangler"


class Color(StrEnum):
    WHITE = "Branco"
    BLACK = "Preto"
    SILVER = "Prata"
    GRAY = "Cinza"
    RED = "Vermelho"
    BLUE = "Azul"
    DARK_BLUE = "Azul Escuro"
    GREEN = "Verde"
    YELLOW = "Amarelo"
    ORANGE = "Laranja"
    BROWN = "Marrom"
    BEIGE = "Bege"
    GOLD = "Dourado"
    BRONZE = "Bronze"
    PEARL_WHITE = "Branco Perolado"
    CHAMPAGNE = "Champagne"


class Fuel(StrEnum):
    FLEX = "Flex"
    GASOLINE = "Gasolina"
    DIESEL = "Diesel"
    ELECTRIC = "Elétrico"
    HYBRID = "Híbrido"
    NATURAL_GAS = "Gás Natural"


class Transmission(StrEnum):
    MANUAL = "Manual"
    AUTOMATIC = "Automático"
    CVT = "CVT"
    AUTOMATED_MANUAL = "Automatizado"
    DUAL_CLUTCH = "Dupla Embreagem"


class Engine(StrEnum):
    MOTOR_1_0 = "1.0"
    MOTOR_1_3 = "1.3"
    MOTOR_1_4 = "1.4"
    MOTOR_1_5 = "1.5"
    MOTOR_1_6 = "1.6"
    MOTOR_1_8 = "1.8"
    MOTOR_2_0 = "2.0"
    MOTOR_2_5 = "2.5"
    MOTOR_3_0 = "3.0"
    MOTOR_3_5 = "3.5"
    MOTOR_4_0 = "4.0"
    ELECTRIC = "Electric"


class Doors(IntEnum):
    TWO = 2
    FOUR = 4


class Condition(StrEnum):
    NEW = "Novo"
    SEMI_NEW = "Seminovo"
    USED = "Usado"


class Category(StrEnum):
    HATCH = "Hatch"
    SEDAN = "Sedan"
    SUV = "SUV"
    PICKUP = "Pickup"
    MINIVAN = "Minivan"
    COUPE = "Coupe"
    CONVERTIBLE = "Convertible"
    WAGON = "Wagon"
    VAN = "Van"
