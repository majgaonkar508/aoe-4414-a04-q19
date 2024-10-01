# ecef_to_eci.py
#
# Usage: python3 ecef_to_eci.py year month day hour minute second ecef_x_km ecef_y_km ecef_z_km
#  Converts from year, month, day, hour, minute, second and ECEF frame to ECI frame
# Parameters:
#  year: year of interest - int
#  month: month of interest - int
#  day: day of interest - int
#  hour: hour of interest - int
#  minute: minute of interest - int
#  second: second of interest - float
#  ecef_x_km: x-component of ECEF frame
#  ecef_y_km: y-component of ECEF frame
#  ecef_z_km: z-component of ECEF frame
# Output:
#  eci_x_km: x-component of ECI frame
#  eci_y_km: y-component of ECI frame
#  eci_z_km: z-component of ECI frame
# Written by Mandar Ajgaonkar
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

# import Python modules
import math # math module
import sys # argv

# constants
w = 7.292115*10**-5 # rad/s

# initialize script arguments
year = float('nan')
month = float('nan')
day = float('nan')
hour = float('nan')
minute = float('nan')
second = float('nan')
ecef_x_km = float('nan')
ecef_y_km = float('nan')
ecef_z_km = float('nan')

# parse script arguments
if len(sys.argv) == 10:
    try:
        year = int(sys.argv[1])
        month = int(sys.argv[2])
        day = int(sys.argv[3])
        hour = int(sys.argv[4])
        minute = int(sys.argv[5])
        second = float(sys.argv[6])
        ecef_x_km = float(sys.argv[7])
        ecef_y_km = float(sys.argv[8])
        ecef_z_km = float(sys.argv[9])
    except ValueError:
      print("Error: year, month, day, hour, minute, second, ecef_x_km, ecef_y_km, ecef_z_km must be numeric.")
      exit()
else:
  print('python3 ecef_to_eci.py year month day hour minute second ecef_x_km ecef_y_km ecef_z_km')
  exit()

# main script for calculating fractional julian date
jd = day - 32075 + 1461*(year + 4800 - (14 - month)//12)//4 + 367*(month - 2 + (14 - month)//12*12)//12 - 3*((year + 4900 - (14 - month)//12)//100)//4
jd_midnight = jd - 0.5
d_frac = (second + 60*(minute + 60*hour))/86400
jd_frac = jd_midnight + d_frac

# calculate GMST angle 
t_ut1 = (jd_frac - 2451545.0)/36525
GMST_sec = 67310.54841 + (876600*60*60 + 8640184.812866)*t_ut1 + 0.093104*t_ut1**2 - 6.2*10**-6*t_ut1**3

# calculate additional seconds
add_sec = math.fmod(GMST_sec, 86400) 

# convert additional seconds to radians
add_rad = add_sec*w

# ensure GMST_rad is within [0, 2pi)
GMST_rad = math.fmod(add_rad + 2*math.pi, 2*math.pi)

# calculate ECI vector 
eci_x_km = ecef_x_km*math.cos(GMST_rad) + ecef_y_km*-math.sin(GMST_rad)
eci_y_km = ecef_x_km*math.sin(GMST_rad) + ecef_y_km*math.cos(GMST_rad)
eci_z_km = ecef_z_km

# print results
print(eci_x_km)
print(eci_y_km)
print(eci_z_km)
