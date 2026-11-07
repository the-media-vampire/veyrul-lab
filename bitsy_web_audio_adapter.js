/**
 * Bitsy v0.2 → Web Audio API sound adapter (stub / integration contract)
 *
 * Interface source: art_01M6Q546ZG458Z26XTSCVA605K rev 1
 * system.md @ ee412fa8c072d16af4aedd90d4ad3fb7306911b0
 *
 * ASSUMPTIONS (must hold for this adapter to work):
 *  1. Host runs in a browser with Web Audio API available.
 *  2. Caller triggers an AudioContext after a user gesture (browser policy).
 *  3. Bitsy frequency unit is decihertz (dHz): Hz = dHz / 10.
 *  4. Bitsy volume range 0–15 maps linearly to Web Audio gain 0.0–1.0.
 *  5. PULSE_1_8 / PULSE_1_4 / PULSE_1_2 map to 'square' (closest available
 *     OscillatorType); Web Audio has no native duty-cycle control.
 *  6. This adapter covers only bitsy.sound() and bitsy.loop().
 *     Memory, graphics and input are out of scope here.
 *
 * NOT TESTED against a running Bitsy engine. Experimental API (v0.2 is
 * flagged as likely to change significantly version-to-version).
 */

// --- Constants (mirror system.md) ---
const SOUND1 = 'SOUND1';
const SOUND2 = 'SOUND2';
const PULSE_1_8 = 'PULSE_1_8';  // duty 12.5% — no Web Audio equivalent; use square
const PULSE_1_4 = 'PULSE_1_4';  // duty 25%   — no Web Audio equivalent; use square
const PULSE_1_2 = 'PULSE_1_2';  // square wave — direct square OscillatorType

// --- Adapter state ---
const ctx = new AudioContext();
const channels = {};

function _getOrCreateChannel(channel) {
  if (!channels[channel]) {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'square'; // closest available; see assumption 5
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    gain.gain.setValueAtTime(0, ctx.currentTime); // silent until triggered
    channels[channel] = { osc, gain };
  }
  return channels[channel];
}

/**
 * bitsy.sound(channel, duration, frequency, volume, pulse)
 *
 * channel:   SOUND1 | SOUND2
 * duration:  milliseconds
 * frequency: decihertz (dHz)  → divide by 10 for Hz
 * volume:    0–15             → divide by 15 for gain 0.0–1.0
 * pulse:     PULSE_1_8 | PULSE_1_4 | PULSE_1_2
 */
function sound(channel, duration, frequency, volume, pulse) {
  const { osc, gain } = _getOrCreateChannel(channel);
  const now = ctx.currentTime;
  const hz = frequency / 10;          // dHz → Hz (assumption 3)
  const gainVal = volume / 15;        // 0–15 → 0.0–1.0 (assumption 4)
  const durationSec = duration / 1000;

  // pulse type: Web Audio only has 'square'; log the mismatch
  if (pulse !== PULSE_1_2) {
    console.warn(`[bitsy-adapter] ${pulse} has no Web Audio equivalent; using square.`);
  }

  osc.frequency.setValueAtTime(hz, now);
  gain.gain.cancelScheduledValues(now);
  gain.gain.setValueAtTime(gainVal, now);
  gain.gain.setValueAtTime(0, now + durationSec); // silence after duration
}

/**
 * bitsy.loop(fn)
 *
 * Registers fn to be called each animation frame.
 * fn receives elapsed time dt in milliseconds (system.md line 207).
 */
let _loopFn = null;
let _lastTime = null;

function loop(fn) {
  _loopFn = fn;
  if (!_lastTime) _startLoop();
}

function _startLoop() {
  function tick(timestamp) {
    if (_loopFn) {
      const dt = _lastTime !== null ? timestamp - _lastTime : 0;
      _lastTime = timestamp;
      _loopFn(dt);
    }
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

// --- Exported bitsy global (host must attach this to window.bitsy) ---
const bitsySoundAdapter = { SOUND1, SOUND2, PULSE_1_8, PULSE_1_4, PULSE_1_2, sound, loop };

export default bitsySoundAdapter;