// cursor_sync_patch.js
// Proposed patch for index.html from art_01M6SQCKMHR4X6A3P84EPKAT0J rev 1.
// Adds cursor_step to the existing timing log so check_cursor_sync.js can compare.
// NOT browser-tested. Structural inspection only.

// --- In the Draw-scheduled callback, alongside the existing step-number display:
// Replace or extend the existing getDraw().schedule block like this:

/*
  Tone.getDraw().schedule((drawTime) => {
    const displayedStep = currentStep; // the same value shown in <span id="now">
    document.querySelector('[data-current]')?.removeAttribute('data-current');
    document
      .querySelectorAll('.cell')
      [displayedStep]
      ?.setAttribute('data-current', '');

    // NEW: push cursor position into the existing window._log array
    if (window._log && window._log.length > 0) {
      const lastEntry = window._log[window._log.length - 1];
      // Tag the matching entry; audio_step was written in the Transport callback
      lastEntry.cursor_step = displayedStep;
    }
  }, time);
*/

// STRUCTURAL NOTES (inspected, not executed):
// 1. getDraw().schedule fires on the render thread at approximately drawTime.
//    It is NOT guaranteed to fire in the same animation frame as the audio
//    callback; that gap is exactly what we are measuring.
// 2. The _log entry is written first in the Transport callback (audio thread
//    lookahead), cursor_step is appended later. If the Draw callback is
//    delayed by a heavy frame, cursor_step will be missing or one entry behind.
// 3. A missing cursor_step on an entry is itself a reportable event—
//    check_cursor_sync.js counts those separately as LATE_DRAW.

console.log('cursor_sync_patch: structural reference only, not executed');