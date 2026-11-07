// Condition A: flip via negative srcRect height in DrawTexturePro
// Compile: gcc condition_a.c -lraylib -lm -o condition_a
// Source: art_01M6Q6PZWS3BYDS2A1RZQB7E0H r1 (README lines 59-65, 75-85)

#include "raylib.h"

int main(void) {
    const int W = 320, H = 240;
    InitWindow(W, H, "flip-A: DrawTexturePro negative height");
    SetTargetFPS(60);

    RenderTexture2D rt = LoadRenderTexture(W, H);

    // Draw into render texture (content is upside-down in GPU memory)
    BeginTextureMode(rt);
        ClearBackground(RAYWHITE);
        DrawRectangle(10, 10, W-20, H-20, LIGHTGRAY);
        DrawRectangleLines(0, 0, W, H, RED);  // 1-px border stress case
        DrawText("RT content", 40, 100, 20, DARKGRAY);
    EndTextureMode();

    BeginDrawing();
        ClearBackground(RAYWHITE);
        // Condition A: negative height flips the source rect
        Rectangle srcRect  = { 0, 0, (float)rt.texture.width,
                                     -(float)rt.texture.height };
        Rectangle destRect = { 0, 0, (float)W, (float)H };
        DrawTexturePro(rt.texture, srcRect, destRect,
                       (Vector2){0,0}, 0.0f, WHITE);
    EndDrawing();

    TakeScreenshot("condition_a.png");  // capture for pixel diff
    WaitTime(0.5);
    UnloadRenderTexture(rt);
    CloseWindow();
    return 0;
}