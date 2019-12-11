#Version with pandas

#import des librairies
#import os

import numpy as np # lib de math matrice
import quaternion # quaternions lib
import pandas as pd  # pour manipuler des tableau de manière efficace


# funtions 

def add_rot_mat_cols_r_BGeo_rk_angle( file_to_import = "data.csv"):
# This fucntion add 13 columns to the PIX4 data log

#Parametres
#file_to_import ="data_short_version.csv"

#minimum acceptable value for the mean of the guessed vertical vector dot product with the Geo vertical vector
#event if r_BGeo is actually vertical when flying strait the mean dot product is < 1 because when turning it is < 1
  min_mean_r_BGeo_z = 0.92 

#On stocke les donnée excel dans un panda dataframe ( bien plusutilie que dans de tableau classique)
# la dataframe s'apelle: df
#df = pd.read_excel(file_to_import, index_col=0)  
  df = pd.read_csv(file_to_import)  # doctest: +SKIP

#On affiche quelques info :
  print(" la df  fait :" + str(len(df)) + " lignes")

  print(" df  shape ( nb row, nb col) :" + str(df.shape)  )
  print( "\n info : \n")
  print( df.info())
  print( "\n description : \n" )
  print( df.describe())

  print( "affiche une vu tronquée 5 premieres lignes de  df")
  print(df.head(5))

# We are going to add colums to the df
# nine columns will be added for the rotation matrice where the BX base (u,v,w) expressed in BGeo base (i,j,k)
# three columns containing the mean vertical vector (which hopefully is the r vector in BP the parapente base (p,q,r)) 
# in the BGeo base, and one for the angle between this one and the vertical vector k. 13 columns altogether

# Read quaternions from PIX4 log
  q4_array = np.array(df[["q[0]","q[1]","q[2]","q[3]"]])
  q_array = quaternion.as_quat_array(q4_array)
# for each timestep the matrix is the BX base (u,v,w) expressed in BGeo base (i,j,k) therefore it is an array of matrices
# [[u.i v.i w.i]
#  [u.j v.j w.j]
#  [u.k v.k w.k]]
  mat_rot_array = quaternion.as_rotation_matrix(q_array) 
#

# Store in df as columns u.i,u.j,u.k,v.i,v.j,v.k,w.i,w.j,w.k 
  uvw_array=np.zeros((len(df.index),9))

  for i in range(0,len(df.index)):
    for j in range(0,3):
      for k in range(0,3):
        uvw_array[i,3*j+k]=mat_rot_array[i,k,j] 
#print(mat_rot_array[0])  
#print(str(uvw_array[0]) + "\n")
  df.loc[:,"ui"]=uvw_array[:,0]
  df.loc[:,"uj"]=uvw_array[:,1]
  df.loc[:,"uk"]=uvw_array[:,2]
  df.loc[:,"vi"]=uvw_array[:,3]
  df.loc[:,"vj"]=uvw_array[:,4]
  df.loc[:,"vk"]=uvw_array[:,5]
  df.loc[:,"wi"]=uvw_array[:,6]
  df.loc[:,"wj"]=uvw_array[:,7]
  df.loc[:,"wk"]=uvw_array[:,8] 
#print(df.head(3))

# we are going to find the vector r expressed in BX which is the best we can find as the 3rd vector in the BP base (p,q,r)
# r = au+bv+cw with r_BX=(a,b,c) coord of r in BX are found thank to mu and lam coming rom partial derivatives=0 on r_BX.k
  mean_rot_mat = np.mean(mat_rot_array, axis=0)
#print("\n mean_rot_mat : " )
#print(mean_rot_mat)
#print("\n moyennes : \n" )
#print("ui_vi_wi_mean=" + str(mean_rot_mat[0]))
#print("uj_vj_wj_mean=" + str(mean_rot_mat[1]))
#print("uk_vk_wk_mean=" + str(mean_rot_mat[2]))
# mu and lam calculation
  mu=np.arctan2(mean_rot_mat[2,2],mean_rot_mat[2,1])
  lam=np.arctan2(mean_rot_mat[2,1]*np.cos(mu)+mean_rot_mat[2,2]*np.sin(mu),mean_rot_mat[2,0])
#print("mu = " + str(mu) + "     lam = " + str(lam) + "\n")
  r_BX=np.array([np.cos(lam), np.sin(lam)*np.cos(mu), np.sin(lam)*np.sin(mu)]) #[a,b,c]=[cos(lam),sin(lan)cos(mu),sin(lam)sin(mu)]
  mean_r_BGeo=mean_rot_mat@r_BX
#print("mean_r_BGeo = " + str(mean_r_BGeo))
  if mean_r_BGeo[2]<min_mean_r_BGeo_z: #mean(r.k)=mean_r_BGeo[2] has to be near but cannot be 1.0
    if mean_r_BGeo[2]<-min_mean_r_BGeo_z:
      print("r_BX is upside down we are changing to -r_BX")
      r_BX=-r_BX #r_BX we found is the opposite of vertical still it is vertical
    else:
      print("vertical_vector r might not have been guessed correctly, mean_r_BGeo = " + str(mean_r_BGeo))
#print("r_BX : r_BX = " + str(r_BX) + "\n")
  r_BGeo_array=np.zeros((len(df.index),3))
  for i in range(0,len(df.index)):
    r_BGeo_array[i] = mat_rot_array[i]@r_BX
#print("r_BGeo_array[0] = " + str(r_BGeo_array[0]))
#print("r_BGeo_array[1] = " + str(r_BGeo_array[1]))
  df.loc[:,"ri"]=r_BGeo_array[:,0]
  df.loc[:,"rj"]=r_BGeo_array[:,1]
  df.loc[:,"rk"]=r_BGeo_array[:,2] 
# Now we put a column with arccos(r.k) which is the angle between the mean vertical and the actual vertical 
  df.loc[:,"rk_angle"]=np.arccos(r_BGeo_array[:,2])
  print(df.head(5))

# Comment ils calcule les angles d'euler:
# roll = np.arctan2(2.0 * (q[0] * q[1] + q[2] * q[3]),
#                     1.0 - 2.0 * (q[1] * q[1] + q[2] * q[2]))
# pitch = np.arcsin(2.0 * (q[0] * q[2] - q[3] * q[1]))
# yaw = np.arctan2(2.0 * (q[0] * q[3] + q[1] * q[2]),
#                     1.0 - 2.0 * (q[2] * q[2] + q[3] * q[3])) 

add_rot_mat_cols_r_BGeo_rk_angle( "data_short_version.csv" )
# 
