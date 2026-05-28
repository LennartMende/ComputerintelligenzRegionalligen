clubs: dict[int, tuple[float, float]] = {
    1: (54.7598, 9.4071),    # SC Weiche Flensburg 08
    2: (53.8976, 10.1853),   # SV Todesfelde
    3: (53.8812, 10.6690),   # VfB Lübeck
    4: (53.8583, 10.6814),   # 1. FC Phönix Lübeck
    5: (53.7038, 9.3805),    # SV Drochtersen/Assel
    6: (53.5892, 9.9686),    # Eimsbütteler TV
    7: (53.5876, 9.9691),    # Hamburger SV II
    8: (53.3990, 13.0947),   # SV Babelsberg 03
    9: (53.3792, 7.2034),    # Kickers Emden
    10: (53.1880, 8.5836),   # Blumenthaler SV
    11: (53.1295, 8.2064),   # VfB Oldenburg
    12: (53.0911, 8.0572),   # SSV Jeddeloh
    13: (53.0867, 8.7943),   # Bremer SV
    14: (53.0642, 8.8437),   # SV Werder Bremen II
    15: (53.0385, 8.6431),   # SV Atlas Delmenhorst
    16: (52.5400, 13.4772),  # BFC Dynamo
    17: (52.5172, 13.2367),  # Hertha BSC II
    18: (52.4683, 13.4176),  # SV Tasmania Berlin
    19: (52.4327, 13.3547),  # BFC Preussen
    20: (52.4088, 9.6018),   # TSV Havelse
    21: (52.4026, 9.7694),   # HSC Hannover
    22: (52.3900, 13.1924),  # RSV Eintracht Stahnsdorf
    23: (52.3766, 9.7729),   # Hannover 96 II
    24: (52.3666, 14.0360),  # VSG Altglienicke
    25: (52.2860, 9.5122),   # 1. FC Germania Egestorf/Langreder
    26: (52.2713, 7.9191),   # Sportfreunde Lotte
    27: (52.1251, 11.6708),  # 1. FC Magdeburg II
    28: (52.1032, 13.1483),  # FSV 63 Luckenwalde
    29: (51.8917, 8.3881),   # FC Gütersloh
    30: (51.8572, 6.6098),   # 1. FC Bocholt
    31: (51.7308, 8.7111),   # SC Paderborn II
    32: (51.6371, 7.8684),   # Westfalia Rhynern
    33: (51.5595, 7.0674),   # FC Schalke 04 II
    34: (51.5219, 7.1715),   # VfL Bochum II
    35: (51.4936, 6.8545),   # Rot-Weiß Oberhausen
    36: (51.4928, 7.4542),   # Borussia Dortmund II
    37: (51.4858, 7.1186),   # SG Wattenscheid 09
    38: (51.4654, 11.9622),  # Hallescher FC
    39: (51.3582, 12.3077),  # BSG Chemie Leipzig
    40: (51.3029, 12.4193),  # 1. FC Lokomotive Leipzig
    41: (51.2987, 9.4840),   # KSV Hessen Kassel
    42: (51.1753, 6.4497),   # Borussia Mönchengladbach II
    43: (51.1736, 6.9345),   # VfB 03 Hilden
    44: (50.9937, 7.1200),   # SV Bergisch Gladbach
    45: (50.9601, 11.0373),  # FC Rot-Weiß Erfurt
    46: (50.9159, 11.5829),  # FC Carl Zeiss Jena
    47: (50.9083, 6.9057),   # 1. FC Köln II
    48: (50.8527, 8.0261),   # Sportfreunde Siegen
    49: (50.8421, 12.9456),  # Chemnitzer FC
    50: (50.7411, 8.1912),   # TSV Steinbach Haiger
    51: (50.7402, 7.0846),   # Bonner SC
    52: (50.7285, 12.5194),  # FSV Zwickau
    53: (50.5977, 12.7113),  # FC Erzgebirge Aue
    54: (50.5401, 9.6653),   # SG Barockstadt Fulda-Lehnerz
    55: (50.3296, 10.4324),  # TSV Aubstadt
    56: (50.1281, 8.7232),   # FSV Frankfurt
    57: (50.0513, 10.2030),  # 1. FC Schweinfurt
    58: (50.0063, 8.6819),   # Eintracht Frankfurt II
    59: (50.0009, 8.2457),   # 1. FSV Mainz 05 II
    60: (49.7675, 9.9322),   # Würzburger Kickers
    61: (49.5564, 10.9948),  # SC Eltersdorf
    62: (49.4787, 8.5005),   # VfR Mannheim
    63: (49.4352, 11.1312),  # 1. FC Nürnberg II
    64: (49.4346, 7.7801),   # 1. FC Kaiserslautern II
    65: (49.3322, 8.6484),   # SV Sandhausen
    66: (49.3161, 7.3544),   # FC 08 Homburg
    67: (49.3152, 8.6422),   # FC-Astoria Walldorf
    68: (49.3059, 10.5578),  # SpVgg Ansbach 09
    69: (49.2668, 11.2991),  # SpVgg Greuther Fürth II
    70: (49.1757, 12.6690),  # DJK Vilzing
    71: (48.9401, 9.1981),   # SGV Freiberg
    72: (48.8878, 11.1923),  # VfB Eichstätt
    73: (48.8405, 10.0725),  # VfR Aalen
    74: (48.7540, 9.1883),   # Stuttgarter Kickers
    75: (48.4045, 10.0095),  # SSV Ulm 1846
    76: (48.3431, 10.9088),  # TSV Schwaben Augsburg
    77: (48.3145, 12.2756),  # TSV Buchbach
    78: (48.2180, 10.0923),  # FV Illertissen
    79: (48.1789, 12.8347),  # Wacker Burghausen
    80: (48.1110, 11.5745),  # FC Bayern München II
    81: (48.0738, 11.6158),  # SpVgg Unterhaching
    82: (48.0636, 10.8484),  # TSV Landsberg
    83: (47.9889, 7.8929),   # SC Freiburg II
    84: (47.9792, 10.1651),  # FC Memmingen
}