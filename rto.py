"""rto.py: retransmission timeout estimators. Owner: Archit."""


class FixedRTO:
    def __init__(self, timeout=0.2):
        self.initial = timeout
        self.timeout = timeout

    def value(self):
        return self.timeout

    def sample(self, rtt, resent):
        pass

    def backoff(self):
        self.timeout = min(60.0, self.timeout * 2)

    def forward(self):
        self.timeout = self.initial


Fixed = FixedRTO
