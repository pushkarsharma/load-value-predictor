import argparse

from randomPredictor import RandomPredictor
from medianPredictor import MedianPredictor
from basePredictor import BasePredictor
from modePredictor import ModePredictor

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Local Value Predictor')
    parser.add_argument('--history', type=int, help="history length", choices=range(2, 21), default=7)
    arguments = parser.parse_args()

    base_predictor = BasePredictor()
    mode_predictor = ModePredictor(arguments.history)
    median_predictor = MedianPredictor(arguments.history)
    random_predictor = RandomPredictor(arguments.history)

    with open("pinatrace.txt") as fp:
        total_loads = 0
        base_correct_count, mode_correct_count, median_correct_count, random_correct_count = 0, 0, 0, 0
        base_was_correct, mode_was_correct, median_was_correct, random_was_correct = True, True, True, True

        line = fp.readline()
        while line:
            total_loads += 1

            line_split = line.split()
            pc_address, load_address, actual_load_value = line_split[0], line_split[2], line_split[3]

            if base_predictor.checkIfExists(pc_address, load_address):
                base_prediction = base_predictor.getPrediction(pc_address, load_address)
                mode_prediction, mode_confidence = mode_predictor.getPrediction(pc_address, load_address)
                median_prediction, median_confidence = median_predictor.getPrediction(pc_address, load_address)
                random_prediction, random_confidence = random_predictor.getPrediction(pc_address, load_address)

                if base_prediction == actual_load_value:
                    base_correct_count += 1
                    base_was_correct = True
                else:
                    base_was_correct = False

                if (mode_prediction == actual_load_value and mode_confidence >= 0.5) or (mode_prediction != actual_load_value and mode_confidence < 0.5):
                    mode_correct_count += 1
                    mode_was_correct = True
                else:
                    mode_was_correct = False

                if (median_prediction == actual_load_value and median_confidence >= 0.5) or (median_prediction != actual_load_value and median_confidence < 0.5):
                    median_correct_count += 1
                    median_was_correct = True
                else:
                    median_was_correct = False

                if (random_prediction == actual_load_value and random_confidence >= 0.5) or (random_prediction != actual_load_value and random_confidence < 0.5):
                    random_correct_count += 1
                    random_was_correct = True
                else:
                    random_was_correct = False

                base_predictor.addToHistory(pc_address, load_address, actual_load_value, base_was_correct)
                mode_predictor.addToHistory(pc_address, load_address, actual_load_value, mode_was_correct)
                median_predictor.addToHistory(pc_address, load_address, actual_load_value, median_was_correct)
                random_predictor.addToHistory(pc_address, load_address, actual_load_value, random_was_correct)
            else:
                base_predictor.addToHistory(pc_address, load_address, actual_load_value, True)
                mode_predictor.addToHistory(pc_address, load_address, actual_load_value, True)
                median_predictor.addToHistory(pc_address, load_address, actual_load_value, True)
                random_predictor.addToHistory(pc_address, load_address, actual_load_value, True)

            line = fp.readline()

        base_accuracy = ((base_correct_count)/total_loads) * 100
        mode_accuracy = ((mode_correct_count)/total_loads) * 100
        median_accuracy = ((median_correct_count)/total_loads) * 100
        random_accuracy = ((random_correct_count)/total_loads) * 100
        
        print()
        print('Base Accuracy : ', round(base_accuracy, 4), '%')
        print('Mode Accuracy : ', round(mode_accuracy, 4), '%')
        print('Median Accuracy : ', round(median_accuracy, 4), '%')
        print('Random Accuracy : ', round(random_accuracy, 4), '%')
        print()