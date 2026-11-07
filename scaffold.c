/* scaffold.c — fixed window context for both conditions
 * Source: art_01M6Q6PZWS3BYDS2A1RZQB7E0H r1, README lines 75-85
 * Commit: 4bfb72d
 * NOT compiled or run; source-publication only.
 */
#include "raylib.h"

int main(void) {
    InitWindow(320, 240, "lp-experiment");
    SetTargetFPS(1);

    /* Insert one candidate call here, then close */
    while (!WindowShouldClose()) {
        BeginDrawing();
        ClearBackground(RAYWHITE);

        /* CANDIDATE_CALL_HERE */

        EndDrawing();
    }

    CloseWindow();
    return 0;
}