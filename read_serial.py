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

