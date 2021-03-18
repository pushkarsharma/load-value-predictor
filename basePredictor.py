from predictor import Predictor


class BasePredictor(Predictor):

    def __init__(self, history_length=1):
        super().__init__(history_length)

    def getPrediction(self, pc_address, load_address):
        load_values = self.history[pc_address][load_address]['load_values']
        if load_values:
            return load_values[-1]


if __name__ == '__main__':
    base_predictor = BasePredictor()
    total_loads, correct_count = 0, 0

    with open("pinatrace.txt") as fp:
        was_correct = True
        line = fp.readline()
        while line:
            total_loads += 1

            line_split = line.split()
            pc_address, load_address, actual_load_value = line_split[0], line_split[2], line_split[3]

            if base_predictor.checkIfExists(pc_address, load_address):
                prediction = base_predictor.getPrediction(
                    pc_address, load_address)
                if prediction == actual_load_value:
                    correct_count += 1
                    was_correct = True
                else:
                    was_correct = False

                base_predictor.addToHistory(
                    pc_address, load_address, actual_load_value, was_correct)
            else:
                base_predictor.addToHistory(
                    pc_address, load_address, actual_load_value, True)
            line = fp.readline()
        print('Base Accuracy : ', correct_count/total_loads)
