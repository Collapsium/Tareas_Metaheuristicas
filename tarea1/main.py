import sys
import threading
import time

sys.setrecursionlimit(500)

def get_curr_global():
    global global_earnings
    while True:
        with open("sum_data_3.txt", "a") as file:
            file.write(str(global_earnings) + "\n")
        time.sleep(60)  # Sleep for 1 minute

def read_file(filename):
    current_list = []
    values = []
    cont = 1
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip().split() 
            curr_list = []
            curr_list.extend(map(int,line))
            if line:  
                values.append(curr_list) 


    return values

global_earnings = 0
def MFC(curr_proyect, curr_budget, local_earnings, tareas_visited ):
    #print(f"curr_proyect: {curr_proyect}")
    global proyects_visited
    
    #revisar si sirve como candidato
    proyect_price = 0
    for i, x in enumerate(tareas_por_proyecto[curr_proyect]):
        #si hay que hacer la tarea x, y además el proyecto aún no está visitado:
        if x == 1 and tareas_visited[i] == 0:
            proyect_price += costo_n_tareas[i] 
            tareas_visited[x] = 1

    #restriccion presupuesto
    if curr_budget - proyect_price <= 0:
        global global_earnings  
        global_earnings = max(global_earnings, local_earnings)
        #print(f"GLOBAL_BUDGET :{global_earnings} ")
        return
    else:
        proyects_visited[curr_proyect] = 1

    #Recursion prox variable
    for i in range(0, len(proyects_visited)):
        if proyects_visited[i] == 0:
            MFC(i, curr_budget - proyect_price, local_earnings + ganancias_m_proyectos[curr_proyect], tareas_visited)
            proyects_visited[curr_proyect] = 0

    return
lists =  read_file(r'C:\Users\kueru\Documents\VSCode\semestre_9\metaheuristicas\3_2024.txt')
#print('size', len(lists))

#guardar datos:
m_proyectos = 0
n_tareas = 0
b_budget = 0
ganancias_m_proyectos = []
costo_n_tareas = []
tareas_por_proyecto = []

m_proyectos = lists[0][0]
n_tareas = lists[1][0]
b_budget = lists[2][0]

proyects_visited = [0 for _ in range(m_proyectos)]

for i in range(0,  m_proyectos):
    ganancias_m_proyectos.append(lists[3][i])

for i in range(0, n_tareas):
    costo_n_tareas.append(lists[4][i])

for i in range(5, len(lists)):
    aux_list = []
    for j in range(0, len(lists[i])):
        aux_list.append(lists[i][j])
    
    tareas_por_proyecto.append(aux_list)


print(f"# Filas de tareas por proyecto: {len(tareas_por_proyecto)} ; # Proyectos: {m_proyectos}")

thread = threading.Thread(target=get_curr_global)
thread.daemon = True  
thread.start()

for i in range(0, m_proyectos):
    curr_tareas_visited = [0 for _ in range(n_tareas)]
    MFC(i, b_budget, 0, curr_tareas_visited)