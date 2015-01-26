__author__ = 'Samartha'

import random

class_zero = {}
class_one = {}
PofC_train = {}
trng_file_class_list = []

trngfile_name = "processed_train_00.csv"
testfile_name = "processed_test_00.csv"

#for Training file
trng_file = open(trngfile_name,"r")
trngfile_line_ctr = 0
for line in trng_file:
    trngfile_line_ctr+=1
    # if(trngfile_line_ctr == 1):
    #     continue
    line = line.replace("\n","")

    attr = line.split(",")
    class_value = int(attr[len(attr)-1])
    trng_file_class_list.append(int(class_value))
    #calculate probability of IsBadBuy = yes or no
    if(class_value in PofC_train):
        PofC_train[class_value]+=1
    else :
        PofC_train[class_value] = 1
    for i in range(3, len(attr)-1):
        feature_attr = int(float(attr[i]))

        #for getting to know which attribute the given class value belongs to
        if(class_value == 0):
            if (i, feature_attr) in class_zero:
                class_zero[(i, feature_attr)]+=1
            else :
                class_zero[(i, feature_attr)] = 1
        else :
            if (i,feature_attr) in class_one :
                class_one[(i, feature_attr)]+=1
            else :
                class_one[(i, feature_attr)] = 1

trngfile_line_ctr-=1

#print(len(class_zero))
#print(len(class_one))
IsBadBuy_count = PofC_train[1]
NotIsBadBuy_count = PofC_train[0]
print("IsBadBuy count = " + str(PofC_train[1]))
print("Is Not BadBuy count = " + str(PofC_train[0]))


#probability of IsBadBuy in Training file
prob_IsBadBuy = float((PofC_train[1]))/trngfile_line_ctr
print("prob_IsBadBuy = " + str(prob_IsBadBuy))
prob_NotIsBadBuy = float((PofC_train[0]))/trngfile_line_ctr
print("prob_NotIsBadBuy = " + str(prob_NotIsBadBuy))

#get conditional probability of each attribute
IsBadBuy = False
#trng_file = open("trng_modified - Copy.csv","r")
trng_file = open(trngfile_name,"r")
line_ctr = 0
attr_list =  []
predicted_class_list = []
for line in trng_file:
    attr_list = []
    line_ctr+=1
       continue
    line = line.replace("\n","")

    attr = line.split(",")
    #print("len(attr)-1 = ", len(attr)-1)
    for i in range(0, len(attr)-1):
        attr_list.append(attr[i])

    cond_prob_IsBadBuy = 1
    cond_prob_NotIsBadBuy = 1
    final_cond_prob_NotIsBadBuy = 1
    final_cond_prob_IsBadBuy = 1

    class_value = int(attr[len(attr_list)-1])

    for z in range(3,len(attr_list)-1):
    #for item in attr_list:
        item = int(float(attr_list[z]))
        #print((z, item))
        if ((z, item) in class_zero):
            cond_prob_NotIsBadBuy = float(class_zero[(z, item)])/NotIsBadBuy_count
            final_cond_prob_NotIsBadBuy *= cond_prob_NotIsBadBuy
            #print("Negative conditional prob = " + str(final_cond_prob_NotIsBadBuy))
        else :
            cond_prob_NotIsBadBuy = float(1)/NotIsBadBuy_count
            final_cond_prob_NotIsBadBuy *= cond_prob_NotIsBadBuy

        if ((z, item) in class_one):
            cond_prob_IsBadBuy = float(class_one[(z, item)])/IsBadBuy_count
            #print("cond_prob_IsBadBuy = " + str(cond_prob_IsBadBuy))
            final_cond_prob_IsBadBuy *= cond_prob_IsBadBuy
            #print("Positive conditional prob = " + str(final_cond_prob_IsBadBuy))
        else :
            cond_prob_NotIsBadBuy = float(1)/IsBadBuy_count
            final_cond_prob_IsBadBuy *= cond_prob_IsBadBuy

    final_cond_prob_IsBadBuy*=prob_IsBadBuy
    #print("final_cond_prob_IsBadBuy = " + str(final_cond_prob_IsBadBuy))
    final_cond_prob_NotIsBadBuy*=prob_NotIsBadBuy
    if(IsBadBuy):
        predicted_class = 1
    elif(final_cond_prob_IsBadBuy > final_cond_prob_NotIsBadBuy):
        predicted_class = 0
    else :
        predicted_class = 1

    predicted_class_list.append(predicted_class)

true_pos = 0
true_neg = 0
false_pos = 0
false_neg = 0

#print(predicted_class_list)
for i in range(len(predicted_class_list)):
    if(predicted_class_list[i] == trng_file_class_list[i]):
        if(predicted_class_list[i] == 1):
            true_pos += 1
        else :
            true_neg+=1
    else :
        if(predicted_class_list[i] > trng_file_class_list[i]):
            false_pos +=1
        else :
            false_neg+=1

print(true_pos, false_neg)
print(false_pos, true_neg)

#Apply the model on test data
outfile = open("output.csv","w")
ref_id = 73015
outfile.write("RefId,IsBadBuy\n")

IsBadBuy = False
#test_file = open("test_modified.csv","r")
test_file = open(testfile_name, "r")
line_ctr = 0
attr_list =  []
predicted_class_list = []
for line in test_file:
    attr_list = []
    line_ctr+=1
    line = line.replace("\n","")

    attr = line.split(",")
    #print("len(attr)-1 = ", len(attr)-1)
    for i in range(0, len(attr)-1):
        attr_list.append(attr[i])

    cond_prob_IsBadBuy = 1
    cond_prob_NotIsBadBuy = 1
    final_cond_prob_NotIsBadBuy = 1
    final_cond_prob_IsBadBuy = 1
    predicted_class_list = []
    IsBadBuy= False

    if((float(attr_list[21]) - float(attr_list[17])) == float(0) or (float(attr_list[21]) - float(attr_list[17])) == float(110)):
        IsBadBuy = True

    if((float(attr_list[9])) == 26):
        IsBadBuy = True
    if(float(attr_list[13]) > 70000 and float(attr_list[3]) == 2004):
        IsBadBuy = True
    # if(float(attr_list[5]) > 10 or float(attr_list[3]) == 2003):
    #     IsBadBuy = True
    if(int(attr_list[5]) == 5 and int(attr_list[12]) == 1):
        IsBadBuy = True
    # if(int(attr_list[4]) == 6 ):
    #     IsBadBuy = True
    if(int(attr_list[8] > 130) and int(attr_list[12]) == 1):
        IsBadBuy = True
    if(int(attr_list[4]) == 9):
        IsBadBuy = True
    if((int(attr_list[3]) == 2006) and int(attr_list[5])==4 and (int(attr_list[8]) >= 100 )):
        IsBadBuy = True

    if((int(attr_list[3]) == 2007) and int(attr_list[5])==3 and int(attr_list[12]) == 1):
        IsBadBuy = True
    if((int(attr_list[3]) == 2003) and int(attr_list[5])==7 and int(attr_list[13]) < 50000):
        IsBadBuy = True

    if(int(attr_list[3]) == 2004 and int(attr_list[5]) == 6 and int(attr_list[6]) < 100):
        IsBadBuy = True
    if(int(attr_list[3]) == 2005 and (int(attr_list[13]) > 80000 )):
        IsBadBuy = True
    if(int(attr_list[3]) == 2009 and (int(attr_list[13]) > 80000 )):
        IsBadBuy = True
    if(int(attr_list[3]) == 2002 and (int(attr_list[4]) == 7 or int(attr_list[4]) == 8)):
        IsBadBuy = True

    #ref_id = int(attr_list[1])
    ref_id = int(attr_list[0])
    for z in range(4,len(attr_list)):
    #for item in attr_list:
        item = int(float(attr_list[z]))
        #print((z, item))
        if ((z, item) in class_zero):
            cond_prob_NotIsBadBuy = float(class_zero[(z, item)])/NotIsBadBuy_count
            final_cond_prob_NotIsBadBuy *= cond_prob_NotIsBadBuy
            #print("Negative conditional prob = " + str(final_cond_prob_NotIsBadBuy))
        # else :
        #     cond_prob_NotIsBadBuy = float(1)/NotIsBadBuy_count
        #     final_cond_prob_NotIsBadBuy *= cond_prob_NotIsBadBuy

        if ((z, item) in class_one):
            cond_prob_IsBadBuy = float(class_one[(z, item)])/IsBadBuy_count
            #print("cond_prob_IsBadBuy = " + str(cond_prob_IsBadBuy))
            final_cond_prob_IsBadBuy *= cond_prob_IsBadBuy
            #print("Positive conditional prob = " + str(final_cond_prob_IsBadBuy))
        # else :
        #     cond_prob_NotIsBadBuy = float(1)/IsBadBuy_count
        #     final_cond_prob_IsBadBuy *= cond_prob_IsBadBuy

    final_cond_prob_IsBadBuy*=prob_IsBadBuy
    #print("final_cond_prob_IsBadBuy = " + str(final_cond_prob_IsBadBuy))
    final_cond_prob_NotIsBadBuy*=prob_NotIsBadBuy
    #print("final_cond_prob_NotIsBadBuy = " + str(final_cond_prob_NotIsBadBuy))
    #print("-----------------------------------------")
    if(IsBadBuy):
        predicted_class = 1
    elif(final_cond_prob_IsBadBuy > final_cond_prob_NotIsBadBuy):
        predicted_class = 0
    else :
        predicted_class = 1
    IsBadBuy = False
    #print("Predicted class = " + str(predicted_class))
    outfile.write(str(ref_id) + "," + str(predicted_class)+"\n")
    #ref_id+= 1
    predicted_class_list.append(predicted_class)

#print("len(predicted class list) = " +str(len(predicted_class_list)))

outfile.close()

#ADA BOOST
train_file_dict = {}
train_file_class_dict = {}
trainfile_line_ctr = 0
for line in open(trngfile_name):
    trainfile_line_ctr += 1
    if trainfile_line_ctr == 1 :
        continue
    if len(line) > 5 :
        #line_ctr+=1
        stuff = line.split(",")
        train_file_class_dict[trainfile_line_ctr] = stuff[len(stuff)-1]
        #print(train_file_class_dict[line_ctr])
        train_file_dict[trainfile_line_ctr] = stuff[:-1]

#print("len(train_file_class_dict) = " + str(len(train_file_class_dict)))

#Adaboost on Train file
rounds = 50
weight = []
sample_size = int(0.8 * trainfile_line_ctr)
#sample_size = 1000
w = 1.0/sample_size
#print("w = " + str(w))
for i in range(0,trainfile_line_ctr+1):
    weight.append(w)
sample_c_pos={}
sample_c_zero={}
model_pos = []
model_neg = []
error_rate = []
PofC_train = {}

for k in range(0, rounds):
    print("Started Sampling ... round "+str(k))
    d= random.sample(range(1, trainfile_line_ctr), sample_size)
    d.sort()
    if 1 in d:
        d.remove(1)
    #print("d = " + str(d))
    predicted_class_list = []
   sample_class_zero = {}
    sample_class_one= {}

    for line_num in d:
        #print("line num = " + str(line_num))
        if line_num == 1:
            continue
        line = train_file_dict[line_num]
        #print("line = " + str(line))
        #line_ctr +=1
        attr=[]
        attr_list = []
        attr_list_2 = []
        c_pos_prob_list = []
        c_neg_prob_list = []

        for item in line:
            attr_list.append(item)
        #print(attr_list)
        cond_prob_IsBadBuy = 1
        cond_prob_NotIsBadBuy = 1
        final_cond_prob_NotIsBadBuy = 1
        final_cond_prob_IsBadBuy = 1

        class_value = int(train_file_class_dict[line_num])

        #calculate probability of IsBadBuy = yes or no
        if(class_value in PofC_train):
            PofC_train[class_value]+=1
        else :
            PofC_train[class_value] = 1
        #print("attr_list len = " + str(len(attr_list)))
        for i in range(4, len(attr_list)-1):
            feature_attr = int(float(attr_list[i]))
            #print("feature attr = " + str(feature_attr))

            #for getting to know which attribute the given class value belongs to
            if(class_value == 0):
                if (i, feature_attr) in sample_class_zero:
                    sample_class_zero[(i, feature_attr)]+=1

                else :
                    sample_class_zero[(i, feature_attr)] = 1
                    # print("added to sample_class_zero")
            else :
                if (i,feature_attr) in sample_class_one :
                    sample_class_one[(i, feature_attr)]+=1
                else :
                    sample_class_one[(i, feature_attr)] = 1

    model_pos.append(sample_class_one)
    model_neg.append(sample_class_zero)

    IsBadBuy_count = PofC_train[1]
    #print("IsBadBuy count = " + str(IsBadBuy_count))
    NotIsBadBuy_count = PofC_train[0]
    #print("NotIsBadBuy count = " + str(NotIsBadBuy_count))
    prob_IsBadBuy = float((PofC_train[1]))/len(d)
    prob_NotIsBadBuy = float((PofC_train[0]))/len(d)
    predicted_class_list = []
    for line_num in d:
        attr_list = []
        if(line_num == 1):
            continue
        line = train_file_dict[line_num]
        for item in line:
            attr_list.append(item)


        cond_prob_IsBadBuy = 1
        cond_prob_NotIsBadBuy = 1
        final_cond_prob_NotIsBadBuy = 1
        final_cond_prob_IsBadBuy = 1
        IsBadBuy = False

        if((float(attr_list[21]) - float(attr_list[17])) == float(0) or (float(attr_list[21]) - float(attr_list[17])) == float(110)):
            IsBadBuy = True
        if((float(attr_list[8])) == 26):
            IsBadBuy = True
        if(float(attr_list[13]) > 70000 and float(attr_list[4]) == 2004):
            IsBadBuy = True
        if(float(attr_list[4]) == 2004 and float(attr_list[7])>100):
            IsBadBuy = True
        #class_value = int(attr[34])

        ref_id = int(attr_list[1])
        for z in range(4,len(attr_list)):
            item = int(float(attr_list[z]))
            #print((z, item))
            if ((z, item) in sample_class_zero):
                cond_prob_NotIsBadBuy = float(sample_class_zero[(z, item)])/NotIsBadBuy_count
                final_cond_prob_NotIsBadBuy *= cond_prob_NotIsBadBuy

            else :
                cond_prob_NotIsBadBuy = float(1)/NotIsBadBuy_count
                final_cond_prob_NotIsBadBuy *= cond_prob_NotIsBadBuy

            if ((z, item) in sample_class_one):
                cond_prob_IsBadBuy = float(sample_class_one[(z, item)])/IsBadBuy_count
                final_cond_prob_IsBadBuy *= cond_prob_IsBadBuy

            else :
                cond_prob_NotIsBadBuy = float(1)/IsBadBuy_count
                final_cond_prob_IsBadBuy *= cond_prob_IsBadBuy

        final_cond_prob_IsBadBuy*=prob_IsBadBuy
        final_cond_prob_NotIsBadBuy*=prob_NotIsBadBuy
        if(IsBadBuy):
            predicted_class = 1
        elif(final_cond_prob_IsBadBuy > final_cond_prob_NotIsBadBuy):
            predicted_class = 0
        else :
            predicted_class = 1
        IsBadBuy = 0
        predicted_class_list.append(predicted_class)


    hit_count = 0
    miss_count = 0
    error_Mi = 0
    correctly_classified = []
    for x in range(0, len(predicted_class_list)):
        #print("d[x]= "+str(d[x]))
        if int(predicted_class_list[x]) == int(train_file_class_dict[d[x]]):
            hit_count+=1
            correctly_classified.append(x)
        else :
            error_Mi+= weight[d[x]]*1
            miss_count+=1

    if error_Mi > 0.5 :
        break

    error_rate.append(error_Mi)
    temp = float(error_Mi)/(1-error_Mi)
    for x in range(0, len(predicted_class_list)):
        if int(predicted_class_list[x]) == int(train_file_class_dict[d[x]]):
            weight[d[x]]*=temp



#Apply Adaboost on the Test file
adaboost_class_val_list = []
wt = []
pred_model_values_list = []
for z in range(0, len(model_pos)):
    model_class_one = {}
    model_class_zero = {}
    #wt = []
    wt.append((1.0 - error_rate[z])/error_rate[z])
    predicted_class_list = []
    test_file = open(testfile_name, "r")
    line_ctr = 0
    attr_list =  []
    predicted_class_list = []
    cond_prob_IsBadBuy = 1
    cond_prob_NotIsBadBuy = 1
    final_cond_prob_NotIsBadBuy = 1
    final_cond_prob_IsBadBuy = 1
    predicted_class_list = []
    final_cond_prob_pos = 1
    final_cond_prob_neg = 1
    model_class_one = model_pos[z]
    model_class_zero = model_neg[z]

    NotIsBadBuy_count = len(model_neg[z])
    IsBadBuy_count = len(model_pos[z])
    #print("model_class_one = " + str(model_class_one))
    #print("model_class_zero = " + str(model_class_zero))
    #print(len(model_class_one))
    NotIsBadBuy_count = len(model_neg[z])
    IsBadBuy_count = len(model_pos[z])
    prob_of_C_pos = len(model_class_one)/sample_size
    #print("prob_of_C_pos = " + str(prob_of_C_pos))
    #print(len(model_class_one))
    prob_of_C_neg = len(model_class_zero)/sample_size
    #print("prob_of_C_neg = " + str(prob_of_C_neg))


    for line in test_file:
        attr_list = []
        line_ctr+=1
        if(line_ctr == 1):
            continue
        line = line.replace("\n","")

        attr = line.split(",")
        #print("len(attr)-1 = ", len(attr)-1)
        for i in range(0, len(attr)-1):
            attr_list.append(attr[i])

        IsBadBuy = False
        final_cond_prob_IsBadBuy = 1.0
        final_cond_prob_NotIsBadBuy = 1.0

        if((float(attr_list[21]) - float(attr_list[17])) == float(0) or (float(attr_list[21]) - float(attr_list[17])) == float(110)):
            IsBadBuy = True
        if((float(attr_list[8])) == 26):
            IsBadBuy = True
        if(float(attr_list[13]) > 70000 and float(attr_list[4]) == 2004):
            IsBadBuy = True
        if(float(attr_list[4]) == 2004 and float(attr_list[7])>100):
            IsBadBuy = True

        z = 0
        for z in range(4,len(attr_list)):
            item = int(float(attr_list[z]))
            #print((z, item))
            if ((z, item) in model_class_zero):
                cond_prob_NotIsBadBuy = float(model_class_zero[(z, item)])/NotIsBadBuy_count
                #cond_prob_NotIsBadBuy*=0.3
                final_cond_prob_NotIsBadBuy *= cond_prob_NotIsBadBuy
                #print("Negative conditional prob = " + str(final_cond_prob_NotIsBadBuy))
            else :
                cond_prob_NotIsBadBuy = float(1)/NotIsBadBuy_count
                final_cond_prob_NotIsBadBuy *= cond_prob_NotIsBadBuy

            if ((z, item) in model_class_one):
                cond_prob_IsBadBuy = float(model_class_one[(z, item)])/IsBadBuy_count
                final_cond_prob_IsBadBuy *= cond_prob_IsBadBuy
                #print("Positive conditional prob = " + str(final_cond_prob_IsBadBuy))
            else :
                cond_prob_NotIsBadBuy = float(1)/IsBadBuy_count
                final_cond_prob_IsBadBuy *= cond_prob_IsBadBuy


        final_cond_prob_IsBadBuy*=prob_of_C_pos
        final_cond_prob_NotIsBadBuy*=prob_of_C_neg

        predicted_class = 0
        if IsBadBuy:
            predicted_class = 1
        if float(final_cond_prob_IsBadBuy) > float(final_cond_prob_NotIsBadBuy) :
            predicted_class = 1
        else :
            predicted_class = 0
        # print("Predicted Class = " + str(predicted_class))
        predicted_class_list.append(predicted_class)

    pred_model_values_list.append(predicted_class_list)

#print("Predicted Models Value List len = " + str(len(pred_model_values_list)))

# outfile = open("output_1.csv","w")
# ref_id = 73015
# t = ref_id
# outfile.write("RefId,IsBadBuy\n")
# print(len(pred_model_values_list[0]))
# for i in range(len(pred_model_values_list[0])):
#     outfile.write(str(t) + "," + str(pred_model_values_list[0][i]))
#     #print(i)
#     t+=1
#     outfile.write("\n")










