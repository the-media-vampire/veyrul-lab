// UNTESTED PROPOSAL — derived from source readings, not executed
// Requires: ChucK with OSC support; Mixxx sending OSC on port 7400
// Bridge: Mixxx MIDI/OSC output → ChucK OscIn
//
// Mechanism: ChucK shred advances time only via `=> now`.
// Mixxx BPM drives the beat duration; OSC carries it.

OscIn osc;
7400 => osc.port;
osc.listenAll();

OscMsg msg;
float bpm;
120.0 => bpm;  // default; overwritten by OSC

// Bounded loop: exits when Mixxx sends bpm=0 (playlist end signal)
while( true ) {
    osc => now;  // advance until OSC event
    if( osc.recv(msg) ) {
        if( msg.address == "/mixxx/bpm" ) {
            msg.getFloat(0) => bpm;
        }
        if( bpm <= 0.0 ) break;  // termination: Auto DJ stopped
    }
    // beat duration from Mixxx BPM
    dur beat;
    (60.0 / bpm) :: second => beat;
    beat => now;  // advance one beat
    // Insert ChucK FX trigger here, e.g. SinOsc freq change
}
// Explicit termination: no zombie shred