"""

Elastic collistions between 2 blocks and 1 wall.

|wall|______[b1]______<=v2=[b2]__

See the GUI in collisions_gui.py

"""


class Block:

    def __init__(self, m, v, x, a=1):
        self.m = m
        self.v = v
        self.x = x
        self.x1 = x
        self.a = a
    
    def q(self):
        return self.m * self.v

    def try_iterate(self, dt):
        self.x1 = self.x + self.v * dt

    def confirm_iterate(self):
        self.x = self.x1

    def hit_wall(self):
        self.v = -self.v


class System:
    def __init__(self, b1: Block, b2: Block):
        self.b1 = b1
        self.b2 = b2
        self.num_collisions = 0
        assert b2.m > b1.m 
        assert b2.x > b1.x

        self.num_iters = 0
        self.max_iters = 200_000
        self.t = 0.0
        self.eps = 1e-200
        self.dt = 0.1
        self.dt_iter = self.dt

        self.stats_func = lambda *args: None

    def q(self):
        return self.b1.q() + self.b2.q()

    def do_collision(self):
        # Elastic collision
        M = self.b1.m + self.b2.m
        DM = self.b1.m - self.b2.m
        v1 = DM / M * self.b1.v + 2 * self.b2.m / M * self.b2.v
        v2 = 2 * self.b1.m / M * self.b1.v - DM / M * self.b2.v
        self.b1.v = v1
        self.b2.v = v2

    def iterate(self):
    
        def gap12():
            return self.b2.x1 - self.b1.x1 - self.b1.a - self.b2.a
            
        def gap_wall():
            return self.b1.x1 - self.b1.a
            
        def block_collision_above_eps():
            gap = gap12()
            return gap < 0 and abs(gap) > self.eps
            
        def wall_collision_above_eps():
            # Check if collision  wall-b1 is outside tolerance:
            gap = gap_wall()
            return gap < 0 and abs(gap) > self.eps

        dt = self.dt

        self.b1.try_iterate(dt)
        self.b2.try_iterate(dt)
        
        collided = gap12() < self.eps

        while (collided and block_collision_above_eps()): 
            dt /= 2
            self.b1.try_iterate(dt)
            self.b2.try_iterate(dt)
            
        wall_hit = gap_wall() < self.eps

        while (wall_hit and wall_collision_above_eps()): 
            dt /= 2
            self.b1.try_iterate(dt)
            self.b2.try_iterate(dt)

        self.b1.confirm_iterate()
        self.b2.confirm_iterate()

        if collided:
            self.num_collisions += 1
            self.do_collision()
            
        if wall_hit:
            self.b1.hit_wall()

        self.t += dt
        self.dt_iter = dt

    def set_stats_func(self, func):
        """If set, performs some actions for every time step.
        `func` should have a `System` as the only argument.
        """
        self.stats_func = func

    def stop_simulation(self):
        return (
            self.b2.v >= abs(self.b1.v) or
            self.num_iters > self.max_iters
        )

    def loop(self):
        while not self.stop_simulation():
            self.stats_func(self)
            self.iterate()
            self.num_iters += 1
        self.stats_func(self)


def stats_draw_text(system: System):
    b1_to_wall = system.b1.x - system.b1.a
    b1_to_b2 = system.b2.x - system.b1.x - system.b1.a - system.b2.a
    print('|{}#{}#{}v1:{:.2f} v2:{:.2f} hits:{}     '.format(
        ' ' * int(10 * system.b1.x),
        ' ' * (int(10 * system.b2.x) - int(10 * system.b1.x)), 
        ' ' * (110 - int(10 * system.b2.x)),
        system.b1.v,
        system.b2.v,
        system.num_collisions,
        ), 
        end='\r'
    )

def stats_print_text(system: System):
    print(
        '=============>'
        f'{system.num_iters:15d}\t'
        f'{system.t:15.6f}\t'
        f'{system.dt_iter:15.6f}\t'
        f'{system.b1.x:15.6f}\t'
        f'{system.b1.v:15.6f}\t'
        f'{system.b2.x:15.6f}\t'
        f'{system.b2.v:15.6f}'
    )


def stats_save2file(system: System):
    with open('stats.txt', 'a') as f:
        f.write(f'{system.t:15.6f}\t{system.b1.x:15.6f}\t{system.b1.v:15.6f}'
                f'\t{system.b2.x:15.6f}\t{system.b2.v:15.6f}\n')


def main():

    b1 = Block(m=1, v=0, x=400, a=10)
    b2 = Block(m=99999, v=-0.5, x=550, a=15)
    sys = System(b1, b2)
    sys.set_stats_func(stats_save2file)
    sys.loop()


if __name__ == '__main__':
    main()