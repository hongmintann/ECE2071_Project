import time
import serial
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import csv

sample_rate = 6400
num_of_channels = 1
bytes_per_sample = 2

# Part 1
# Ask user to choose an operating mode
print("=============== MENU ===============")
print("1 -> Manual Recording Mode")
print("2 -> Distance Trigger Mode")
mode_choice = int(input(">> Enter mode : "))
if (mode_choice != 1 and mode_choice != 2):
    print("Invalid mode detected.")
    exit()
# Modify parameters of each operating mode
print("======== Parameter Settings ========")
if (mode_choice == 1):
    audio_duration = int(input(">> Enter audio duration (s) : "))
    operation_command = "1     "
else:
    ultrasonic_distance = int(input(">> Enter ultrasonic sensor threshold distance (cm) : "))
    audio_duration = int(input(">> Enter audio duration (s) : "))
    operation_command = f"2 - {ultrasonic_distance}"
print("")

# Part 2
cumulative_bytes = 0
total_bytes = audio_duration * (sample_rate * num_of_channels * bytes_per_sample)
# Open serial port for communication
ser = serial.Serial(port = "COM9", baudrate = 230400, bytesize = 8, parity = "N", stopbits = 1, timeout = 5)
print(f"Serial port : {ser.name}")
# Send operation mode chosen by the user to microcontroller
ser.write(operation_command.encode())
time.sleep(1)
# Open and write raw ADC value into binary file
print("Start reading data...")
with open("raw_ADC_values.data","wb") as file:
    while cumulative_bytes < total_bytes:
        read_bytes = ser.read(500)
        file.write(read_bytes)
        cumulative_bytes += len(read_bytes)
    file.close()
# Close serial port
ser.close()
print("Stop reading data...")
print("")

# Part 3
# Ask user to choose output formats
input_count = 0
output_list = []
print("========== Output Formats ==========")
print("1 -> '.wav' audio file")
print("2 -> '.png' image file")
print("3 -> '.csv. data file")
while (input_count < 3):
    output_format = int(input(">> Enter output format : "))
    if (output_format >= 1 and output_format <= 3):
        output_list.append(output_format)
    else:
        break
    input_count += 1
print("")

