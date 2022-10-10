import xlwings as xw
import pandas as pd
import re

import csv
import os
import math
import sys
import time
import linecache


def Get_Match_Data_Count_and_Index(str_Match_data, str_FullPath, i_loop_read_file_size, i_Start_Data_Search, i_End_Data_Search):
    
    with open(str_FullPath, mode="r") as file_num:
        
        time_Start = time.time()
        #i_Data_RowCounts = linecache.getlines(str_FullPath)
        #aaa=linecache.getline(str_FullPath, 3)       
        time_End = time.time()
        print(time_End-time_Start)
        
        file_num.seek(i_Start_Data_Search)
        list_Data_Result = []   #initial
        list_Data_Result.append([0])
        #===========================================================
        i_Data_RowCounts= -1    #initial
        i_Match_Count= 0    #initial
        for i_Data_RowCounts, str_Line in enumerate(file_num):
            if str_Line[: 2+1] == str_Match_data:
                i_Match_Count+=1
                list_split=re.split(r' |\n', str_Line)
                i_index=i_Data_RowCounts*3
                i_2_Data=int(list_split[1])
                i_3_Cyc=int(list_split[2])
                list_Data_Result.append([i_index,i_2_Data,i_3_Cyc])
                
        i_Data_RowCounts+=1
        list_Data_Result[0].append(i_Match_Count)
        list_Data_Result.append([i_Data_RowCounts*3])   #final row count
        file_num.close()
    
    return list_Data_Result


time_Start = time.time()


str_Path = r"C:\Users\Lms\Desktop\python 上課\python嘗試大檔案\\"

if str_Path[:-1] !="\\":
    str_Path + "\\"

print(str_Path)

str_FileName ="tryOnly.txt"
List_DTL_check =['4401030','4401002','100']
List_Cycle_check=['0','0','1']


i_DTL_check_Count=len(List_DTL_check)

str_FullPath=str_Path + str_FileName


str_FileName_output_csv = "CE_output.csv"

#===========check RaeData Exist or not===============
if (os.path.isfile(str_FullPath)==False):
    #if no file
    print("No this RawData file ==>" + str_FullPath)
    #exit()

#========================================================================


#~~~~~big file size seperate N-time to read(seperate from "die")~~~~~~

i_File_Size = os.path.getsize(str_FullPath)

i_loop_read_file_size = 120000  #位元組
#i_loop_read_file_size = 300*1024*1024  #位元組
i_loop_read_file_size=16000000  #file lines

i_seperate_Read_Time= math.ceil(i_File_Size/i_loop_read_file_size)

str_DATA_Search="die"
list_Die_XY_and_index = Get_Match_Data_Count_and_Index(str_DATA_Search, str_FullPath, i_loop_read_file_size, 0, i_File_Size)

i_die_Count = list_Die_XY_and_index[0][-1]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

time_End = time.time()
print(time_End-time_Start)


with open(str_FullPath, mode="r") as file_num:
    
    i_add_save_DieXY_information=3
    list_Result_each_Die = [["" for i in range(i_DTL_check_Count+i_add_save_DieXY_information)] for j in range(i_die_Count +1)]
    list_Result_each_Die[0][0] = "Row(RowData)"
    list_Result_each_Die[0][1] = "Die_X"
    list_Result_each_Die[0][2] = "Die_Y"
    for i_Die in range(1, i_die_Count+1):
        list_Result_each_Die[i_Die][0]=list_Die_XY_and_index[i_Die][0]
        list_Result_each_Die[i_Die][1]=list_Die_XY_and_index[i_Die][1]
        list_Result_each_Die[i_Die][2]=list_Die_XY_and_index[i_Die][2]
    
    
    
    #=============DTL check=====================
    
    for i_DTL in range(i_DTL_check_Count):
        print("now find DTL(" + str(i_DTL) + "): " + "%" + List_DTL_check[i_DTL])
        list_Result_each_Die[0][i_add_save_DieXY_information+i_DTL]="%" + List_DTL_check[i_DTL] + "_" + List_Cycle_check[i_DTL]
        i_index=-1
        
        for i_Die in range(1, i_die_Count +1 ):
            print("Now CHECK DIE: " +str(i_Die))
            
            file_num.seek(0)
            i_Start_Data_Search=list_Die_XY_and_index[i_Die][0]
            i_End_Data_Search=list_Die_XY_and_index[i_Die+1][0]-1
            cc=file_num.readlines()[int(i_Start_Data_Search/3) : int(i_End_Data_Search/3) +1]
            #print(cc)
            str_data = "".join(cc)  #list to string
            list_split=re.split(r' |\n', str_data)
            
            
            i_find_same_DTL_count = list_split.count("%" + List_DTL_check[i_DTL] )
            print("i_find_same_DTL_count: " + str(i_find_same_DTL_count))
            i_shift_check = 0
            Flag_hasFind_Result = False
            
            for i_find_same_cycle in range(i_find_same_DTL_count):
                i_match_DTL = list_split.index("%" + List_DTL_check[i_DTL], i_shift_check)  
                print("i_match_DTL index: " + str(i_match_DTL) + " , RawData (from " + str(i_Start_Data_Search+i_shift_check) + " to " + str(i_End_Data_Search) + ")" )
                print("i_match_DTL index: " + str(i_match_DTL) + " , list_split (from " + str(i_shift_check) + " to " + str(len(list_split)-1) + ")" )
                
                if List_Cycle_check[i_DTL] == list_split[i_match_DTL + 2]:
                    
                    #DTL + cycle all match
                    print("此i_match_DTL的cyc也正確: " + str(List_Cycle_check[i_DTL]) + "==" + str(list_split[i_match_DTL + 2]))
                    Flag_hasFind_Result = True
                    list_Result_each_Die[i_Die][i_add_save_DieXY_information + i_DTL]=list_split[i_match_DTL + 1]
                    break
                else:
                    
                    #DTL match but cycle different
                    print("此i_match_DTL的cyc錯誤: " + str(List_Cycle_check[i_DTL]) + "!=" + str(list_split[i_match_DTL + 2]))
                    i_shift_check = i_match_DTL + 1
                    
            if Flag_hasFind_Result == False :
                #no Find ==> this die no data
                list_Result_each_Die[i_Die][i_add_save_DieXY_information + i_DTL] ="NA"
            
        print("list_Result_each_Die: " + str(list_Result_each_Die))
        
    file_num.close()
            
    #==================================================================================================================


#=============DTL find result output to csv=====================

with open(str_Path + str_FileName_output_csv, mode="a", newline='') as file_num:
    writer = csv.writer(file_num, quoting = csv.QUOTE_ALL, delimiter=",")
    writer.writerows(list_Result_each_Die)
    
    file_num.close()
#==================================================================================================================


time_End = time.time()
print("Finish: " + str(time_End-time_Start))




