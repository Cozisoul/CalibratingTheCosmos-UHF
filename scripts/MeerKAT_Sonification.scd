s.options.outDevice = "External Headphones"

s.boot;

(
// Refined cosmic drone
~synth = {
    var sig, freqsClean, numOscs, oscArray;
    freqsClean = ~freqs.reject(_.isNil);
    numOscs = freqsClean.size.min(20);
    oscArray = Array.fill(numOscs, { |i|
        var freq = freqsClean.wrapAt(i) + LFNoise1.kr(0.2).range(-0.5, 0.5); // micro detune
        var amp = 0.2 / numOscs;
        SinOsc.ar(freq, 0, amp)
    });
    sig = oscArray.sum;
    sig = LPF.ar(sig, 500 + LFNoise1.kr(0.1).range(0, 200)); // gently moving filter
    sig = FreeVerb.ar(sig, mix: 0.4); // add space
    Out.ar(0, sig ! 2);
}.play;
)

(
// Use `~` for top-level variables
~csvPath = "/Users/thapelomasebe/Radio/bandpass_export.csv";
~data = CSVFileReader.read(~csvPath);
~row = ~data[0]; // First antenna, "antenna_00"
~amps = ~row[1..]; // Skip the label
~ampsFloat = ~amps.collect(_.asFloat);

// Map to frequencies
~minFreq = 100;
~maxFreq = 1000;
~freqs = ~ampsFloat.collect { |val|
    if (val.notNil) {
        val.linexp(0.0, 2.0, ~minFreq, ~maxFreq);
    } {
        nil
    }
};
//
 Play cosmic drone
~synth = {
    var sig;
    var freqsClean = ~freqs.reject(_.isNil);
    var numOscs = freqsClean.size.min(20);
    var oscArray = Array.fill(numOscs, { |i|
        var freq = freqsClean.wrapAt(i);
        var amp = 0.5 / numOscs;
        SinOsc.ar(freq, 0, amp)
    });
    sig = oscArray.sum;
    sig = sig * 0.5;
    Out.ar(0, sig ! 2);
}.play;
)

(
// Granular cosmic layer using MeerKAT data
~gran = {
    var freqsClean = ~freqs.reject(_.isNil);
    var numGrains = 10;
    var density = 20;
    var trig = Dust.kr(density);
    var freq = if(freqsClean.size > 0, { freqsClean.choose }, { 440 }); // fallback
    var sig = GrainSin.ar(
        2,      // stereo
        trig,   // trigger
        0.2,    // grain duration
        freq,   // frequency in Hz
        0,      // pan
        0.2     // amplitude
    );
    sig = sig * 0.3;
    sig = FreeVerb.ar(sig, mix: 0.4);
    Out.ar(0, sig);
}.play;
)

(
// Use `~` for top-level variables
~csvPath = "/Users/thapelomasebe/Radio/bandpass_export.csv";
~data = CSVFileReader.read(~csvPath);
~row = ~data[0]; // First antenna, "antenna_00"
~amps = ~row[1..]; // Skip the label
~ampsFloat = ~amps.collect(_.asFloat);

// Map to frequencies
~minFreq = 100;
~maxFreq = 1000;
~freqs = ~ampsFloat.collect { |val|
    if (val.notNil) {
        val.linexp(0.0, 2.0, 50, 2000);
    } {
        nil
    }
};

// Play cosmic drone
~synth = {
    var sig;
    var freqsClean = ~freqs.reject(_.isNil);
    var numOscs = freqsClean.size.min(20);
    var oscArray = Array.fill(numOscs, { |i|
        var freq = freqsClean.wrapAt(i);
        var amp = 0.7 / numOscs;
        SinOsc.ar(freq, 0, amp)
    });
    sig = oscArray.sum;
    sig = sig * 0.5;
    Out.ar(0, sig ! 2);
}.play;
)

// To stop playback:
(
// When ready to stop the drone
~synth.free
)

(
// --- First, define some sample data that looks like your real data ---
// Let's pretend these numbers are from your bandpass amplitude plot.
// Notice they are not in an audible frequency range.
~freqs = [0.85, 0.9, 0.92, 1.0, 1.05, 1.1, 1.15];


// --- Now, run the new, corrected granular synth ---
~gran = {
    var freqsClean, rawDataValue, mappedFreq;
    var density = 20;
    var trig = Dust.kr(density);

    // Get a clean list of numbers from your data source
    freqsClean = ~freqs.reject(_.isNil);

    // Choose one raw data point from your list
    rawDataValue = if(freqsClean.size > 0, { freqsClean.choose }, { 1.0 });

    // ===== THIS IS THE CRITICAL FIX =====
    // Map the raw data value to an audible frequency range.
    // Here, we map numbers from the range [0.8 to 1.2] to the range [200 Hz to 1500 Hz].
    mappedFreq = rawDataValue.linlin(0.8, 1.2, 200, 1500);

    var sig = GrainSin.ar(
        2,      // stereo
        trig,   // trigger
        0.2,    // grain duration
        mappedFreq, // <<< USE THE NEW, MAPPED FREQUENCY
        0,      // pan
        0.2     // amplitude
    );

    sig = sig * 0.3;
    sig = FreeVerb.ar(sig, mix: 0.4, room: 0.8);
    Out.ar(0, sig);
}.play;
)

// To stop the sound, run this:
// ~gran.free;

s.freeAll;