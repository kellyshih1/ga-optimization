import sys
import random, math

class binary_ga:
    def __init__(self, config):
        self.config = config
    
    def crossover(self, parent1, parent2):
        # get random number, do crossover if less than self.config.cross_prob
        if random.random() < self.config.cross_prob:
            if self.config.uniform_crossover:
                # do uniform crossover
                child1 = []
                child2 = []
                for i in range(len(parent1)):
                    if random.random() < 0.5:
                        child1.append(parent1[i])
                        child2.append(parent2[i])
                    else:
                        child1.append(parent2[i])
                        child2.append(parent1[i])
                return child1, child2
            else: 
                # two point crossover
                # pick two random points p1, p2 from [1, self.config.dimension * 10] where p1 < p2
                p1, p2 = sorted(random.sample(range(1, len(parent1)), 2))

                child1 = parent1[0:p1] + parent2[p1:p2] + parent1[p2:]
                child2 = parent2[0:p1] + parent1[p1:p2] + parent2[p2:]
                return child1, child2
        else:
            return parent1[:], parent2[:]
    
    def mutate(self, individual):
        mutated_ind = []
        for bit in individual:
            if random.random() < self.config.mut_prob:
                mutated_ind.append('1' if bit == '0' else '0')
            else:
                mutated_ind.append(bit)
        return mutated_ind

    def evaluate_fitness(self, individual):
        def bits_to_int(b):
            bits = len(b)
            val = int(b, 2)
            if b[0] == '1':  
                val -= 1 << bits
            return val

        decoded = []
        for i in range(self.config.dimension):
            gene = individual[i*10:(i+1)*10]
            integer_value = ''.join(gene)
            real_value = bits_to_int(integer_value)
            decoded.append(real_value)
        
        # schwefel 
        ans = self.config.dimension * 418.98291
        for x in decoded:
            ans -= x * (math.sin((abs(x)) ** 0.5))
        return ans
    
    def select_parents(self, population):
        parent_pop = [] 
        k = self.config.tournament_size
        # make parent population (size = population size)
        for _ in range(len(population)): 
            t = random.sample(population, k)
            # sort by fitness, small to large (better fitness to worse fitness)
            t.sort(key=lambda x: self.evaluate_fitness(x)) 
            parent_pop.append(t[0])  # append the best individual
        return parent_pop
    
    def initialize_population(self):
        pop = [] 
        for _ in range(self.config.population_size):
            individual = []
            for _ in range(self.config.dimension * 10):
                # pick a random bit
                individual.append(random.choice(['0', '1']))
            pop.append(individual)
        return pop
    
    def run(self):
        population = self.initialize_population()

        for gen_num in range(self.config.num_generations):
            # print best fitness in current population
            # if gen_num % 50 == 0:
            #     best_fitness = min([self.evaluate_fitness(ind) for ind in population])
            #     print(f"Generation {gen_num}, Best Fitness: {best_fitness}")
            
            # select parents
            parent_pop = self.select_parents(population)
            child_pop = [] 
            # shuffle parents
            random.shuffle(parent_pop)

            # create offspring, each pair of parents create 2 children
            for j in range(0, len(parent_pop)-1, 2):
                parent1 = parent_pop[j]
                parent2 = parent_pop[j+1]
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                child_pop.append(child1)
                child_pop.append(child2)

            # select next generation 
            # combine population and children, select best individuals
            pooled = population + child_pop
            pooled.sort(key=lambda x: self.evaluate_fitness(x))

            # update the population
            population = pooled[:self.config.population_size]
        
        final_fitness = min(self.evaluate_fitness(ind) for ind in population)
        return final_fitness

class real_ga: 
    def __init__(self, config):
        self.config = config

    def crossover(self, parent1, parent2):
        # get random number, do crossover if less than self.config.cross_prob
        if random.random() < self.config.cross_prob:
            if self.config.uniform_crossover:
                # do uniform crossover
                child1 = []
                child2 = []
                for i in range(len(parent1)):
                    if random.random() < 0.5:
                        child1.append(parent1[i])
                        child2.append(parent2[i])
                    else:
                        child1.append(parent2[i])
                        child2.append(parent1[i])
                return child1, child2
            else: 
                # using whole arithmetic 
                alpha = 0.2
                child1 = []
                child2 = []
                for i in range(len(parent1)):
                    c1 = alpha * parent1[i] + (1 - alpha) * parent2[i]
                    c2 = (1 - alpha) * parent1[i] + alpha * parent2[i]
                    child1.append(c1)
                    child2.append(c2)
                return child1, child2
        else:
            return parent1[:], parent2[:]
        
    def mutate(self, individual):
        mutated_ind = []
        for i in range(len(individual)):
            if random.random() < self.config.mut_prob:
                mutated_ind.append(random.uniform(-512, 511))
            else:
                mutated_ind.append(individual[i])
        return mutated_ind
    
    def evaluate_fitness(self, individual):
        # schwefel 
        ans = self.config.dimension * 418.98291
        for x in individual:
            ans -= x * (math.sin((abs(x)) ** 0.5))
        return ans
    
    def select_parents(self, population):
        parent_pop = [] 
        k = self.config.tournament_size
        # make parent population (size = population size)
        for _ in range(len(population)): 
            t = random.sample(population, k)
            # sort by fitness, small to large (better fitness to worse fitness)
            t.sort(key=lambda x: self.evaluate_fitness(x)) 
            parent_pop.append(t[0])  # append the best individual
        return parent_pop
        
    def initialize_population(self):
        pop = [] 
        for _ in range(self.config.population_size):
            individual = []
            for _ in range(self.config.dimension):
                # pick a random real number between [-512, 511]
                individual.append(random.uniform(-512, 511))
            pop.append(individual)
        return pop 

    def run(self):
        population = self.initialize_population()

        for gen_num in range(self.config.num_generations):
            # print best fitness in current population
            # if gen_num % 50 == 0:
            #     best_fitness = min([self.evaluate_fitness(ind) for ind in population])
            #     print(f"Generation {gen_num}, Best Fitness: {best_fitness}")
            
            # select parents
            parent_pop = self.select_parents(population)
            child_pop = [] 
            # shuffle parents
            random.shuffle(parent_pop)

            # create offspring, each pair of parents create 2 children
            for j in range(0, len(parent_pop)-1, 2):
                parent1 = parent_pop[j]
                parent2 = parent_pop[j+1]
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                child_pop.append(child1)
                child_pop.append(child2)

            # select next generation 
            # combine population and children, select best individuals
            pooled = population + child_pop
            pooled.sort(key=lambda x: self.evaluate_fitness(x))

            # update the population
            population = pooled[:self.config.population_size]
        
        final_fitness = min(self.evaluate_fitness(ind) for ind in population)
        return final_fitness

            
def ga(config):
    if config.representation == 'real':
        algorithm = real_ga(config)
        res = algorithm.run()
        print(res)
    else: 
        algorithm = binary_ga(config)
        res = algorithm.run()
        print(res)
    return