from abc import ABC, abstractmethod


class Predictor(ABC):

    def __init__(self, history_length=1):
        # self.history = {
        #     "pc_addr" : {
        #         "ld_addr" : {
        #             "load_values" : ["ld_val_1", "ld_val_2"],
        #             "confidence" : 0.6
        #         }
        #     }
        # }
        self.history = {}
        self.history_length = history_length

    @abstractmethod
    def getPrediction(self, pc_address, load_address):
        pass

    def updateLoadValue(self, pc_address, load_address, load_value):
        self.history[pc_address][load_address]['load_values'].append(
            load_value)
        self.history[pc_address][load_address]['load_values'] = self.history[pc_address][load_address]['load_values'][-self.history_length:]

    def checkIfExists(self, pc_address, load_address):
        if (pc_address in self.history) and (load_address in self.history[pc_address]):
            return True
        return False

    def updateConfidence(self, pc_address, load_address, was_correct):
        if was_correct:
            self.history[pc_address][load_address]['confidence'] += 0.2
            self.history[pc_address][load_address]['confidence'] = min(self.history[pc_address][load_address]['confidence'], 1)
        else:
            self.history[pc_address][load_address]['confidence'] -= 0.2
            self.history[pc_address][load_address]['confidence'] = max(self.history[pc_address][load_address]['confidence'], 0)

    def addToHistory(self, pc_address, load_address, load_value, was_correct):
        if not self.checkIfExists(pc_address, load_address):
            if pc_address not in self.history:
                self.history[pc_address] = {}

            self.history[pc_address][load_address] = {
                'load_values': [], 'confidence': 1}
            self.updateLoadValue(pc_address, load_address, load_value)
        else:
            self.updateLoadValue(pc_address, load_address, load_value)
            self.updateConfidence(pc_address, load_address, was_correct)
