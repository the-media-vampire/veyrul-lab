-- TIC-80 Probe Additions — Vera's Falsification Companion
-- Paste AFTER cart.lua content (replace TIC() function), or use standalone.
-- Source: art_01M6Q7AXM1R42XNV7AW8BVSBCY rev 1
-- Status: UNRUN — proposals only. Requires TIC-80 runtime.

-- TIER 1 PROBE: Pixel boundary test
-- Draw at (239,135) = last valid pixel per README claim.
-- Draw at (240,136) = one beyond. If both render, the 240x136 claim is in question.
local function probe_screen_bounds()
  pix(239, 135, 7)  -- should render (white dot, bottom-right corner)
  pix(240, 136, 8)  -- should be clipped or error; if visible, claim fails
  print("Bounds probe: see corners", 2, 70, 14)
end

-- TIER 2 PROBE: Sound channel boundary test
-- Channel 3 (0-indexed) is the last of 4. Channel 4 should not exist.
local function probe_channels()
  local ok, err = pcall(function()
    sfx(0, "C-3", 1, 3, 15)  -- channel 3: last valid
  end)
  print("Ch3 ok: "..tostring(ok), 2, 80, ok and 11 or 8)
  -- Channel 4 probe: TIC-80 may not raise pcall-catchable errors.
  -- Manual check: does sfx(0,"C-3",1,4,15) produce audio or silently succeed?
  print("Ch4: run sfx(0,'C-3',1,4,15) manually", 2, 88, 6)
end

-- TIER 2 PROBE: Button out-of-range
local function probe_btn_range()
  local b8 = btn(8)  -- index 8 = 9th button; should be nil or false
  print("btn(8)=" .. tostring(b8) .. " (expect false/nil)", 2, 100, b8 and 8 or 11)
end

function TIC()
  cls(0)
  print("Vera Falsification Probes", 2, 2, 7)
  print("UNRUN PROPOSALS - fill in Observed", 2, 10, 8)
  probe_screen_bounds()
  probe_channels()
  probe_btn_range()
end