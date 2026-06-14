from dataclasses import dataclass
from types import MappingProxyType





@dataclass(frozen=True)
class ClubData:

    club_coords : dict[int, tuple[float, float]] = MappingProxyType({
        1: (54.7598, 9.4071),    # SC Weiche Flensburg 08
        2: (53.8976, 10.1853),   # SV Todesfelde
        3: (53.8812, 10.6690),   # VfB Lübeck
        4: (53.8583, 10.6814),   # 1. FC Phönix Lübeck
        5: (53.7038, 9.3805),    # SV Drochtersen/Assel
        6: (53.5892, 9.9686),    # Eimsbütteler TV
        7: (53.5876, 9.9691),    # Hamburger SV II
        8: (53.3990, 13.0947),   # SV Babelsberg 03
        9: (53.3792, 7.2034),    # Kickers Emden
        10: (53.1295, 8.2064),   # VfB Oldenburg
        11: (53.0911, 8.0572),   # SSV Jeddeloh
        12: (53.0867, 8.7943),   # Bremer SV
        13: (53.0642, 8.8437),   # SV Werder Bremen II
        14: (53.0385, 8.6431),   # SV Atlas Delmenhorst
        15: (52.5400, 13.4772),  # BFC Dynamo
        16: (52.4683, 13.4176),  # SV Tasmania Berlin
        17: (52.4327, 13.3547),  # BFC Preussen
        18: (52.4088, 9.6018),   # TSV Havelse
        19: (52.4026, 9.7694),   # HSC Hannover
        20: (52.3900, 13.1924),  # RSV Eintracht Stahnsdorf
        21: (52.3766, 9.7729),   # Hannover 96 II
        22: (52.3666, 14.0360),  # VSG Altglienicke
        23: (52.2713, 7.9191),   # Sportfreunde Lotte
        24: (52.1251, 11.6708),  # 1. FC Magdeburg II
        25: (52.1032, 13.1483),  # FSV 63 Luckenwalde
        26: (51.8917, 8.3881),   # FC Gütersloh
        27: (51.8572, 6.6098),   # 1. FC Bocholt
        28: (51.7308, 8.7111),   # SC Paderborn II
        29: (51.6371, 7.8684),   # Westfalia Rhynern
        30: (51.5595, 7.0674),   # FC Schalke 04 II
        31: (51.5219, 7.1715),   # VfL Bochum II
        32: (51.4936, 6.8545),   # Rot-Weiß Oberhausen
        33: (51.4928, 7.4542),   # Borussia Dortmund II
        34: (51.4858, 7.1186),   # SG Wattenscheid 09
        35: (51.4654, 11.9622),  # Hallescher FC
        36: (51.3582, 12.3077),  # BSG Chemie Leipzig
        37: (51.3029, 12.4193),  # 1. FC Lokomotive Leipzig
        38: (51.2987, 9.4840),   # KSV Hessen Kassel
        39: (51.1753, 6.4497),   # Borussia Mönchengladbach II
        40: (51.1736, 6.9345),   # VfB 03 Hilden
        41: (50.9937, 7.1200),   # SV Bergisch Gladbach
        42: (50.9601, 11.0373),  # FC Rot-Weiß Erfurt
        43: (50.9159, 11.5829),  # FC Carl Zeiss Jena
        44: (50.9083, 6.9057),   # 1. FC Köln II
        45: (50.8527, 8.0261),   # Sportfreunde Siegen
        46: (50.8421, 12.9456),  # Chemnitzer FC
        47: (50.7411, 8.1912),   # TSV Steinbach Haiger
        48: (50.7402, 7.0846),   # Bonner SC
        49: (50.7285, 12.5194),  # FSV Zwickau
        50: (50.5977, 12.7113),  # FC Erzgebirge Aue
        51: (50.5401, 9.6653),   # SG Barockstadt Fulda-Lehnerz
        52: (50.3296, 10.4324),  # TSV Aubstadt
        53: (50.1281, 8.7232),   # FSV Frankfurt
        54: (50.0513, 10.2030),  # 1. FC Schweinfurt
        55: (50.0063, 8.6819),   # Eintracht Frankfurt II
        56: (50.0009, 8.2457),   # 1. FSV Mainz 05 II
        57: (49.5564, 10.9948),  # SC Eltersdorf
        58: (49.4787, 8.5005),   # VfR Mannheim
        59: (49.4352, 11.1312),  # 1. FC Nürnberg II
        60: (49.4346, 7.7801),   # 1. FC Kaiserslautern II
        61: (49.3322, 8.6484),   # SV Sandhausen
        62: (49.3161, 7.3544),   # FC 08 Homburg
        63: (49.3152, 8.6422),   # FC-Astoria Walldorf
        64: (49.3059, 10.5578),  # SpVgg Ansbach 09
        65: (49.2668, 11.2991),  # SpVgg Greuther Fürth II
        66: (49.1757, 12.6690),  # DJK Vilzing
        67: (48.9401, 9.1981),   # SGV Freiberg
        68: (48.8878, 11.1923),  # VfB Eichstätt
        69: (48.8405, 10.0725),  # VfR Aalen
        70: (48.7540, 9.1883),   # Stuttgarter Kickers
        71: (48.4045, 10.0095),  # SSV Ulm 1846
        72: (48.3431, 10.9088),  # TSV Schwaben Augsburg
        73: (48.3145, 12.2756),  # TSV Buchbach
        74: (48.2180, 10.0923),  # FV Illertissen
        75: (48.1789, 12.8347),  # Wacker Burghausen
        76: (48.1110, 11.5745),  # TSV 1860 München
        77: (48.1110, 11.5745),  # FC Bayern München II
        78: (48.0738, 11.6158),  # SpVgg Unterhaching
        79: (48.0636, 10.8484),  # TSV Landsberg
        80: (47.9889, 7.8929),   # SC Freiburg II
    })

    club_names: dict[int, str] = MappingProxyType({
        1: "SC Weiche Flensburg 08",
        2: "SV Todesfelde",
        3: "VfB Lübeck",
        4: "1. FC Phönix Lübeck",
        5: "SV Drochtersen/Assel",
        6: "Eimsbütteler TV",
        7: "Hamburger SV II",
        8: "SV Babelsberg 03",
        9: "Kickers Emden",
        10: "VfB Oldenburg",
        11: "SSV Jeddeloh",
        12: "Bremer SV",
        13: "SV Werder Bremen II",
        14: "SV Atlas Delmenhorst",
        15: "BFC Dynamo",
        16: "SV Tasmania Berlin",
        17: "BFC Preussen",
        18: "TSV Havelse",
        19: "HSC Hannover",
        20: "RSV Eintracht Stahnsdorf",
        21: "Hannover 96 II",
        22: "VSG Altglienicke",
        23: "Sportfreunde Lotte",
        24: "1. FC Magdeburg II",
        25: "FSV 63 Luckenwalde",
        26: "FC Gütersloh",
        27: "1. FC Bocholt",
        28: "SC Paderborn II",
        29: "Westfalia Rhynern",
        30: "FC Schalke 04 II",
        31: "VfL Bochum II",
        32: "Rot-Weiß Oberhausen",
        33: "Borussia Dortmund II",
        34: "SG Wattenscheid 09",
        35: "Hallescher FC",
        36: "BSG Chemie Leipzig",
        37: "1. FC Lokomotive Leipzig",
        38: "KSV Hessen Kassel",
        39: "Borussia Mönchengladbach II",
        40: "VfB 03 Hilden",
        41: "SV Bergisch Gladbach",
        42: "FC Rot-Weiß Erfurt",
        43: "FC Carl Zeiss Jena",
        44: "1. FC Köln II",
        45: "Sportfreunde Siegen",
        46: "Chemnitzer FC",
        47: "TSV Steinbach Haiger",
        48: "Bonner SC",
        49: "FSV Zwickau",
        50: "FC Erzgebirge Aue",
        51: "SG Barockstadt Fulda-Lehnerz",
        52: "TSV Aubstadt",
        53: "FSV Frankfurt",
        54: "1. FC Schweinfurt",
        55: "Eintracht Frankfurt II",
        56: "1. FSV Mainz 05 II",
        57: "SC Eltersdorf",
        58: "VfR Mannheim",
        59: "1. FC Nürnberg II",
        60: "1. FC Kaiserslautern II",
        61: "SV Sandhausen",
        62: "FC 08 Homburg",
        63: "FC-Astoria Walldorf",
        64: "SpVgg Ansbach 09",
        65: "SpVgg Greuther Fürth II",
        66: "DJK Vilzing",
        67: "SGV Freiberg",
        68: "VfB Eichstätt",
        69: "VfR Aalen",
        70: "Stuttgarter Kickers",
        71: "SSV Ulm 1846",
        72: "TSV Schwaben Augsburg",
        73: "TSV Buchbach",
        74: "FV Illertissen",
        75: "Wacker Burghausen",
        76: "TSV 1860 München",
        77: "FC Bayern München II",
        78: "SpVgg Unterhaching",
        79: "TSV Landsberg",
        80: "SC Freiburg II",
    })
