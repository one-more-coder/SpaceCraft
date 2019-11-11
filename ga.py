from neural import NeuralNetwork as NN

class Individual:
    def __init__(self):
        self.fitness = 0
        self.individual_obj = NN()
        self.score = 0

class Population:

    def __init__(self):
        self.popSize = 9
        self.objects = list()
        self.fit_size_population = 6
        for i in range(self.popSize):
            self.objects.append(Individual())
            self.objects[i].fitness = i

    #Sorting the objects in the descending order of fitness value
    def sorting(self):
        self.objects.sort(key = lambda x: x.fitness, reverse = True)

    #Displaying the fitness score of individual objects
    def display(self):
        for i in range(self.popSize):
            print(self.objects[i].fitness)

   # <-------------Defining Genetic Algorithm---------------->

    #Taking only 6 fittest objects and deleting others
    def fitness_function(self):
        self.sorting()
        size_of_list = len(self.objects)
        del self.objects[self.fit_size_population:size_of_list]
        self.popSize = self.fit_size_population


t = Population()
t.fitness_function()
t.display()
