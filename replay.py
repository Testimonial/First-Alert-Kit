"""
First alert kit REPLY MODE
Author: Jaroslava Kazbundova, Miroslav Capek, Jachym Goth
Team: Edubbaa
Organization: Edubbaa - základní škola, s. r. o.
Supervised by: Ladislav Bihari

ladislav.bihari@gmail.com
+420 773 798 278

From visualization perspective Red's bad and green's good
If any parameter is out of the safe range will use a weighted factor individualy
for each metric and calculate weighted average.
As you will find out each metric is specify by range and weighted factor individually
"""


import os
import csv

dir_path = os.path.dirname(os.path.realpath(__file__))

def create_csv_file(data_file):
    "Create a new CSV file and add the header row"
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['datetime',
                         'temp_cent','temp',
                         'hum_cent','hum',
                         'tdp_cent','tdp',
                         'pres_cent','pres',
                         'long','lat','wm'])

def add_csv_data(data_file, data):
    "Add a row of data to the data_file CSV"
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

try:

  """
    Variable definition section
    Author: Jaroslava, Miroslav
    Quality Assurance: Jachym
  
    This section define parameters with its initial values. For testing purpose we
    specified ideal values for temperature, humidity and pressure.
  
  #base_t=26   #baseline temperature
  #base_rh=45  #baseline relative humidity
  #base_p=1013.25  #Pa, it is 1013.25 mBar
  
    For real case scenario we are expecting program will be executed in controlled
    environment so for that reason we are seting up values from that moment
    of execution. Weighted mean is so sensitive so we cannot stick to constats
  """
  base_t=30.385456085205078   #baseline temperature
  base_rh=35.223148345947266  #baseline relative humidity
  base_p=982.548828125  #Pa, it is 1013.25 mBar

  base_acc_x = -0.0015
  base_acc_y = 0.0036
  base_acc_z = 0.0163

#datetime,cpu_temp,temp,hum,tdp,pres,mag_x,mag_y,mag_z,acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z,long,lat,wm
#2021-04-18 21:07:10.152553,35.78,30.3855,33.84,17.1534,982.5513,-45.8292,-1.5277,42.3373,-0.001,0.0046,0.0193,0.2637,0.229,0.08,44.51537200987,-119.06172659264124,93.428


  # GET ORIENTATION
  """
    We decided to exclude orientation metrics from our eqation
    Complexity to track real and expected orbit is just out of our knowledge
    #Orientation
  """

  base_mag_x = -45.90709686279297
  base_mag_y = -1.4960670471191406
  base_mag_z = 42.324710845947266

  # GET GYRO
  # We are constantly seting gyro x,y,z to zero with program start
  #0.2637,0.229,0.08
  base_gyro_x=0.2637
  base_gyro_y=0.229
  base_gyro_z=0.08

  squeezeBy=1
  # Temperature positive and degative deviation tolerance range
  t1_pos_dev=5/squeezeBy
  t1_neg_dev=-10/squeezeBy

  # Relative Humidity positive and negative deviation tolerance range
  rh_pos_dev=15/squeezeBy
  rh_neg_dev=-40/squeezeBy

  #Pressure positive and negative deviation tolerance range
  p_pos_dev=200/squeezeBy
  p_neg_dev=-250/squeezeBy

  #Very important dew point range lowest and highest
  tdp_dev_min=-6/squeezeBy
  tdp_dev_max=-2/squeezeBy
  tdp_wf=100

  """
    We are getting to weighted factor topic. From our experiments it seems
    we are confident with next factors. We were looking for importance of each
    deviation range
    Author: Jaroslava, Miroslav
    Quality assurance: Jachym
    
    Weighted factors are optimal numbers as results of long term experiments
    what is confortable and what is dangerous
    First alert kit purpose is to initiate RED ALERT
  """
  pos_t_wf=24 #Temperature positive deviation weighted factor
  nul_t_wf=30 #When Temperature is just all right weighted factor
  neg_t_wf=13 #Temperature negative deviation weighted factor

  pos_rh_wf=20 #Relative Humidity positive deviation weighted factor
  nul_rh_wf=20 #When Relative Humidity is just all right weighted factor
  neg_rh_wf=10 #Relative Humidity positive deviation weighted factor

  pos_p_wf=10 #Pressure positive deviation weighted factor
  nul_p_wf=10 #When Pressure is just all right weighted factor
  neg_p_wf=10
  
  """
    End of Weighted Factor definition
  """

  """
    Section importend from viasial expressin of Weighted factor
    Red's Bad, Green's Good and all between
  """
#  start = Color('green')
#  end = Color('red')
#  color=tuple(i for i in start.gradient(end, steps=100))

except:
  print("Oops!")

def get_sense_data():
    
    # csv file name
    filename = "data.csv"
  
    # initializing the titles and rows list
    rows = []
  
    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        next(csvreader)
      
        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)
  
        # get total number of rows
        print("Total no. of rows: %d"%(csvreader.line_num))

    for row in rows:
        sense_data=[]
        sense_data.append(row[0])
        
        # Weights summary null
        w_sum=0
        
        # Weighted Temperature metric
        t1=float(row[2])
        t1_diff=t1-base_t
        if (t1-base_t) == 0:
            t1_w=nul_t_wf
            sense_data.append(0)
            w_sum=w_sum + nul_t_wf
        elif t1-base_t > 0:
            t1_w=pos_t_wf * abs((t1_diff*100)/t1_pos_dev)
            sense_data.append(round(abs((t1_diff*100)/t1_pos_dev), 4))
            w_sum=w_sum + pos_t_wf
        else:
            t1_w=neg_t_wf * abs((t1_diff*100)/t1_neg_dev)
            sense_data.append(round(abs((t1_diff*100)/t1_neg_dev), 4))
            w_sum=w_sum + neg_t_wf
        sense_data.append(round(t1, 4))

        # Weighted Relative Humidity metric
        rh=float(row[3])
        rh_diff=rh-base_rh
        if rh-base_rh == 0:
            rh_w=nul_rh_wf
            sense_data.append(0)
            w_sum=w_sum + nul_rh_wf
        elif rh-base_rh < 0:
            rh_w=neg_rh_wf * abs((rh_diff*100)/rh_neg_dev)
            sense_data.append(round(abs((rh_diff*100)/rh_neg_dev), 4))
            w_sum=w_sum + neg_rh_wf
        else:
            rh_w=pos_rh_wf * abs((rh_diff*100)/rh_pos_dev)
            sense_data.append(round(abs((rh_diff*100)/rh_pos_dev), 4))
            w_sum=w_sum + pos_rh_wf
        sense_data.append(round(rh, 4))

        # Weighted Dew Point metric,
        # really tricky one and we spend on it so long to get the logic
        tdp=t1-(100-rh)/5
        temp_min=t1+tdp_dev_min
        temp_max=t1+tdp_dev_max
        temp_is=tdp-temp_min
        temp_of=temp_max-temp_min
        #tdp_diff=t1-tdp
        if tdp < temp_min:
            tdp_w=1
            sense_data.append(0)
            w_sum=w_sum + 1
        elif tdp <= temp_max and tdp >= temp_min:
            tdp_w=tdp_wf * abs((temp_is*100)/temp_of)
            sense_data.append(round(abs((temp_is*100)/temp_of), 4))
            w_sum=w_sum + tdp_wf
        else:
            tdp_w=tdp_wf * 100
            sense_data.append(100)
            w_sum=w_sum + tdp_wf
        #print(tdp_w,"  ",tdp)
        sense_data.append(round(tdp, 4))
    
        # Weighted Pressure metric
        p=float(row[5])
        p_diff=p-base_p
        if p-base_p == 0:
            p_w=nul_p_wf
            sense_data.append(0)
            w_sum=w_sum + nul_p_wf
        elif p-base_p < 0:
            p_w=neg_p_wf * abs((p_diff*100)/p_neg_dev)
            sense_data.append(round(abs((p_diff*100)/p_neg_dev), 4))
            w_sum=w_sum + neg_p_wf
        else:
            p_w=pos_p_wf * abs((p_diff*100)/p_pos_dev)
            sense_data.append(round(abs((p_diff*100)/p_pos_dev), 4))
            w_sum=w_sum + pos_p_wf
        sense_data.append(round(p, 4))
        
        sense_data.extend([round(float(row[15]), 4),round(float(row[16]), 4)])
        
        wm=(t1_w + rh_w + tdp_w + p_w)/w_sum
        sense_data.append(wm)
        add_csv_data(data_file, sense_data)


try:
  data_file = dir_path + "/wm.csv"
  create_csv_file(data_file)
  counter = 1

except:
  print("Oops")
  #logger.error('{}: {})'.format(e.__class__.__name__, e))


get_sense_data()
