"""SoundCraft dual-interface dispatcher (adapter contract v0.1).
Derived from documented interfaces only; not run against a live instance.
License: MIT
"""
from __future__ import annotations
import json, socket, subprocess
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ConfinementRoots:
    """MCP in-process roots. --connect + these flags is documented as an error."""
    read: list[str] = field(default_factory=list)
    write: list[str] = field(default_factory=list)
    def as_flags(self) -> list[str]:
        return [f for r in self.read for f in ("--read-root", r)] + \
               [f for w in self.write for f in ("--write-root", w)]

@dataclass
class Command:
    name: str
    params: dict[str, Any] = field(default_factory=dict)

@dataclass
class CommandResult:
    transport: str
    raw: str
    exit_code: int | None = None

def desktop_reachable(host="127.0.0.1", port=7777, timeout=0.5) -> bool:
    """Probe TCP control channel. Port 7777 is a placeholder."""
    try:
        with socket.create_connection((host, port), timeout=timeout): return True
    except OSError: return False

def send_via_tcp(cmd: Command, host="127.0.0.1", port=7777) -> CommandResult:
    msg = json.dumps({"type": "engine.execute",
                      "command": cmd.name, "params": cmd.params}) + "\n"
    with socket.create_connection((host, port), timeout=5.0) as s:
        s.sendall(msg.encode())
        data = b""
        while True:
            chunk = s.recv(4096)
            if not chunk or b"\n" in chunk: data += chunk; break
            data += chunk
    return CommandResult("tcp", data.decode().strip())

def send_via_mcp(cmd: Command, session: str,
                 roots: ConfinementRoots | None = None) -> CommandResult:
    batch = json.dumps({"tools": [{"name": "engine.execute",
        "input": {"command": cmd.name, "params": cmd.params}}]})
    flags = roots.as_flags() if roots else []
    p = subprocess.run(["soundcraft-cli", "mcp", *flags, session],
                       input=batch, capture_output=True, text=True)
    return CommandResult("mcp", p.stdout.strip(), p.returncode)

class SoundCraftDispatcher:
    """Prefer TCP when desktop is reachable; fall back to MCP."""
    def __init__(self, session: str, roots: ConfinementRoots | None = None,
                 host="127.0.0.1", port=7777):
        self.session, self.roots, self.host, self.port = session, roots, host, port
    def run(self, cmd: Command) -> CommandResult:
        if desktop_reachable(self.host, self.port):
            return send_via_tcp(cmd, self.host, self.port)
        return send_via_mcp(cmd, self.session, self.roots)

# Example (not executed):
# d = SoundCraftDispatcher("demo.scraft",
#       ConfinementRoots(read=["/proj"], write=["/proj"]))
# print(d.run(Command("mix.volume", {"track": "Kick", "db": -6})))