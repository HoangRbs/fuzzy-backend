# P = tap (n) BENH NHAN, S = tap (m) TRIEU CHUNG, D = tap (p) CHUAN DOAN BENH
import json


class fuzzyLogicElement:
    def __init__(self, U, N, V):
        self.U = U
        self.N = N
        self.V = V


P = 1  # P chuan doan benh (benh NHIEM TRUNG THAN)
N = 1  # N benh nhan
M = 11  # M trieu chung

# reading input.json
inputFile = open("input.json")
userSymtomsLevel = json.load(inputFile)
inputFile.close()

# Q ~~ PFS(P x S) # Q's datas will be read from input.json
Q = [
    [
        # fuzzyLogicElement(0.25, 0.05, 0.7),  # Abrupt Fever and chill
        # fuzzyLogicElement(0.75, 0.05, 0.2),  # Cloudy Urine
        # fuzzyLogicElement(0.75, 0.05, 0.2),  # Dysuria
        # fuzzyLogicElement(0.75, 0.05, 0.2),  # Hementuria
        # fuzzyLogicElement(0.75, 0.05, 0.2),  # Hesitancy
        # fuzzyLogicElement(0.75, 0.05, 0.2),  # Nausea and vomiting
        # fuzzyLogicElement(0.75, 0.05, 0.2),  # Nocturia
        # fuzzyLogicElement(0.25, 0.05, 0.7),  # Purulent Urine
        # fuzzyLogicElement(0.25, 0.05, 0.7),  # Suprapubic pain
        # # Flank pain umilateral or bilateral
        # fuzzyLogicElement(0.75, 0.05, 0.2),
        # fuzzyLogicElement(0.75, 0.05, 0.2)   # Urinary frequency
    ],
    # [],
    # []
]

# init datas for Q
for symtom in userSymtomsLevel:
    u = userSymtomsLevel[symtom]
    n = 0
    v = 0

    if u == 0:  # no
        n = 0
        v = 1
    elif u == 0.25:  # low
        n = 0.05
        v = 0.7
    elif u == 0.5:  # maybe
        n = 0
        v = 0.5
    elif u == 0.75:  # high
        n = 0.05
        v = 0.2
    elif u == 1:  # extra high
        n = 0
        v = 0

    Q[0].append(fuzzyLogicElement(u, n, v))


# R ~~ PFS(D x S)
R = [
    [
        fuzzyLogicElement(0.5, 0.05, 0.4),
        fuzzyLogicElement(0.8, 0.05, 0.1),
        fuzzyLogicElement(0.7, 0.05, 0.2),
        fuzzyLogicElement(0.75, 0.05, 0.15),
        fuzzyLogicElement(0.95, 0, 0.05),
        fuzzyLogicElement(0.6, 0.05, 0.3),
        fuzzyLogicElement(0.65, 0.05, 0.25),
        fuzzyLogicElement(0.6, 0.05, 0.25),
        fuzzyLogicElement(0.75, 0.05, 0.2),
        fuzzyLogicElement(0.55, 0.05, 0.35),
        fuzzyLogicElement(0.75, 0.05, 0.15),
    ],
    # [],
    # []
]

# S_T ~~ PFS(P * D)
# initialize S_T
S_T = []
for j in range(N):
    S_T.append([])

# SUY DIEN MO

for i in range(P):
    for j in range(N):

        # calulate U_T ~~ max(min())
        tempArr = []
        for k in range(M):
            tempArr.append(min(Q[j][k].U, R[i][k].U))

        global U_T
        U_T = tempArr[0]

        for k in range(len(tempArr)):
            if tempArr[k] > U_T:
                U_T = tempArr[k]

        # calulate N_T ~~ min(min())
        tempArr = []

        for k in range(M):
            tempArr.append(min(Q[j][k].N, R[i][k].N))

        global N_T
        N_T = tempArr[0]

        for k in range(len(tempArr)):
            if tempArr[k] < N_T:
                N_T = tempArr[k]

        # calulate V_T ~~ min(max())
        tempArr = []
        for k in range(M):
            tempArr.append(max(Q[j][k].V, R[i][k].V))

        global V_T
        V_T = tempArr[0]

        for k in range(len(tempArr)):
            if tempArr[k] < V_T:
                V_T = tempArr[k]

        # T = Q o R
        # khu mo
        S_T_result = U_T - V_T * (1 - (U_T + N_T + V_T))

        # save data into S_T table
        S_T[j].append(S_T_result)

outputFile = open("output.txt", "w")

result = ""

# write datas to output.json
for j in range(N):  # 1 person
    for i in range(P):  # 1 desease
        result = "{}".format(
            round(S_T[j][i], 2)
        )

outputFile.write(result)
outputFile.close()
