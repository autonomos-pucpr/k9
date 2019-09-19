from navegacao import move_to_pose
import numpy as np

x_traj = []
y_traj = []
dist_passo = []
ang_passo = []

x1, y1 = move_to_pose(3,3,0,40,20,0.43)
x2, y2 = move_to_pose(40,20,0.43,30,2,2*np.pi/3)
x3, y3 = move_to_pose(30,2,2*np.pi/3,6,18,np.pi/2)

"""
x_traj.append(x1)
x_traj.append(x2)
x_traj.append(x3)
y_traj.append(y1)
y_traj.append(y2)
y_traj.append(y3)

"""
