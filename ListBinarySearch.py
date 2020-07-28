fish_records=[1,1,2,3,6,7,8,18] #排序后的钓鱼数量记录
low=0
high=len(fish_records)-1
find_value=7                    #要寻找的值,可以灵活调整
find_OK=False                   #是否找到标志,True为找到
i=1                             #统计在列表里的查找次数
while low<=high:
    middle=int((low+high)/2)
    if find_value==fish_records[middle]:  #找到时
        find_OK=True                      #设置找到标志为True
        break
    elif find_value>fish_records[middle]: #没有找到,但是找的值范围大于中位值时
        low=middle+1                      #范围在midle+1和high之间
    elif find_value<fish_records[middle]: #没有找到,但是找的值范围小于中位值时
        high=middle-1                     #范围在low和midle-1之间
    i+=1                                  #统计在列表里的查找次数
if find_OK:
    print('%d is in the list on List_Number %d,tried %d times.'%(find_value,middle,i)) #打印寻找值及找到的列表下标,找的次数
else:
    print('The number %d is not in the list!Tried %d times.'%(find_value,i))          #打印没有找到信息及查找次数

#7在列表下标5处,找了2次.                   寻找结果
