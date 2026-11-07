-- TIC-80 Lua Starter Cartridge
-- Constants from README (art_01M6Q7AXM1R42XNV7AW8BVSBCY rev 1, lines 46-65)
-- These are documented limits, not runtime-verified.

local SCREEN_W    = 240   -- README line 46: 240x136 display
local SCREEN_H    = 136
local PALETTE_N   = 16    -- README line 46: 16 color palette
local SPRITES_N   = 256   -- README line 46: 256 8x8 color sprites
local CHANNELS_N  = 4     -- README line 46: 4 channel sound
local CTRL_N      = 4     -- README line 64: up to 4 controllers
local BTN_N       = 8     -- README line 65: up to 8 buttons each

-- Baseline check: draw constants to screen.
-- Observable outcome: if TIC-80 runs this, the printed values
-- should match the README numbers. Mismatch = documented claim fails.
local function draw_baseline()
  cls(0)
  print("TIC-80 README Baseline", 2, 2, 7)
  print("SCREEN: "..SCREEN_W.."x"..SCREEN_H, 2, 12, 11)
  print("PALETTE: "..PALETTE_N.." colors",    2, 20, 11)
  print("SPRITES: "..SPRITES_N,               2, 28, 11)
  print("CHANNELS: "..CHANNELS_N,             2, 36, 11)
  print("CTRLS: "..CTRL_N.." x "..BTN_N.."btn", 2, 44, 11)
end

-- Live input probe: show which buttons are pressed on ctrl 0.
-- Baseline: 0 buttons pressed with no input.
local function draw_input()
  print("BTN CTRL0:", 2, 56, 6)
  local x = 72
  for b = 0, BTN_N - 1 do
    local col = btn(b) and 11 or 1
    print(tostring(b), x + b * 8, 56, col)
  end
end

function TIC()
  draw_baseline()
  draw_input()
end

-- END --