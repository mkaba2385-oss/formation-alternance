import numpy as np

a = np.random.randint(0, 101, 100)

print(f"Moyenne: {np.mean(a)}, Médiane: {np.median(a)}, Ecart-type: {np.std(a):.2f}")


#

i = np.arange(5)
j = np.arange(5)

matrice = i[:, np.newaxis] * j

print(matrice)


#

de = np.random.randint(1, 7, 1000)
for face in range(1, 7):
    print(f"{face} : {np.sum(de == face)}")

# 

b = np.random.randint(-10,10, (10,10))

b[b < 0] =0
print(b)