import timeit
from nim import train, play

def benchmark_choose_action(ai, state, num_iterations=100000, epsilon=False):
    """
    Benchmark the choose_action function using timeit.
    """
    def test_function():
        return ai.choose_action(state, epsilon=epsilon)
    
    # Run the benchmark
    total_time = timeit.timeit(test_function, number=num_iterations)
    
    print(f"Benchmarking choose_action with epsilon={epsilon}")
    print(f"Total time for {num_iterations} calls: {total_time:.6f} seconds")
    print(f"Average time per call: {total_time/num_iterations:.6f} seconds")
    print(f"Calls per second: {num_iterations/total_time:.2f}")
    print("-" * 50)
    
    return total_time

# Train the AI
ai = train(10000)

# Benchmark before playing
print("\nBenchmarking AI performance:")
print("=" * 50)
benchmark_choose_action(ai, [1, 3, 5, 7], num_iterations=100000, epsilon=False)
benchmark_choose_action(ai, [1, 3, 5, 7], num_iterations=100000, epsilon=True)

# Start the game
play(ai)