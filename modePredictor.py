from predictor import Predictor
from statistics import mode

class ModePredictor(Predictor):

    def __init__(self, history_length=1):
        super().__init__(history_length)

    def getPrediction(self, pc_address, load_address):
        load_values = self.history[pc_address][load_address]['load_values']
        confidence = self.history[pc_address][load_address]['confidence']
        if load_values:
            return mode(load_values), confidence


if __name__ == '__main__':
    mode_predictor = ModePredictor(7)
    total_loads, correct_count = 0, 0

    with open("pinatrace.txt") as fp:
        was_correct = True
        line = fp.readline()
        while line:
            total_loads += 1

            line_split = line.split()
            pc_address, load_address, actual_load_value = line_split[0], line_split[2], line_split[3]

            if mode_predictor.checkIfExists(pc_address, load_address):
                prediction, confidence = mode_predictor.getPrediction(pc_address, load_address)
                if (prediction == actual_load_value and confidence >= 0.5) or (prediction != actual_load_value and confidence < 0.5):
                    correct_count += 1
                    was_correct = True
                else:
                    was_correct = False

                mode_predictor.addToHistory(pc_address, load_address, actual_load_value, was_correct)
            else:
                mode_predictor.addToHistory(pc_address, load_address, actual_load_value, True)
            line = fp.readline()
        print('Mode Accuracy : ', correct_count/total_loads)
