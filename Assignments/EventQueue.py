from queue import PriorityQueue

class EventQueue:
    def __init__(self):
        # Initialize a priority queue to manage events by their time
        self.events = PriorityQueue()

    def add_event(self, event):
        # Add an event to the priority queue
        self.events.put(event)

    def get_next_event(self):
        # Get the next event if the queue is not empty, otherwise return None
        if not self.events.empty():
            return self.events.get()
        return None

    def has_more_events(self):
        # Check if there are more events to process
        return not self.events.empty()

    def process_events(self):
        # Process events in the queue until no more remain
        while self.has_more_events():
            event = self.get_next_event()
            event.process(self)  # Process the event and pass the event queue
