import matplotlib.pyplot as plt

n = 50

inf = 9999

grid = []
for x in range(n+1):
    for y in range(n+1):
        grid.append((x, y))
grid.remove((0, 0))

rights = []

for i, p in enumerate(grid):
    for q in grid[i+1:]:

        px, py = p
        qx, qy = q

        if p == q:
            continue

        if ((px == 0 and qy == 0) or
            (py == 0 and qx == 0) or
            (px == 0 and py == qy) or
            (qx == 0 and py == qy) or
            (py == 0 and px == qx) or
            (qy == 0 and px == qx)
            ):
            rights.append((p, q))
        else:
            op_slope = inf if px == 0 else py / px
            oq_slope = inf if qx == 0 else qy / qx
            pq_slope = inf if qy - py == 0 else (qx - px) / (qy - py)

            if op_slope == -pq_slope or oq_slope == -pq_slope:
                rights.append((p, q))

print(len(rights))

if n <= 3:

    for i, ((px, py), (qx, qy)) in enumerate(rights):
        ax = plt.subplot(6, 6, i+1)
        ax.plot((0, px, qx, 0), (0, py, qy, 0), 'k', lw=3)
        ax.set_xlim((0, n))
        ax.set_ylim((0, n))
        ax.set_xticks(list(range(n + 1)))
        ax.set_yticks(list(range(n + 1)))
        ax.grid(True)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
    plt.tight_layout()
    plt.show()

# answer for n = 50 is 14234