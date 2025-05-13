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

# Part 4
# Compile & run "ADC_WAV_Converter.c" to generate "WAV_Output.wav"
wav_format_indicator = 1
if wav_format_indicator in output_list:
    print("Start compiling file...")
    compile_command = ["gcc", "ADC_WAV_Converter.c", "-o","ADC_WAV_Converter"]
    compile_result = subprocess.run(compile_command, capture_output = True, text = True)
    if compile_result.returncode != 0:
        print("Compilation result : Fail.")
        exit()
    else:
        print("Compilation result : Success.")
        print("Start generating audio file...")
        run_command = ["./ADC_WAV_Converter", "raw_ADC_values.data", "WAV_Output.wav"]
        run_result = subprocess.run(run_command, capture_output = True, text = True)
        print("Program result (Audio) : " + run_result.stdout)

# Part 5
# Convert the raw ADC values from bytes to unsigned 16-bit integers
png_format_indicator = 2
if png_format_indicator in output_list:
    print("Start generating image...")
    with open("raw_ADC_values.data", "rb") as file:
        raw_bytes = file.read()
        raw_ADC_values = np.frombuffer(raw_bytes, dtype = np.uint16)
        file.close()
    # Generate a time axis for the plot below
    time = np.arange(len(raw_ADC_values)) / sample_rate
    # Create a plot of "amplitude" vs "time" waveform (in PNG format)
    plt.figure()
    plt.plot(time, raw_ADC_values)
    plt.title("Amplitude v.s. Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("Raw ADC Data.png")
    plt.close()
    print("Program result (Image) : Success.")

