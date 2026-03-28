class LamportClock:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1
        return self.value

    def update(self, received_time):
        self.value = max(self.value, received_time) + 1
        return self.value