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
        print("size of list = " + str(len(self.objects)) + "\n")
        for i in range(self.popSize):
            print(self.objects[i].fitness)

   # <-------------Defining Genetic Algorithm---------------->

    #Selecting only 6 fittest objects and deleting others
    def selection(self):
        self.sorting()
        size_of_list = len(self.objects)
        del self.objects[self.fit_size_population:size_of_list]
        self.popSize = self.fit_size_population

    #Defining the crossover function
    def crossover(self):

        for i in range(self.popSize):

            temp_obj_1 = Individual()
            temp_obj_1.fitness = self.objects[i].fitness
            temp_obj_1.score = self.objects[i].score
            temp_obj_1.individual_obj = self.objects[i].individual_obj

            for j in range(i+1,self.popSize):

                temp_obj_2 = Individual()
                temp_obj_2.fitness = self.objects[j].fitness
                temp_obj_2.score = self.objects[j].score
                temp_obj_2.individual_obj = self.objects[j].individual_obj

                temp = temp_obj_1.individual_obj.bias[0]
                temp_obj_1.individual_obj.bias[0] = temp_obj_2.individual_obj.bias[0]
                temp_obj_2.individual_obj.bias[0] = temp

                self.objects.append(temp_obj_1)
                self.objects.append(temp_obj_2)

        size_of_list = len(self.objects)
        self.popSize = size_of_list

        for i in range(self.popSize):
            self.objects[i].fitness = 0
            self.objects[i].score = 0


t = Population()
t.selection()
t.crossover()
t.display()
