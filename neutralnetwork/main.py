import numpy as np

class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes
        
        # Gewichten initialiseren
        self.input_to_hidden_weights = np.random.rand(self.input_nodes, self.hidden_nodes)
        self.hidden_to_output_weights = np.random.rand(self.hidden_nodes, self.output_nodes)

    def tanh(self, x):
        return np.tanh(x)

    def feedforward(self, input_data):
        # Berekenen van de input naar de hidden layer
        hidden_input = np.dot(input_data, self.input_to_hidden_weights)
        """
        input_data
        [0, 0, 1, 0]

        input_to_hidden_weights
            [[0.84388801, 0.59878285, 0.65012619, 0.08908922],
            [0.11843478, 0.2165329 , 0.50980027, 0.42884881],
            [0.59116486, 0.87328584, 0.72923639, 0.52626971],
            [0.78402765, 0.16742232, 0.33995742, 0.11067888]]

        (0.84388801 * 0) + (0.11843478 * 0) + (0.59116486 * 1) + (0.78402765 * 0) = 0.59116486
        En dit dan per rij.


        
        """

        # Normalizeren van waardes tussen 0 - 1
        hidden_output = self.tanh(hidden_input)

        # Berekenen van de hidden layer naar de output
        output_input = np.dot(hidden_output, self.hidden_to_output_weights)

        """
        hidden output: [0.9141156 , 0.93345543, 0.95478578, 0.77924138]
        hiddentooutput: [0.17660043],[0.37260424], [0.62243381],[0.09585225]
                                                                             KEER elkaar, dus:
        0.9141156 * 0.17660043 + 0.93345543 * 0.37260424 + 0.95478578 * 0.62243381 + 0.77924138 * 0.09585225 = 1.17822565
        """

        output = self.tanh(output_input)
        
        return output

    def train(self, training_data, training_labels, epochs, learning_rate):
        for epoch in range(epochs):
            for input_data, label in zip(training_data, training_labels):
                # Stap 3: Feedforward
                output = self.feedforward(input_data)
                
                # Stap 4: Bereken de fout
                error = label - output
                
                # Stap 5: Pas de gewichten aan
                self.adjust_weights(input_data, output, error, learning_rate)

    def adjust_weights(self, input_data, output, error, learning_rate):
        # Stap 1: Bereken de aanpassingen voor de gewichten van de verborgen laag naar de outputlaag

        # Bereken de gradient van de outputlaag, hoe goed is de output?
        output_gradient = error * output * (1 - output)

        # Bereken de delta voor de gewichten van de verborgen laag naar de outputlaag
        # Berekent hoe de fout in de outputlaag wordt teruggevoerd naar de verborgen laag
        delta_hidden_to_output_temp = np.dot(output_gradient * self.hidden_to_output_weights.T, self.tanh(np.dot(input_data, self.input_to_hidden_weights)))

        # Pas learning rate toe, vaak kleine marge
        delta_hidden_to_output = learning_rate * delta_hidden_to_output_temp.T

        # Stap 2: Bereken de aanpassingen voor de gewichten van de inputlaag naar de verborgen laag

        # Bereken de gradient van de verborgen laag
        hidden_gradient = output_gradient * self.hidden_to_output_weights.T * self.tanh(np.dot(input_data, self.input_to_hidden_weights))

        # Bereken de delta voor de gewichten van de inputlaag naar de verborgen laag
        delta_input_to_hidden = learning_rate * np.dot(input_data.reshape(-1, 1), hidden_gradient.reshape(1, -1))

        # Stap 3: Pas de gewichten aan

        # Pas de gewichten van de inputlaag naar de verborgen laag aan
        self.input_to_hidden_weights += delta_input_to_hidden

        # Pas de gewichten van de verborgen laag naar de outputlaag aan
        self.hidden_to_output_weights += delta_hidden_to_output


# Voorbeeld training data (input en output)
training_data = np.array([[0, 0, 1, 0], [1, 1, 1, 0], [1, 0, 1, 1], [0, 1, 1, 1]])
training_labels = np.array([[0], [1], [1], [0]])

# Stap 1: Maak een instantie van NeuralNetwork
nn = NeuralNetwork(input_nodes=4, hidden_nodes=4, output_nodes=1)

# Stap 6: Train het netwerk
epochs = 50000
learning_rate = 0.1
nn.train(training_data, training_labels, epochs, learning_rate)

# Test het getrainde netwerk met alle inputdata
for input_data, label in zip(training_data, training_labels):
    predicted_output = nn.feedforward(input_data)
    print("Input:", input_data, "Correct output:", label[0], "Predicted output:", predicted_output)


