import threading
import queue

# Define the base class Actor which all specific actors will inherit from
class Actor:
    def __init__(self):
        # Initialize a thread-safe queue for messages and a flag for actor's active state
        self.messages = queue.Queue()
        self.alive = True
        # Setup the thread for running the actor; set as daemon to close on program exit
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    # Method to send messages to the actor's queue
    def send(self, message, value):
        self.messages.put((message, value))

    # The main loop of the actor that processes messages as long as the actor is alive
    def run(self):
        while self.alive:
            message, value = self.messages.get()
            self.handle_message(message, value)

    # Placeholder method to handle messages, must be overridden by subclass
    def handle_message(self, message, value):
        raise NotImplementedError("This method should be overridden by subclasses.")

    # Method to stop the actor's processing loop and ensure the thread finishes cleanly
    def stop(self):
        self.alive = False
        self.thread.join()

# NumericActor subclass for handling numeric specific tasks
class NumericActor(Actor):
    def __init__(self):
        super().__init__()
        # Start with number set to zero
        self.number = 0

    # Implementation of handling messages for storing and modifying numeric values
    def handle_message(self, message, value):
        if message == "store":
            self.number = value
        elif message == "add":
            self.number += value
        elif message == "subtract":
            self.number -= value
        print(f"NumericActor: Current Value is {self.number}")

# StringActor subclass for handling string specific tasks
class StringActor(Actor):
    def __init__(self):
        super().__init__()
        # Start with an empty text
        self.text = ""

    # Implementation of handling messages for storing and appending strings
    def handle_message(self, message, value):
        if message == "store":
            self.text = value
        elif message == "concat":
            self.text += value
        print(f"StringActor: Current String is '{self.text}'")

# SpawnerActor subclass for creating new actors
class SpawnerActor(Actor):
    def handle_message(self, message, value):
        if message == "spawn":
            # Spawn the specified number of NumericActors and initialize them
            for i in range(value):
                new_actor = NumericActor()
                new_actor.send("store", i)
                print(f"SpawnerActor: Spawned NumericActor with initial value {i}")

# Main section to test the functionality of the actors
if __name__ == "__main__":
    # Create and test NumericActor
    num_actor = NumericActor()
    num_actor.send("store", 10)
    num_actor.send("add", 5)
    num_actor.send("subtract", 3)

    # Create and test StringActor
    str_actor = StringActor()
    str_actor.send("store", "Hello")
    str_actor.send("concat", " World")

    # Create and test SpawnerActor
    spawn_actor = SpawnerActor()
    spawn_actor.send("spawn", 3)

    # Wait for input to allow time for all messages to be processed
    input("Press Enter to stop actors...")

    # Stop all actors
    num_actor.stop()
    str_actor.stop()
    spawn_actor.stop()
