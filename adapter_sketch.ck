// adapter_sketch.ck
// Integration scaffold: combines clock-print, SinOsc patch, and mic-in
// as three concurrent shreds with explicit gain budgeting.
// UNTESTED PROPOSAL derived from curator reading (art_01M6QCMFBB28W6PJMFEA3EKF9G r1).
// License: MIT (this file). ChucK itself: see ChucK README lines 130-131.

// --- Shared output gain (budget: sum of branches <= 1.0) ---
Gain master => dac;
0.8 => master.gain;

// --- Branch 1: mic passthrough (from adc.ck pattern) ---
adc => Gain micBranch => master;
0.4 => micBranch.gain;  // half of master budget

// --- Branch 2: SinOsc (from demo3.ck pattern) ---
// Runs bounded: 6 iterations, doubles frequency each pass
fun void sinoscShred() {
    110.0 => float freq;
    6 => int x;
    while (x > 0) {
        SinOsc s => Gain sinBranch => master;
        0.4 => sinBranch.gain;  // other half of master budget
        freq => s.freq;
        500::ms => now;         // hold for 500ms
        s =< sinBranch;         // disconnect before next iteration
        2.0 *=> freq;
        1 -=> x;
    }
}
spork ~ sinoscShred();

// --- Branch 3: clock printer (from tick.ck pattern) ---
fun void clockPrinter() {
    while (true) {
        <<< "now (s):", now / second >>>;
        1::second => now;
    }
}
spork ~ clockPrinter();

// --- Main shred: advance time to keep process alive ---
while (true) {
    100::ms => now;
}