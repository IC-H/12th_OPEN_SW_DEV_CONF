from django.core.management.base import BaseCommand, CommandError
from batch.learning import DeepLearner
import numpy as np

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        try:
            nn = DeepLearner(
                input_dim = 2,
                n_layer1 = 50,
                n_layer2 = 50,
                learning_rate = 0.001)

            nn.teach(
                X_train = np.array([[0, 0], [1, 0], [0, 1], [1, 1]]),  ###
                Y_train = np.array([[0], [1], [1], [0]]),  ###
                dropout_prob = 1.0,
                n_try = 100, 
                batch_size = 16)

            print('result')
            nn.get_result()
            nn.get_fitted_value(np.array([[0, 0], [1, 0], [0, 1], [1, 1]]))

        except CommandError as e:
            print(e)