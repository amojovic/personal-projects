I was looking for a real time voice changer online.

All of them either seem overpriced and/or really unintuitive to set up, especially because i just wanted to mess around with my friends via voice modulator online.

So i decided to start building my own (very basic one for now).

This is what it does currently:

Captures live audio from your microphone.

Applies a noise gate to cut out low-level background noise.

Processes the audio with several effects:

Robot effect: Modulates the mic input with a sine wave to create a robotic sound.

Chord effect: Adds harmony notes (root, third, fifth) to the mic input, creating a chord.

Echo effect: Adds delayed repetitions (echo) to the sound.

Mixes the original (dry) signal with the robot and chord effects.

Applies volume control and a compressor to prevent audio clipping.

Outputs the processed sound live to your speakers/headphones.

User controls (via Tkinter GUI):
Sliders to adjust the amount of:

Robot effect (0 to 2)

Chord effect (0 to 2)

Echo effect (0 to 1)

Master volume (0 to 2)

Noise gate threshold (0 to 0.05) to control how sensitive the noise gate is.

///////////////////////////////////////////////////////////////////////////////////////////////////////////

TL;DR version:

You speak into your mic, and the program modifies your voice in real time with cool effects. You can control how robotic it sounds, add harmonies, create echoes, adjust volume, and filter out noise — all through an easy-to-use slider interface.






