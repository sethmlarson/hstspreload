"""Check if a host is in the Google Chrome HSTS Preload list"""

import functools
import os
import typing

__version__ = "2021.5.24"
__checksum__ = "d5f620d912760cae26d544785cf2cd3e8cf4801ba1af695c09ac3a070e669441"
__all__ = ["in_hsts_preload"]

# fmt: off
_GTLD_INCLUDE_SUBDOMAINS = {b'android', b'app', b'bank', b'chrome', b'dev', b'foo', b'gle', b'gmail', b'google', b'hangout', b'insurance', b'meet', b'new', b'page', b'play', b'search', b'youtube'}  # noqa: E501
_JUMPTABLE = [[(0, 11), (11, 5), (16, 9), (25, 61), (86, 26), (112, 12), None, (124, 19), (143, 22), (165, 7), (172, 20), (192, 18), None, (210, 29), (239, 45), (284, 7), (291, 9), (300, 36), (336, 10), (346, 10), (356, 28), None, (384, 54), (438, 8), (446, 18), (464, 19), (483, 13), (496, 14), (510, 14), None, None, (524, 29), (553, 20), (573, 35), (608, 14), (622, 24), (646, 9), None, (655, 25), (680, 27), (707, 8), (715, 13), None, None, (728, 17), (745, 6), (751, 26), (777, 5), (782, 5), (787, 10), (797, 14), (811, 11), (822, 12), (834, 27), None, (861, 11), (872, 11), (883, 7), (890, 29), (919, 18), (937, 27), (964, 46), (1010, 25), (1035, 16), (1051, 8), (1059, 5), (1064, 22), (1086, 18), None, (1104, 36), (1140, 15), (1155, 8), (1163, 11), None, (1174, 5), (1179, 16), (1195, 14), (1209, 18), None, (1227, 14), (1241, 26), (1267, 48), (1315, 19), (1334, 5), (1339, 59), (1398, 14), (1412, 14), (1426, 20), None, (1446, 10), (1456, 13), (1469, 15), (1484, 19), None, (1503, 13), (1516, 19), (1535, 11), (1546, 4), (1550, 22), (1572, 10), (1582, 7), (1589, 14), (1603, 21), (1624, 11), (1635, 21), (1656, 12), (1668, 32), None, (1700, 10), (1710, 14), (1724, 12), (1736, 45), (1781, 15), None, (1796, 11), (1807, 23), (1830, 21), (1851, 26), (1877, 6), (1883, 6), (1889, 7), (1896, 5), (1901, 20), (1921, 23), (1944, 24), (1968, 13), (1981, 15), (1996, 19), (2015, 6), (2021, 61), (2082, 44), (2126, 12), (2138, 23), (2161, 16), (2177, 38), (2215, 6), (2221, 12), (2233, 44), (2277, 6), (2283, 41), (2324, 13), (2337, 23), (2360, 30), (2390, 16), (2406, 8), (2414, 15), (2429, 12), (2441, 19), (2460, 21), (2481, 15), None, (2496, 35), (2531, 21), (2552, 17), (2569, 19), (2588, 26), (2614, 5), (2619, 37), (2656, 26), (2682, 16), (2698, 10), (2708, 17), (2725, 23), (2748, 14), (2762, 17), (2779, 8), (2787, 8), (2795, 7), (2802, 29), (2831, 6), (2837, 18), (2855, 27), (2882, 20), (2902, 17), (2919, 19), (2938, 12), (2950, 40), (2990, 40), (3030, 12), (3042, 48), (3090, 25), (3115, 12), None, (3127, 8), (3135, 25), (3160, 19), (3179, 6), (3185, 23), None, (3208, 30), (3238, 33), (3271, 14), (3285, 12), (3297, 27), None, (3324, 26), (3350, 41), (3391, 50), (3441, 15), (3456, 20), (3476, 15), (3491, 21), (3512, 32), (3544, 24), (3568, 20), (3588, 17), (3605, 60), (3665, 19), (3684, 9), (3693, 12), (3705, 12), (3717, 11), (3728, 10), (3738, 48), (3786, 32), None, (3818, 25), (3843, 23), None, (3866, 8), (3874, 8), (3882, 7), None, (3889, 25), (3914, 17), None, (3931, 21), (3952, 35), (3987, 21), (4008, 10), (4018, 36), (4054, 20), (4074, 22), (4096, 23), (4119, 19), (4138, 12), (4150, 5), (4155, 30), (4185, 24), (4209, 14), (4223, 14), (4237, 47), (4284, 52), None, None, (4336, 51), (4387, 42), None, (4429, 14), None, (4443, 15), (4458, 8), (4466, 21), (4487, 6), (4493, 16), (4509, 17)], [(4526, 7968), (12494, 8354), (20848, 8720), (29568, 7548), (37116, 7893), (45009, 7827), (52836, 8628), (61464, 7590), (69054, 8533), (77587, 7780), (85367, 9201), (94568, 7703), (102271, 8345), (110616, 9588), (120204, 8071), (128275, 8344), (136619, 8715), (145334, 7790), (153124, 8074), (161198, 7680), (168878, 8532), (177410, 8213), (185623, 8560), (194183, 7853), (202036, 8357), (210393, 8064), (218457, 8506), (226963, 8775), (235738, 7831), (243569, 8194), (251763, 8495), (260258, 7992), (268250, 8206), (276456, 8556), (285012, 7592), (292604, 8218), (300822, 8127), (308949, 8802), (317751, 8457), (326208, 8563), (334771, 9022), (343793, 7816), (351609, 7899), (359508, 7855), (367363, 7947), (375310, 8075), (383385, 8156), (391541, 8921), (400462, 8025), (408487, 7627), (416114, 8102), (424216, 8458), (432674, 8601), (441275, 8478), (449753, 8667), (458420, 8202), (466622, 8555), (475177, 8208), (483385, 8607), (491992, 7186), (499178, 8163), (507341, 8307), (515648, 8181), (523829, 8626), (532455, 8408), (540863, 8562), (549425, 7977), (557402, 8872), (566274, 8680), (574954, 8374), (583328, 8061), (591389, 7886), (599275, 7427), (606702, 8562), (615264, 8424), (623688, 8887), (632575, 7688), (640263, 8767), (649030, 8632), (657662, 7770), (665432, 8657), (674089, 7045), (681134, 8123), (689257, 8547), (697804, 7916), (705720, 8270), (713990, 8687), (722677, 8257), (730934, 8486), (739420, 8413), (747833, 9234), (757067, 7595), (764662, 8040), (772702, 8128), (780830, 8259), (789089, 8880), (797969, 8641), (806610, 7849), (814459, 7991), (822450, 7806), (830256, 7895), (838151, 8272), (846423, 8021), (854444, 8017), (862461, 7764), (870225, 8765), (878990, 8688), (887678, 8693), (896371, 9422), (905793, 8631), (914424, 8363), (922787, 8513), (931300, 8081), (939381, 8086), (947467, 8468), (955935, 8581), (964516, 8166), (972682, 7869), (980551, 7967), (988518, 8949), (997467, 8712), (1006179, 8707), (1014886, 8327), (1023213, 8617), (1031830, 9380), (1041210, 8006), (1049216, 7487), (1056703, 8833), (1065536, 8187), (1073723, 9957), (1083680, 8766), (1092446, 7840), (1100286, 8491), (1108777, 8316), (1117093, 8003), (1125096, 8452), (1133548, 7937), (1141485, 8697), (1150182, 8036), (1158218, 8222), (1166440, 8351), (1174791, 8540), (1183331, 7602), (1190933, 7972), (1198905, 8293), (1207198, 7994), (1215192, 8088), (1223280, 8208), (1231488, 7901), (1239389, 8686), (1248075, 8466), (1256541, 8444), (1264985, 8646), (1273631, 8053), (1281684, 8238), (1289922, 8372), (1298294, 8147), (1306441, 8249), (1314690, 7870), (1322560, 7345), (1329905, 7614), (1337519, 8499), (1346018, 8885), (1354903, 8025), (1362928, 8065), (1370993, 8944), (1379937, 8045), (1387982, 7688), (1395670, 8719), (1404389, 8273), (1412662, 7269), (1419931, 8225), (1428156, 9601), (1437757, 7639), (1445396, 7806), (1453202, 8594), (1461796, 8185), (1469981, 8585), (1478566, 8029), (1486595, 7703), (1494298, 9167), (1503465, 8595), (1512060, 7919), (1519979, 8574), (1528553, 9177), (1537730, 9045), (1546775, 7671), (1554446, 8513), (1562959, 7871), (1570830, 8244), (1579074, 8920), (1587994, 7961), (1595955, 8505), (1604460, 8409), (1612869, 8202), (1621071, 8197), (1629268, 7960), (1637228, 8140), (1645368, 8282), (1653650, 7961), (1661611, 8501), (1670112, 7825), (1677937, 8703), (1686640, 8302), (1694942, 8854), (1703796, 8727), (1712523, 7445), (1719968, 8695), (1728663, 8059), (1736722, 8423), (1745145, 8520), (1753665, 8630), (1762295, 8227), (1770522, 8575), (1779097, 8441), (1787538, 8097), (1795635, 8326), (1803961, 8066), (1812027, 8323), (1820350, 8572), (1828922, 8361), (1837283, 7610), (1844893, 9292), (1854185, 8122), (1862307, 8123), (1870430, 8206), (1878636, 8178), (1886814, 7629), (1894443, 8531), (1902974, 8367), (1911341, 8879), (1920220, 8310), (1928530, 7909), (1936439, 8831), (1945270, 8157), (1953427, 9133), (1962560, 7869), (1970429, 7976), (1978405, 7395), (1985800, 8614), (1994414, 8569), (2002983, 8886), (2011869, 8065), (2019934, 8415), (2028349, 8050), (2036399, 8748), (2045147, 7955), (2053102, 7641), (2060743, 8159), (2068902, 7755), (2076657, 8416), (2085073, 8763), (2093836, 8676), (2102512, 7886), (2110398, 8188), (2118586, 8367)], [(2126953, 933), (2127886, 715), (2128601, 754), (2129355, 960), (2130315, 638), (2130953, 838), (2131791, 671), (2132462, 1000), (2133462, 704), (2134166, 758), (2134924, 641), (2135565, 677), (2136242, 827), (2137069, 885), (2137954, 1067), (2139021, 973), (2139994, 1363), (2141357, 736), (2142093, 1008), (2143101, 855), (2143956, 779), (2144735, 879), (2145614, 984), (2146598, 765), (2147363, 795), (2148158, 733), (2148891, 1077), (2149968, 1312), (2151280, 819), (2152099, 853), (2152952, 1063), (2154015, 892), (2154907, 697), (2155604, 842), (2156446, 963), (2157409, 934), (2158343, 847), (2159190, 874), (2160064, 806), (2160870, 1144), (2162014, 726), (2162740, 907), (2163647, 783), (2164430, 784), (2165214, 803), (2166017, 561), (2166578, 1086), (2167664, 1027), (2168691, 889), (2169580, 619), (2170199, 897), (2171096, 734), (2171830, 798), (2172628, 1078), (2173706, 1094), (2174800, 572), (2175372, 767), (2176139, 697), (2176836, 728), (2177564, 892), (2178456, 905), (2179361, 859), (2180220, 1118), (2181338, 1078), (2182416, 835), (2183251, 788), (2184039, 787), (2184826, 511), (2185337, 696), (2186033, 625), (2186658, 826), (2187484, 1001), (2188485, 689), (2189174, 880), (2190054, 700), (2190754, 797), (2191551, 705), (2192256, 738), (2192994, 843), (2193837, 571), (2194408, 892), (2195300, 724), (2196024, 977), (2197001, 714), (2197715, 769), (2198484, 548), (2199032, 761), (2199793, 859), (2200652, 943), (2201595, 875), (2202470, 1092), (2203562, 1243), (2204805, 919), (2205724, 925), (2206649, 842), (2207491, 514), (2208005, 996), (2209001, 887), (2209888, 675), (2210563, 721), (2211284, 825), (2212109, 1008), (2213117, 966), (2214083, 634), (2214717, 652), (2215369, 913), (2216282, 533), (2216815, 589), (2217404, 1018), (2218422, 1032), (2219454, 821), (2220275, 852), (2221127, 803), (2221930, 801), (2222731, 818), (2223549, 823), (2224372, 731), (2225103, 597), (2225700, 801), (2226501, 728), (2227229, 1112), (2228341, 757), (2229098, 889), (2229987, 532), (2230519, 760), (2231279, 882), (2232161, 895), (2233056, 1048), (2234104, 767), (2234871, 1032), (2235903, 896), (2236799, 630), (2237429, 939), (2238368, 787), (2239155, 962), (2240117, 795), (2240912, 753), (2241665, 711), (2242376, 840), (2243216, 692), (2243908, 760), (2244668, 744), (2245412, 824), (2246236, 651), (2246887, 577), (2247464, 637), (2248101, 750), (2248851, 668), (2249519, 804), (2250323, 694), (2251017, 815), (2251832, 604), (2252436, 638), (2253074, 870), (2253944, 764), (2254708, 713), (2255421, 784), (2256205, 1058), (2257263, 805), (2258068, 664), (2258732, 1069), (2259801, 922), (2260723, 720), (2261443, 826), (2262269, 993), (2263262, 736), (2263998, 745), (2264743, 706), (2265449, 756), (2266205, 799), (2267004, 882), (2267886, 677), (2268563, 993), (2269556, 832), (2270388, 920), (2271308, 892), (2272200, 759), (2272959, 630), (2273589, 792), (2274381, 854), (2275235, 1576), (2276811, 610), (2277421, 823), (2278244, 750), (2278994, 1052), (2280046, 913), (2280959, 846), (2281805, 666), (2282471, 674), (2283145, 923), (2284068, 638), (2284706, 589), (2285295, 887), (2286182, 800), (2286982, 948), (2287930, 854), (2288784, 810), (2289594, 763), (2290357, 908), (2291265, 750), (2292015, 948), (2292963, 737), (2293700, 879), (2294579, 671), (2295250, 846), (2296096, 662), (2296758, 981), (2297739, 954), (2298693, 772), (2299465, 1036), (2300501, 780), (2301281, 919), (2302200, 999), (2303199, 1146), (2304345, 957), (2305302, 814), (2306116, 1006), (2307122, 810), (2307932, 589), (2308521, 490), (2309011, 908), (2309919, 827), (2310746, 589), (2311335, 1102), (2312437, 594), (2313031, 824), (2313855, 987), (2314842, 972), (2315814, 925), (2316739, 746), (2317485, 962), (2318447, 797), (2319244, 949), (2320193, 657), (2320850, 700), (2321550, 600), (2322150, 698), (2322848, 486), (2323334, 900), (2324234, 1038), (2325272, 899), (2326171, 751), (2326922, 688), (2327610, 696), (2328306, 1046), (2329352, 616), (2329968, 625), (2330593, 982), (2331575, 519), (2332094, 976), (2333070, 2180), (2335250, 727), (2335977, 767), (2336744, 975), (2337719, 1138), (2338857, 515)], [(2339372, 48), None, (2339420, 35), (2339455, 42), None, None, None, None, None, None, None, None, None, None, None, None, None, (2339497, 42), None, (2339539, 25), (2339564, 44), (2339608, 22), (2339630, 18), None, None, None, None, (2339648, 26), None, None, None, None, (2339674, 21), (2339695, 25), None, None, (2339720, 26), None, None, None, None, (2339746, 71), (2339817, 21), (2339838, 23), None, None, None, None, (2339861, 48), None, None, None, None, None, (2339909, 31), None, None, None, None, (2339940, 42), None, (2339982, 22), None, (2340004, 21), None, (2340025, 26), (2340051, 42), None, None, (2340093, 77), None, None, None, None, None, (2340170, 21), (2340191, 21), None, None, (2340212, 34), (2340246, 42), None, None, None, (2340288, 25), None, None, (2340313, 21), None, None, None, None, None, (2340334, 24), (2340358, 21), None, None, (2340379, 26), None, (2340405, 18), None, (2340423, 54), None, None, None, None, None, None, (2340477, 26), None, None, None, (2340503, 20), None, None, (2340523, 64), (2340587, 42), (2340629, 17), (2340646, 17), (2340663, 26), None, (2340689, 26), None, None, None, (2340715, 26), (2340741, 20), (2340761, 26), None, (2340787, 42), (2340829, 63), None, None, None, (2340892, 40), (2340932, 48), None, None, None, (2340980, 47), None, None, None, None, None, None, None, (2341027, 42), None, (2341069, 80), None, (2341149, 9), None, (2341158, 21), (2341179, 42), None, None, (2341221, 65), (2341286, 82), None, None, (2341368, 42), None, None, (2341410, 24), (2341434, 21), None, None, None, None, None, (2341455, 42), (2341497, 21), (2341518, 21), None, (2341539, 42), (2341581, 25), None, (2341606, 38), (2341644, 21), (2341665, 56), None, None, (2341721, 21), (2341742, 19), (2341761, 26), None, (2341787, 16), None, (2341803, 21), None, None, (2341824, 38), None, (2341862, 22), (2341884, 21), (2341905, 21), (2341926, 21), None, (2341947, 63), None, (2342010, 21), (2342031, 42), None, (2342073, 17), None, None, None, None, (2342090, 21), (2342111, 21), None, None, (2342132, 21), None, None, (2342153, 21), None, (2342174, 26), None, (2342200, 50), None, None, None, (2342250, 50), (2342300, 26), (2342326, 21), (2342347, 21), (2342368, 19), None, (2342387, 35), (2342422, 26), (2342448, 23), (2342471, 39), (2342510, 42), None, None, None, None, None, None, (2342552, 21), None, None, None, (2342573, 21), None, None, (2342594, 90), None, (2342684, 239), (2342923, 38), None, None, None, None]]  # noqa: E501
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
