// Condition B: flip via DrawTextureRec with flipped Rectangle
// Compile: gcc condition_b.c -lraylib -lm -o condition_b
// Source: art_01M6Q6PZWS3BYDS2A1RZQB7E0H r1 (README lines 59-65, 75-85)

#include "raylib.h"

int main(void) {
    const int W = 320, H = 240;
    InitWindow(W, H, "flip-B: DrawTextureRec bottom-up rect");
    SetTargetFPS(60);

    RenderTexture2D rt = LoadRenderTexture(W, H);

    // Identical content draw — fixed variable
    BeginTextureMode(rt);
        ClearBackground(RAYWHITE);
        DrawRectangle(10, 10, W-20, H-20, LIGHTGRAY);
        DrawRectangleLines(0, 0, W, H, RED);  // 1-px border stress case
        DrawText("RT content", 40, 100, 20, DARKGRAY);
    EndTextureMode();

    BeginDrawing();
        ClearBackground(RAYWHITE);
        // Condition B: source rect starts from bottom row, negative height
        Rectangle srcRect = { 0, (float)rt.texture.height,
                              (float)rt.texture.width,
                             -(float)rt.texture.height };
        DrawTextureRec(rt.texture, srcRect, (Vector2){0,0}, WHITE);
    EndDrawing();

    TakeScreenshot("condition_b.png");  // capture for pixel diff
    WaitTime(0.5);
    UnloadRenderTexture(rt);
    CloseWindow();
    return 0;
}