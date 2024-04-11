import threading
from actor_model import NumericActor, StringActor, SpawnerActor

# Function to test the system's ability to handle a high volume of messages efficiently
def test_high_message_volume():
    print("Testing high message volume...")
    num_actor = NumericActor()  # Create an instance of NumericActor
    for i in range(1000):  # Send a large number of messages
        num_actor.send("add", 1)  # Each message instructs the actor to add 1 to its internal state
    threading.Event().wait(2)  # Allow some time for all messages to be processed
    num_actor.stop()  # Stop the actor to clean up the thread

# Function to test the system's ability to spawn multiple actors simultaneously
def test_simultaneous_spawning():
    print("Testing simultaneous actor spawning...")
    spawner = SpawnerActor()  # Create an instance of SpawnerActor
    spawner.send("spawn", 10)  # Send a message to spawn 10 new actors
    threading.Event().wait(1)  # Allow some time for the actors to be spawned and start processing
    spawner.stop()  # Stop the spawner actor to clean up the thread

# Function to test how the system handles unexpected or undefined message types
def test_unexpected_message():
    print("Testing handling of unexpected message types...")
    num_actor = NumericActor()  # Create an instance of NumericActor
    num_actor.send("undefined", 999)  # Send an undefined message type with some arbitrary value
    threading.Event().wait(1)  # Allow some time to see if the actor handles or ignores the message
    num_actor.stop()  # Stop the actor, which should also handle cleaning up the thread

# Main block to execute the tests
if __name__ == "__main__":
    test_high_message_volume()  # Execute the high message volume test
    test_simultaneous_spawning()  # Execute the simultaneous actor spawning test
    test_unexpected_message()  # Execute the test for handling unexpected messages
