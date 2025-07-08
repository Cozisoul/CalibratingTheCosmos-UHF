s.play {
  var env = Env.new(0, 1, 10).decay(2);
  var amp = EnvGen.arenv(env);

  // Generate the audio signal with an envelope
  Out.ar(0) = amp * 0.5;

  // Play the audio signal for 5 second
  s.play(1, 44100);
}

// Define a simple pulse synthesizer
s.addSynth(SynthType.Pulse);

// Apply a low-pass filter to the synthesized sound
s.addEffect(EQ { type: Lowpass, cutoff: 100 });

// Load and visualize the generated audio signal
s.load("example.wav");
s.addSynth(SynthType.Pulse);
s.addEffect(EQ { type: Lowpass, cutoff: 100 });
.s.view;

// Save the generated audio file
44100.write("example2.wav");