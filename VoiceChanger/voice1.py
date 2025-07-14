import tkinter as tk
from pyo import *

# === Start pyo server ===
s = Server().boot()
s.start()

# === Mic input ===
raw_mic = Input(chnl=0)

# === Noise gate threshold control ===
noise_gate_threshold = SigTo(value=0.005, time=0.1)  # smoother transitions

# Noise gate: compare absolute input to threshold, with smoother transitions using SigTo
gate = Compare(Abs(raw_mic), noise_gate_threshold, ">")

# Apply gate and highpass filter to reduce low-frequency rumble
filtered_mic = ButHP(raw_mic * gate, freq=80)

# === Control signals with smoothing ===
robot_amount = SigTo(value=0.5, time=0.05)
chord_amount = SigTo(value=0.5, time=0.05)
echo_amount = SigTo(value=0.0, time=0.05)
volume = SigTo(value=0.8, time=0.05)  # start a bit lower to prevent clipping

# === Robot effect ===
carrier_freq = Sig(100)
carrier = Sine(freq=carrier_freq)
robot = filtered_mic * carrier

# === Chord effect (harmonizer) ===
root = Harmonizer(filtered_mic, transpo=0)
third = Harmonizer(filtered_mic, transpo=4)
fifth = Harmonizer(filtered_mic, transpo=7)
chord = Mix([root, third, fifth], voices=2) * 0.5

# === Mix robot + chord + dry ===
total = robot_amount + chord_amount
total = Clip(total, 0, 2)
dry_amount = 1 - (total / 2)

mixed = (filtered_mic * dry_amount) + (robot * robot_amount) + (chord * chord_amount)

# === Echo ===
delay = Delay(mixed, delay=0.25, feedback=0.15, mul=echo_amount)  # lowered feedback

# === Final output with limiter to avoid clipping ===
final = Compress((mixed + delay) * volume, thresh=-20, ratio=4, risetime=0.01, falltime=0.1)
final.out()

# === GUI callbacks ===
def update_robot(val):
    robot_amount.value = float(val)

def update_chord(val):
    chord_amount.value = float(val)

def update_echo(val):
    echo_amount.value = float(val)

def update_volume(val):
    volume.value = float(val)

def update_gate_thresh(val):
    noise_gate_threshold.value = float(val)

# === Build GUI ===
root_tk = tk.Tk()
root_tk.title("Robot, Chord, Echo, Volume & Gate Threshold Controls")

tk.Label(root_tk, text="Robot Effect (0 to 2)").pack()
robot_slider = tk.Scale(root_tk, from_=0, to=2, resolution=0.01,
                        orient=tk.HORIZONTAL, command=update_robot)
robot_slider.set(0.5)
robot_slider.pack()

tk.Label(root_tk, text="Chord Effect (0 to 2)").pack()
chord_slider = tk.Scale(root_tk, from_=0, to=2, resolution=0.01,
                        orient=tk.HORIZONTAL, command=update_chord)
chord_slider.set(0.5)
chord_slider.pack()

tk.Label(root_tk, text="Echo Effect (0 to 1)").pack()
echo_slider = tk.Scale(root_tk, from_=0, to=1, resolution=0.01,
                       orient=tk.HORIZONTAL, command=update_echo)
echo_slider.set(0.0)
echo_slider.pack()

tk.Label(root_tk, text="Master Volume (0 to 2)").pack()
volume_slider = tk.Scale(root_tk, from_=0, to=2, resolution=0.01,
                         orient=tk.HORIZONTAL, command=update_volume)
volume_slider.set(0.8)
volume_slider.pack()

tk.Label(root_tk, text="Noise Gate Threshold (0 to 0.05)").pack()
gate_thresh_slider = tk.Scale(root_tk, from_=0, to=0.05, resolution=0.001,
                              orient=tk.HORIZONTAL, command=update_gate_thresh)
gate_thresh_slider.set(0.005)
gate_thresh_slider.pack()

root_tk.mainloop()
