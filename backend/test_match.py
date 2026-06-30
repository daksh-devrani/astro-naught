import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engine.math_engine import VedicMathEngine
from engine.astrology import AstrologyEngine
from engine.ashtakoot import AshtakootCalculator

math_engine = VedicMathEngine()
astrology_engine = AstrologyEngine()

# Person 1: 27-09-2005 12:47pm Bareilly
# UTC time: 07:17 AM
m1 = math_engine.calculate_positions(2005, 9, 27, 7, 17, 28.3670, 79.4304, 'KP')
c1 = astrology_engine.generate_chart(m1, 'KP')
moon_deg_1 = c1["planets"]["Moon"]["longitude"]
moon_sign_1 = c1["planets"]["Moon"]["sign_number"]

# Person 2: 27-02-1999 2:51pm Bareilly
# UTC time: 09:21 AM
m2 = math_engine.calculate_positions(1999, 2, 27, 9, 21, 28.3670, 79.4304, 'KP')
c2 = astrology_engine.generate_chart(m2, 'KP')
moon_deg_2 = c2["planets"]["Moon"]["longitude"]
moon_sign_2 = c2["planets"]["Moon"]["sign_number"]

res = AshtakootCalculator.calculate(moon_deg_1, moon_deg_2, moon_sign_1, moon_sign_2)
print("Boy Moon Deg:", moon_deg_1)
print("Boy Moon Sign:", moon_sign_1)
print("Girl Moon Deg:", moon_deg_2)
print("Girl Moon Sign:", moon_sign_2)
print("Ashtakoot Result:", res)
