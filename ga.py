from neural import NeuralNetwork as NN
import random


#Defining individual SpaceCraft object property
class Individual:
    def __init__(self):
        self.fitness = 0
        self.individual_obj = NN()
        self.score = 0

class Population:

    def __init__(self):
        #Setting initial population size
        self.popSize = 9

        #Creating a list to contain SpaceCraft objects
        self.objects = list()

        #Setting the fit SpaceCraft object size to be taken for selection
        self.fit_size_population = 6

        #Creating objects and appending them to the list
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

        #Deleting the objects that are not taken into selection ( i.e index from 6 to last)
        del self.objects[self.fit_size_population:size_of_list]
        self.popSize = self.fit_size_population

    #Defining the crossover function
    def crossover(self):

        for i in range(self.popSize):

            #Creating an object with values same as i-th index in object list
            temp_obj_1 = Individual()
            temp_obj_1.fitness = self.objects[i].fitness
            temp_obj_1.score = self.objects[i].score
            temp_obj_1.individual_obj = self.objects[i].individual_obj

            for j in range(i+1,self.popSize):

                #Creating an object with values same as j-th index in object list
                temp_obj_2 = Individual()
                temp_obj_2.fitness = self.objects[j].fitness
                temp_obj_2.score = self.objects[j].score
                temp_obj_2.individual_obj = self.objects[j].individual_obj

                #Swapping the bias of both the newly created objects
                temp = temp_obj_1.individual_obj.bias[0]
                temp_obj_1.individual_obj.bias[0] = temp_obj_2.individual_obj.bias[0]
                temp_obj_2.individual_obj.bias[0] = temp

                #Appending the objects to the objects list
                self.objects.append(temp_obj_1)
                self.objects.append(temp_obj_2)

        #Setting the new size of object list  and setting the fitness and score to 0
        size_of_list = len(self.objects)
        self.popSize = size_of_list

        for i in range(self.popSize):
            self.objects[i].fitness = 0
            self.objects[i].score = 0

    #Defining mutation functions
    """
    In it , we are checking whether we have to do mutation or not.
    So, for it , we are checking the probability through random function.
    If the value of rand is 1 , then we are updating the value of weight[0]
    """
    def mutation(self):
        for i in range(self.popSize):
            rand = random.random()
            if rand == 1:
                self.objects[i].individual_obj.weights[0] = random.random()


t = Population()
t.selection()
t.crossover()
t.mutation()
t.display()
