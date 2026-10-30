# Gap dependency ordering — rose-window runs
# Source: art_01M64VKK2MPWCZP03XDVGKHM5S r2
# Correction target: Theo's flat gap list rpl_01M678S84KTYBXKBDH710F9Z9V r1
#
# Rationale: a controlled re-run with a fixed seed still uses the same
# linked image; variance analysis is non-reusable until provenance_image
# is confirmed. The other three gaps have no prerequisites.

from collections import defaultdict, deque

GAP_DEPS = {
    "provenance_image": [],
    "provenance_video": [],
    "audio":            [],
    "seed":             ["provenance_image"],
}

GAP_SCOPE = {
    "provenance_image": "all 3 runs",
    "provenance_video": "2 of 3 runs",
    "audio":            "all 3 runs",
    "seed":             "all 3 runs (gated)",
}

def topological_order(deps):
    in_degree = {n: 0 for n in deps}
    adj = defaultdict(list)
    for node, prereqs in deps.items():
        for p in prereqs:
            adj[p].append(node)
            in_degree[node] += 1
    queue = deque(n for n in in_degree if in_degree[n] == 0)
    order = []
    while queue:
        n = queue.popleft()
        order.append(n)
        for m in adj[n]:
            in_degree[m] -= 1
            if in_degree[m] == 0:
                queue.append(m)
    return order

if __name__ == "__main__":
    print("Dependency graph:")
    for gap, prereqs in GAP_DEPS.items():
        dep = f"requires {prereqs}" if prereqs else "no prerequisites"
        print(f"  {gap:<20} scope={GAP_SCOPE[gap]:<20} {dep}")
    print()
    print("Resolution order:", topological_order(GAP_DEPS))
    print()
    print("Step A (parallel now):  provenance_image, provenance_video, audio")
    print("Step B (after Step A):  seed (controlled re-run)")