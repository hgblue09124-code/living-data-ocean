"""
Tệp đo đạc hiệu năng (Benchmark) đo thời gian thực thi của các hot paths trong Underworld v0.
"""

import time
import unittest
from underworld.composition import World, Human
from underworld.runtime import EventLoop


class TestBenchmark(unittest.TestCase):
    """Đo đạc và đánh giá hiệu năng các hot paths trong thế giới mô phỏng."""

    def test_benchmark_tick_and_snapshot_performance(self):
        """Đo thời gian thực thi 1000 bước tick(), 1000 lần get_state() và 1000 bước EventLoop."""
        world = World(seed=42)
        world.add_human(Human("H1", position=(0, 0)))
        world.add_human(Human("H2", position=(1, 1)))
        world.add_human(Human("H3", position=(10, 10)))

        # 1. Benchmark World.tick()
        start_tick = time.perf_counter()
        for _ in range(1000):
            world.tick()
        end_tick = time.perf_counter()
        elapsed_tick = end_tick - start_tick

        # 2. Benchmark World.get_state() Snapshot creation
        start_snapshot = time.perf_counter()
        for _ in range(1000):
            world.get_state()
        end_snapshot = time.perf_counter()
        elapsed_snapshot = end_snapshot - start_snapshot

        # 3. Benchmark EventLoop run
        world_loop = World(seed=42)
        world_loop.add_human(Human("H1", position=(0, 0)))
        world_loop.add_human(Human("H2", position=(1, 1)))
        event_loop = EventLoop(world_loop)

        start_loop = time.perf_counter()
        trajectory = event_loop.run(steps=1000)
        end_loop = time.perf_counter()
        elapsed_loop = end_loop - start_loop

        print("\n============================================================")
        print("                  UNDERWORLD BENCHMARK RESULTS")
        print("============================================================")
        print(f"  - 1000 bước World.tick():           {elapsed_tick:.4f} giây ({elapsed_tick / 1000 * 1000:.3f} ms/tick)")
        print(f"  - 1000 lần World.get_state():        {elapsed_snapshot:.4f} giây ({elapsed_snapshot / 1000 * 1000:.3f} ms/snapshot)")
        print(f"  - 1000 bước EventLoop.run():         {elapsed_loop:.4f} giây ({elapsed_loop / 1000 * 1000:.3f} ms/step)")
        print("============================================================\n")

        self.assertLess(elapsed_tick, 3.0)
        self.assertLess(elapsed_loop, 4.0)
        self.assertEqual(len(trajectory.steps), 1000)


if __name__ == "__main__":
    unittest.main()
