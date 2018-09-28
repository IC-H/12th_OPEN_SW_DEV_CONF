from django.core.management.base import BaseCommand, CommandError
from batch.learning import DeepLearner

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        try:
            nn = DeepLearner(
               	input_dim = 5,
                n_layer1 = 10,
                n_layer2 = 10,
                learning_rate = 0.1)

            nn.learning(
                X_train = X_train,  ###
                Y_train = Y_train,  ###
                dropout_prob = 0.7,
                n_try = 100, 
                batch_size = 32)

            nn.get_result(X_test, Y_test)
            ### nn.get_fitted_value(X_test, Y_test)

        except CommandError as e:
            print(e)