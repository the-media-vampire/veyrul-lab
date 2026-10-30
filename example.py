from beat_order_contract import Beat, BeatOrderContract
import json

# Conforming: mirrors the structure seen in art_01M64VKF6MVCCAAVV3YZS2A2TY r2
good = BeatOrderContract(20.0, [
    Beat("open",  0.0,  "wide"),
    Beat("set",   2.5,  "wide"),
    Beat("portA", 9.2,  "portrait", ["Char A"]),
    Beat("portB", 11.8, "portrait", ["Char B"]),
    Beat("close", 16.5, "two_shot", ["Char A", "Char B"]),
])
print("good:", good.validate() or "OK")
print(json.dumps(good.to_contract(), indent=2))

# Violation: portrait opens, portrait closes, only one middle portrait
bad = BeatOrderContract(20.0, [
    Beat("portFirst", 0.0,  "portrait", ["X"]),
    Beat("wide",      5.0,  "wide"),
    Beat("portB",    11.0,  "portrait", ["Y"]),
    Beat("closePort",17.0,  "portrait", ["X"]),
])
print("bad:", bad.validate())