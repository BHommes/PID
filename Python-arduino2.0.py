import serial
import matplotlib.pyplot as plt
from collections import deque


port = 'COM6'      
baudrate = 9600
max_points = 100   

ser = serial.Serial(port, baudrate)
plt.ion()
data = deque() # Voor geheugen op de t as
# data = deque([0]*max_points, maxlen=max_points) # Voor updatende t as # Maakt een soort schuivende array met data (deque = dubbel ended queue), dus een soort snelle append/pop(0)
fig, ax = plt.subplots()
line, = ax.plot(data)
ax.set_ylim(0, 50)
ax.set_title("Sensorwaarde LIVE")
ax.set_xlabel("Samples")
ax.set_ylabel("Afstand (cm)")
ax.axhline(y=25, color='r', linestyle='--')  # rode stippellijn op y=25
try:
    while True:
        if ser.in_waiting > 0:
            try:
                line_str = ser.readline().decode('utf-8').strip() # stanaard decodering van bite inkomend van arduino
                value = int(line_str)
                data.append(value)

                line.set_ydata(data)
                line.set_xdata(range(len(data)))

                ax.relim() # Herbereken min en max waarde
                ax.autoscale_view(True, True, False) #herbereken x & y as om mee te schuiven
                plt.pause(0.01)
            except ValueError: #sla onnozele data over
                pass  
except KeyboardInterrupt: # Interrupt, CTRL + C voor het sluiten.
    ser.close()

# Lijkt alleen maar te werken in normale Python kernel. Zodra ik het in juypter run krijg ik problemen. 