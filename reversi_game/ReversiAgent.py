import tensorflow as tf
import numpy as np

class ReversiAgent:
    def __init__(self, Q=None):
        if Q is None:
            self._Q = self.__createmodel__()
        else:
            self._Q = tf.keras.models.clone_model(Q)
            self._Q.set_weights(Q.get_weights())


    def get_next_move(self, state, epsilon):
        if np.random.random() < epsilon:
            return np.random.choice(64)
        else:
            return np.argmax(self.get_move_values(state))


    def get_move_values(self, state):
        return self._Q.predict(self.__processtate__(state)).reshape((64,))


    def __processtate__(self, state):
        return state.reshape((-1, 8, 8, 1))


    def __createmodel__(self):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Conv2D(16, (2,2), input_shape=(8,8,1)))
        model.add(tf.keras.layers.Conv2D(8, (4,4)))
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(128, activation='relu'))
        model.add(tf.keras.layers.Dense(256, activation='relu'))
        model.add(tf.keras.layers.Dense(64))

        model.compile(optimizer='adam', loss='mse')

        return model

