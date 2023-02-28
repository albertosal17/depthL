import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
import os
import json
import sys

from quantumCircuit import iteration
from qiskit import QuantumCircuit, transpile

from qiskit import IBMQ
IBMQ.load_account()             
provider = IBMQ.get_provider(hub='ibm-q-research', group='uni-south-cali-1', project='main')

def depth(backend):


    directory='C:\\Users\\ASUS\\Desktop\\TESI\\data\\test\\'
       
    backends=['noiseless',backend]

    if (backend=="lima"):
        qubits = [3,4,5]
    elif(backend=="guadalupe"):
        qubits = [3,4,5,7,10]

    curva = {}

    for n in qubits:

        # Parametri mappa QSM
        params = {
        "k" : 0.273,
        "K" : 1.5,
        }
        params["T"] = params["K"]/params["k"]
        params["L"] = params["T"]*2**n/(2*np.pi)
        params["N"] = 2**n
        print( params )

        #CIRCUITO
        #definisco il circuito (qubit, bit classici)
        qc = QuantumCircuit(n,n)

        qc.x(n-1) #momento iniziale piccato su |001>
        
        qc = iteration(qc, params)
        qc_compiled = transpile(qc, backend=provider.get_backend('ibmq_lima')) #compilo il circuito


        picchi = []
        for backend in backends:

            files = list(os.walk(directory+backend+'\\'))[0][2]
            filtered_files = [file for file in files if str(n) in file]
            double_filtered_files = [file for file in filtered_files if '1iter' in file]
            print("filtered files: ", double_filtered_files)
            #importo i dati contenuti dentro al file
        
            if len(double_filtered_files)>1:
                print("ERRORE")
                exit()

            filename = directory+backend+'\\'+double_filtered_files[0]

            with open(filename) as fh: #with ti consente di non dovere chiudere manualmente il file alla fine 
                json_string = fh.read()           
                data = json.loads(json_string)
            
            picchi.append(data["0"])
        print(picchi)
        if (len(picchi)==2):
            rapporto = picchi[1]/picchi[0]
         
        curva[qc_compiled.depth()]=rapporto

    """    
    if "fake" in backend:
        ls='o--'
    else:
        ls='o-'

    if "ima" in backend:
        color= "red"
    elif "noiseless" in backend:
        color="blue"
    else:
        color = "green"
    """

    plt.plot(curva.keys(), curva.values(), 'o-' ) #label=str(n)+'_'+backendKeyword+str(iter))      
    plt.xticks(list(curva.keys()))
    plt.yticks(list(curva.values()))
    plt.grid()
    plt.yscale("log")
    plt.savefig(directory+'figure\\depth'+ backend+ '.png',dpi=300)

    return



depth('lima')
print('end')