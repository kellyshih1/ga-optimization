# 🧬 Genetic Algorithm for the Schwefel Function Optimization

This project implements a **Genetic Algorithm (GA)** for optimizing the **Schwefel function**, using both **binary** and **real-valued** representations.  
It includes modular, object-oriented implementations of all core GA components — including initialization, selection, crossover, mutation, and survivor selection.

---

## 📘 Overview

The program provides two GA variants:
1. **Binary GA** – Each variable is encoded as a 10-bit binary string, later converted to an integer in two’s complement format.  
2. **Real-Valued GA** – Each variable is represented directly as a floating-point number within a specified range.

Both variants share a similar structure, differing only in how individuals are represented and manipulated.

The algorithm evolves a population of candidate solutions through several generations to minimize the Schwefel function:

\[
f(\vec{x}) = 418.98291N - \sum_{i=1}^N x_i \sin(\sqrt{|x_i|})
\]

---

## 🧩 Implementation Details

### **1. Structure**
The project defines **two main classes**:
- `BinaryGA` – handles encoding, decoding, and binary-specific operations.
- `RealGA` – handles real-number representations and arithmetic operations.

Each class includes:
- `initialize_population()` – random population generation  
- `evaluate_fitness()` – computes Schwefel fitness  
- `select_parents()` – tournament selection  
- `crossover()` – uniform or two-point (binary) / uniform or arithmetic (real)  
- `mutate()` – bit-flip or random reset mutation  
- `run()` – main loop controlling the evolutionary process  

---

### **2. Operators**

| Operator | Binary GA | Real-Valued GA |
|-----------|------------|----------------|
| **Initialization** | Random 0/1 for each bit | Random float in [-512, 511] |
| **Parent Selection** | Tournament selection (size *k*) | Tournament selection (size *k*) |
| **Crossover** | Uniform / Two-point | Uniform / Whole arithmetic |
| **Mutation** | Bit-flip | Random reset |
| **Fitness** | Schwefel (via decoded integers) | Schwefel (directly) |
| **Survivor Selection** | μ + λ elitism (top *p* retained) | μ + λ elitism (top *p* retained) |

---

### **3. Population Model**

At each generation:
1. A **parent population** of size *p* is selected using tournament selection.
2. Parents are shuffled, then paired to produce children via crossover.
3. Children are mutated and evaluated.
4. The new population is formed by selecting the best *p* individuals from parents and offspring.
5. After *g* generations, the best individual is reported.

---

## ⚙️ Usage

### **Command-line Parameters**
Typical arguments include:
- `--representation` → `"binary"` or `"real"`
- `--population-size` → number of individuals *p*
- `--generations` → number of iterations *g*
- `--pc` → crossover probability
- `--pm` → mutation probability
- `--k` → tournament size

### **Example Run**
```bash
python main.py -n 10 -r binary -p 100 -u 0 -c 0.9 -m 0.1 -g 500
