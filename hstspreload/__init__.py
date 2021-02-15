"""Check if a host is in the Google Chrome HSTS Preload list"""

import functools
import os
import typing

__version__ = "2021.2.15"
__checksum__ = "dd69ac5109275d1f2427600c25063a223f1a197d629ef9d1c4b5950e8625c225"
__all__ = ["in_hsts_preload"]

# fmt: off
_GTLD_INCLUDE_SUBDOMAINS = {b'android', b'app', b'bank', b'chrome', b'dev', b'foo', b'gle', b'gmail', b'google', b'hangout', b'insurance', b'meet', b'new', b'page', b'play', b'search', b'youtube'}  # noqa: E501
_JUMPTABLE = [[(0, 11), (11, 5), (16, 9), (25, 57), (82, 26), (108, 12), None, (120, 19), (139, 22), (161, 7), (168, 20), (188, 18), None, (206, 29), (235, 45), (280, 7), (287, 9), (296, 36), (332, 10), (342, 10), (352, 28), None, (380, 54), (434, 8), (442, 18), (460, 19), (479, 13), (492, 14), (506, 14), None, None, (520, 29), (549, 20), (569, 35), (604, 14), (618, 24), (642, 9), None, (651, 25), (676, 27), (703, 8), (711, 13), None, None, (724, 17), (741, 6), (747, 26), (773, 5), (778, 5), (783, 10), (793, 14), (807, 11), (818, 12), (830, 27), None, (857, 11), (868, 11), (879, 7), (886, 29), (915, 18), (933, 27), (960, 46), (1006, 25), (1031, 16), (1047, 8), (1055, 5), (1060, 22), (1082, 18), None, (1100, 36), (1136, 15), (1151, 8), (1159, 11), None, (1170, 5), (1175, 16), (1191, 14), (1205, 18), None, (1223, 14), (1237, 26), (1263, 48), (1311, 19), (1330, 5), (1335, 46), (1381, 14), (1395, 14), (1409, 20), None, (1429, 10), (1439, 13), (1452, 15), (1467, 19), None, (1486, 13), (1499, 19), (1518, 11), (1529, 4), (1533, 22), (1555, 10), (1565, 7), (1572, 14), (1586, 21), (1607, 11), (1618, 21), (1639, 12), (1651, 32), None, (1683, 10), (1693, 14), (1707, 12), (1719, 45), (1764, 15), None, (1779, 11), (1790, 23), (1813, 21), (1834, 26), (1860, 6), (1866, 6), (1872, 7), (1879, 5), (1884, 20), (1904, 23), (1927, 24), (1951, 13), (1964, 15), (1979, 19), (1998, 6), (2004, 61), (2065, 44), (2109, 12), (2121, 23), (2144, 16), (2160, 38), (2198, 6), (2204, 12), (2216, 44), (2260, 6), (2266, 41), (2307, 13), (2320, 23), (2343, 30), (2373, 16), (2389, 8), (2397, 15), (2412, 12), (2424, 19), (2443, 21), (2464, 15), None, (2479, 35), (2514, 21), (2535, 17), (2552, 19), (2571, 26), (2597, 5), (2602, 37), (2639, 26), (2665, 16), (2681, 10), (2691, 17), (2708, 23), (2731, 14), (2745, 17), (2762, 8), (2770, 4), (2774, 7), (2781, 29), (2810, 6), (2816, 18), (2834, 27), (2861, 20), (2881, 17), (2898, 19), (2917, 12), (2929, 40), (2969, 40), (3009, 12), (3021, 48), (3069, 25), (3094, 12), None, (3106, 8), (3114, 25), (3139, 19), (3158, 6), (3164, 23), None, (3187, 30), (3217, 33), (3250, 14), (3264, 12), (3276, 27), None, (3303, 26), (3329, 41), (3370, 50), (3420, 15), (3435, 20), (3455, 15), (3470, 21), (3491, 32), (3523, 24), (3547, 20), (3567, 17), (3584, 60), (3644, 19), (3663, 9), (3672, 12), (3684, 12), (3696, 11), (3707, 10), (3717, 48), (3765, 32), None, (3797, 25), (3822, 12), None, (3834, 8), (3842, 8), (3850, 7), None, (3857, 25), (3882, 17), None, (3899, 21), (3920, 35), (3955, 12), (3967, 10), (3977, 36), (4013, 20), (4033, 22), (4055, 23), (4078, 19), (4097, 12), (4109, 5), (4114, 30), (4144, 24), (4168, 14), (4182, 14), (4196, 47), (4243, 46), None, None, (4289, 51), (4340, 42), None, (4382, 14), None, (4396, 15), (4411, 8), (4419, 21), (4440, 6), (4446, 16), (4462, 17)], [(4479, 7167), (11646, 7648), (19294, 7836), (27130, 6851), (33981, 7308), (41289, 6885), (48174, 7874), (56048, 6881), (62929, 7676), (70605, 6870), (77475, 8160), (85635, 7137), (92772, 7379), (100151, 8514), (108665, 7364), (116029, 7537), (123566, 7914), (131480, 6650), (138130, 7150), (145280, 7176), (152456, 7638), (160094, 7481), (167575, 7804), (175379, 6843), (182222, 7398), (189620, 7256), (196876, 7775), (204651, 7837), (212488, 7233), (219721, 7368), (227089, 7766), (234855, 7325), (242180, 7347), (249527, 7788), (257315, 7014), (264329, 7483), (271812, 7043), (278855, 7959), (286814, 7617), (294431, 7746), (302177, 8216), (310393, 7177), (317570, 7220), (324790, 7033), (331823, 7184), (339007, 7133), (346140, 7409), (353549, 8246), (361795, 7165), (368960, 6827), (375787, 7116), (382903, 7605), (390508, 7615), (398123, 7757), (405880, 7925), (413805, 7626), (421431, 7708), (429139, 7137), (436276, 7898), (444174, 6549), (450723, 7409), (458132, 7343), (465475, 7277), (472752, 7902), (480654, 7888), (488542, 7688), (496230, 7127), (503357, 8037), (511394, 7711), (519105, 7549), (526654, 7177), (533831, 7235), (541066, 6767), (547833, 7754), (555587, 7820), (563407, 8249), (571656, 6960), (578616, 8101), (586717, 7836), (594553, 6896), (601449, 7719), (609168, 6556), (615724, 7437), (623161, 7567), (630728, 7121), (637849, 7267), (645116, 7699), (652815, 7533), (660348, 7731), (668079, 7686), (675765, 8294), (684059, 6709), (690768, 7174), (697942, 7312), (705254, 7574), (712828, 8088), (720916, 8031), (728947, 7229), (736176, 7245), (743421, 7143), (750564, 7163), (757727, 7546), (765273, 7408), (772681, 7245), (779926, 7044), (786970, 7844), (794814, 7796), (802610, 7838), (810448, 8785), (819233, 7875), (827108, 7683), (834791, 7522), (842313, 7255), (849568, 7428), (856996, 7786), (864782, 7571), (872353, 7131), (879484, 7158), (886642, 7183), (893825, 7966), (901791, 7937), (909728, 7770), (917498, 7788), (925286, 7854), (933140, 8711), (941851, 7288), (949139, 6747), (955886, 7873), (963759, 7463), (971222, 9059), (980281, 8070), (988351, 6972), (995323, 7799), (1003122, 7681), (1010803, 7203), (1018006, 7934), (1025940, 7099), (1033039, 7671), (1040710, 7380), (1048090, 7362), (1055452, 7629), (1063081, 7982), (1071063, 7049), (1078112, 7335), (1085447, 7563), (1093010, 7282), (1100292, 7273), (1107565, 7492), (1115057, 7111), (1122168, 8003), (1130171, 7537), (1137708, 7718), (1145426, 7770), (1153196, 7278), (1160474, 7612), (1168086, 7480), (1175566, 7391), (1182957, 7511), (1190468, 7175), (1197643, 6823), (1204466, 6980), (1211446, 7786), (1219232, 8199), (1227431, 7028), (1234459, 7284), (1241743, 7875), (1249618, 7371), (1256989, 7080), (1264069, 7840), (1271909, 7450), (1279359, 6630), (1285989, 7525), (1293514, 8751), (1302265, 6908), (1309173, 7155), (1316328, 7664), (1323992, 7419), (1331411, 7423), (1338834, 7288), (1346122, 6978), (1353100, 8433), (1361533, 7664), (1369197, 7373), (1376570, 7903), (1384473, 8473), (1392946, 8146), (1401092, 6962), (1408054, 7892), (1415946, 7246), (1423192, 7544), (1430736, 8109), (1438845, 7107), (1445952, 7757), (1453709, 7892), (1461601, 7410), (1469011, 7399), (1476410, 7252), (1483662, 7488), (1491150, 7453), (1498603, 7172), (1505775, 7791), (1513566, 6918), (1520484, 7941), (1528425, 7680), (1536105, 8025), (1544130, 7722), (1551852, 6514), (1558366, 7567), (1565933, 7323), (1573256, 7662), (1580918, 7739), (1588657, 7815), (1596472, 7447), (1603919, 7950), (1611869, 7669), (1619538, 7384), (1626922, 7452), (1634374, 7318), (1641692, 7546), (1649238, 7493), (1656731, 7568), (1664299, 6833), (1671132, 8432), (1679564, 7518), (1687082, 7148), (1694230, 7409), (1701639, 7459), (1709098, 6879), (1715977, 7603), (1723580, 7465), (1731045, 8212), (1739257, 7584), (1746841, 7171), (1754012, 7671), (1761683, 7398), (1769081, 8191), (1777272, 7145), (1784417, 7087), (1791504, 6369), (1797873, 7969), (1805842, 7413), (1813255, 7788), (1821043, 7203), (1828246, 7451), (1835697, 7347), (1843044, 7898), (1850942, 7273), (1858215, 6691), (1864906, 7416), (1872322, 6956), (1879278, 7663), (1886941, 7806), (1894747, 7927), (1902674, 7063), (1909737, 7237), (1916974, 7410)], [(1924384, 898), (1925282, 715), (1925997, 715), (1926712, 896), (1927608, 638), (1928246, 715), (1928961, 671), (1929632, 910), (1930542, 721), (1931263, 717), (1931980, 580), (1932560, 660), (1933220, 792), (1934012, 885), (1934897, 1022), (1935919, 877), (1936796, 1304), (1938100, 704), (1938804, 939), (1939743, 819), (1940562, 766), (1941328, 828), (1942156, 946), (1943102, 718), (1943820, 766), (1944586, 715), (1945301, 1050), (1946351, 1266), (1947617, 797), (1948414, 850), (1949264, 1037), (1950301, 862), (1951163, 693), (1951856, 756), (1952612, 830), (1953442, 867), (1954309, 782), (1955091, 820), (1955911, 757), (1956668, 1110), (1957778, 695), (1958473, 848), (1959321, 831), (1960152, 753), (1960905, 780), (1961685, 502), (1962187, 1042), (1963229, 1010), (1964239, 823), (1965062, 574), (1965636, 869), (1966505, 706), (1967211, 762), (1967973, 1065), (1969038, 1016), (1970054, 572), (1970626, 702), (1971328, 665), (1971993, 666), (1972659, 888), (1973547, 833), (1974380, 832), (1975212, 1107), (1976319, 995), (1977314, 819), (1978133, 772), (1978905, 788), (1979693, 472), (1980165, 679), (1980844, 620), (1981464, 775), (1982239, 955), (1983194, 652), (1983846, 791), (1984637, 631), (1985268, 745), (1986013, 688), (1986701, 725), (1987426, 828), (1988254, 526), (1988780, 863), (1989643, 687), (1990330, 915), (1991245, 700), (1991945, 689), (1992634, 467), (1993101, 669), (1993770, 801), (1994571, 885), (1995456, 802), (1996258, 948), (1997206, 1183), (1998389, 903), (1999292, 941), (2000233, 786), (2001019, 476), (2001495, 996), (2002491, 871), (2003362, 606), (2003968, 721), (2004689, 770), (2005459, 922), (2006381, 966), (2007347, 571), (2007918, 652), (2008570, 844), (2009414, 507), (2009921, 541), (2010462, 1028), (2011490, 1029), (2012519, 802), (2013321, 812), (2014133, 803), (2014936, 804), (2015740, 751), (2016491, 732), (2017223, 696), (2017919, 578), (2018497, 770), (2019267, 707), (2019974, 1026), (2021000, 756), (2021756, 847), (2022603, 502), (2023105, 691), (2023796, 828), (2024624, 880), (2025504, 998), (2026502, 782), (2027284, 990), (2028274, 843), (2029117, 616), (2029733, 897), (2030630, 733), (2031363, 879), (2032242, 795), (2033037, 736), (2033773, 725), (2034498, 701), (2035199, 644), (2035843, 706), (2036549, 718), (2037267, 804), (2038071, 614), (2038685, 534), (2039219, 603), (2039822, 696), (2040518, 666), (2041184, 785), (2041969, 688), (2042657, 808), (2043465, 602), (2044067, 593), (2044660, 772), (2045432, 742), (2046174, 692), (2046866, 784), (2047650, 988), (2048638, 761), (2049399, 576), (2049975, 1044), (2051019, 927), (2051946, 648), (2052594, 750), (2053344, 889), (2054233, 736), (2054969, 707), (2055676, 600), (2056276, 711), (2056987, 749), (2057736, 830), (2058566, 691), (2059257, 932), (2060189, 819), (2061008, 891), (2061899, 814), (2062713, 707), (2063420, 630), (2064050, 773), (2064823, 762), (2065585, 1492), (2067077, 577), (2067654, 741), (2068395, 740), (2069135, 1012), (2070147, 849), (2070996, 848), (2071844, 639), (2072483, 662), (2073145, 930), (2074075, 623), (2074698, 603), (2075301, 873), (2076174, 784), (2076958, 943), (2077901, 849), (2078750, 779), (2079529, 764), (2080293, 896), (2081189, 690), (2081879, 977), (2082856, 680), (2083536, 863), (2084399, 618), (2085017, 806), (2085823, 610), (2086433, 863), (2087296, 843), (2088139, 724), (2088863, 963), (2089826, 761), (2090587, 890), (2091477, 981), (2092458, 1115), (2093573, 922), (2094495, 726), (2095221, 1020), (2096241, 794), (2097035, 589), (2097624, 476), (2098100, 878), (2098978, 794), (2099772, 525), (2100297, 1083), (2101380, 597), (2101977, 798), (2102775, 924), (2103699, 878), (2104577, 927), (2105504, 733), (2106237, 874), (2107111, 783), (2107894, 879), (2108773, 619), (2109392, 665), (2110057, 519), (2110576, 722), (2111298, 469), (2111767, 851), (2112618, 931), (2113549, 881), (2114430, 718), (2115148, 675), (2115823, 604), (2116427, 982), (2117409, 523), (2117932, 656), (2118588, 860), (2119448, 535), (2119983, 946), (2120929, 2131), (2123060, 697), (2123757, 726), (2124483, 957), (2125440, 1072), (2126512, 518)], [(2127030, 48), None, (2127078, 35), (2127113, 42), None, None, None, None, None, None, None, None, None, None, None, None, None, (2127155, 42), None, (2127197, 25), (2127222, 44), (2127266, 22), (2127288, 18), None, None, None, None, (2127306, 26), None, None, None, None, (2127332, 21), (2127353, 25), None, None, (2127378, 26), None, None, None, None, (2127404, 44), (2127448, 21), (2127469, 23), None, None, None, None, (2127492, 48), None, None, None, None, None, (2127540, 31), None, None, None, None, (2127571, 42), None, (2127613, 22), None, (2127635, 21), None, (2127656, 26), (2127682, 42), None, None, (2127724, 77), None, None, None, None, None, (2127801, 21), (2127822, 21), None, None, (2127843, 34), (2127877, 42), None, None, None, (2127919, 25), None, None, (2127944, 21), None, None, None, None, None, (2127965, 24), (2127989, 21), None, None, (2128010, 26), None, (2128036, 18), None, (2128054, 54), None, None, None, None, None, None, (2128108, 26), None, (2128134, 19), None, (2128153, 20), None, None, (2128173, 42), (2128215, 42), (2128257, 17), (2128274, 17), (2128291, 26), None, (2128317, 26), None, None, None, (2128343, 26), (2128369, 20), (2128389, 26), None, (2128415, 42), (2128457, 63), None, None, None, (2128520, 40), (2128560, 48), None, None, None, (2128608, 47), None, None, None, None, None, None, None, (2128655, 42), None, (2128697, 55), None, (2128752, 9), None, (2128761, 21), (2128782, 42), None, None, (2128824, 65), (2128889, 82), None, None, (2128971, 42), None, None, None, (2129013, 21), None, None, None, None, None, (2129034, 42), (2129076, 21), (2129097, 21), None, (2129118, 42), (2129160, 25), None, (2129185, 16), (2129201, 21), (2129222, 56), None, None, (2129278, 21), (2129299, 19), (2129318, 26), None, (2129344, 16), None, (2129360, 21), None, None, (2129381, 38), None, (2129419, 22), (2129441, 21), (2129462, 21), None, None, (2129483, 63), None, (2129546, 21), (2129567, 42), None, (2129609, 17), None, None, None, None, (2129626, 21), (2129647, 21), None, None, (2129668, 21), None, None, (2129689, 21), None, (2129710, 26), None, (2129736, 50), None, None, None, (2129786, 50), (2129836, 26), (2129862, 21), (2129883, 21), (2129904, 19), None, (2129923, 35), (2129958, 26), (2129984, 23), (2130007, 39), (2130046, 42), None, None, None, None, None, None, (2130088, 21), None, None, None, (2130109, 21), None, None, (2130130, 90), None, (2130220, 239), (2130459, 38), None, None, None, None]]  # noqa: E501
_CRC8_TABLE = [
    0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15,
    0x38, 0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d,
    0x70, 0x77, 0x7e, 0x79, 0x6c, 0x6b, 0x62, 0x65,
    0x48, 0x4f, 0x46, 0x41, 0x54, 0x53, 0x5a, 0x5d,
    0xe0, 0xe7, 0xee, 0xe9, 0xfc, 0xfb, 0xf2, 0xf5,
    0xd8, 0xdf, 0xd6, 0xd1, 0xc4, 0xc3, 0xca, 0xcd,
    0x90, 0x97, 0x9e, 0x99, 0x8c, 0x8b, 0x82, 0x85,
    0xa8, 0xaf, 0xa6, 0xa1, 0xb4, 0xb3, 0xba, 0xbd,
    0xc7, 0xc0, 0xc9, 0xce, 0xdb, 0xdc, 0xd5, 0xd2,
    0xff, 0xf8, 0xf1, 0xf6, 0xe3, 0xe4, 0xed, 0xea,
    0xb7, 0xb0, 0xb9, 0xbe, 0xab, 0xac, 0xa5, 0xa2,
    0x8f, 0x88, 0x81, 0x86, 0x93, 0x94, 0x9d, 0x9a,
    0x27, 0x20, 0x29, 0x2e, 0x3b, 0x3c, 0x35, 0x32,
    0x1f, 0x18, 0x11, 0x16, 0x03, 0x04, 0x0d, 0x0a,
    0x57, 0x50, 0x59, 0x5e, 0x4b, 0x4c, 0x45, 0x42,
    0x6f, 0x68, 0x61, 0x66, 0x73, 0x74, 0x7d, 0x7a,
    0x89, 0x8e, 0x87, 0x80, 0x95, 0x92, 0x9b, 0x9c,
    0xb1, 0xb6, 0xbf, 0xb8, 0xad, 0xaa, 0xa3, 0xa4,
    0xf9, 0xfe, 0xf7, 0xf0, 0xe5, 0xe2, 0xeb, 0xec,
    0xc1, 0xc6, 0xcf, 0xc8, 0xdd, 0xda, 0xd3, 0xd4,
    0x69, 0x6e, 0x67, 0x60, 0x75, 0x72, 0x7b, 0x7c,
    0x51, 0x56, 0x5f, 0x58, 0x4d, 0x4a, 0x43, 0x44,
    0x19, 0x1e, 0x17, 0x10, 0x05, 0x02, 0x0b, 0x0c,
    0x21, 0x26, 0x2f, 0x28, 0x3d, 0x3a, 0x33, 0x34,
    0x4e, 0x49, 0x40, 0x47, 0x52, 0x55, 0x5c, 0x5b,
    0x76, 0x71, 0x78, 0x7f, 0x6a, 0x6d, 0x64, 0x63,
    0x3e, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2c, 0x2b,
    0x06, 0x01, 0x08, 0x0f, 0x1a, 0x1d, 0x14, 0x13,
    0xae, 0xa9, 0xa0, 0xa7, 0xb2, 0xb5, 0xbc, 0xbb,
    0x96, 0x91, 0x98, 0x9f, 0x8a, 0x8d, 0x84, 0x83,
    0xde, 0xd9, 0xd0, 0xd7, 0xc2, 0xc5, 0xcc, 0xcb,
    0xe6, 0xe1, 0xe8, 0xef, 0xfa, 0xfd, 0xf4, 0xf3
]
# fmt: on

_IS_LEAF = 0x80
_INCLUDE_SUBDOMAINS = 0x40


try:
    from importlib.resources import open_binary

    def open_pkg_binary(path: str) -> typing.BinaryIO:
        return open_binary("hstspreload", path)


except ImportError:

    def open_pkg_binary(path: str) -> typing.BinaryIO:
        return open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), path),
            "rb",
        )


@functools.lru_cache(maxsize=1024)
def in_hsts_preload(host: typing.AnyStr) -> bool:
    """Determines if an IDNA-encoded host is on the HSTS preload list"""

    if isinstance(host, str):
        host = host.encode("ascii")
    labels = host.lower().split(b".")

    # Fast-branch for gTLDs that are registered to preload all sub-domains.
    if labels[-1] in _GTLD_INCLUDE_SUBDOMAINS:
        return True

    with open_pkg_binary("hstspreload.bin") as f:
        for layer, label in enumerate(labels[::-1]):
            # None of our layers are greater than 4 deep.
            if layer > 3:
                return False

            # Read the jump table for the layer and label
            jump_info = _JUMPTABLE[layer][_crc8(label)]
            if jump_info is None:
                # No entry: host is not preloaded
                return False

            # Read the set of entries for that layer and label
            f.seek(jump_info[0])
            data = bytearray(jump_info[1])
            f.readinto(data)

            for is_leaf, include_subdomains, ent_label in _iter_entries(data):
                # We found a potential leaf
                if is_leaf:
                    if ent_label == host:
                        return True
                    if include_subdomains and host.endswith(b"." + ent_label):
                        return True

                # Continue traversing as we're not at a leaf.
                elif label == ent_label:
                    break
            else:
                return False
    return False


def _iter_entries(data: bytes) -> typing.Iterable[typing.Tuple[int, int, bytes]]:
    while data:
        flags = data[0]
        size = data[1]
        label = bytes(data[2 : 2 + size])
        yield (flags & _IS_LEAF, flags & _INCLUDE_SUBDOMAINS, label)
        data = data[2 + size :]


def _crc8(value: bytes) -> int:
    # CRC8 reference implementation: https://github.com/niccokunzmann/crc8
    checksum = 0x00
    for byte in value:
        checksum = _CRC8_TABLE[checksum ^ byte]
    return checksum
