

from itertools import groupby
from operator import itemgetter



# import requests

# url = 'https://be-together-backend.herokuapp.com/users/profile/vote_list/all'
# headers = {'user-agent': 'my-app/0.0.1'}
# response = requests.get(url, headers=headers)




dataigetfromget = [
    {
        "id": 1,
        "whishlist": [
            "1",
            "3",
            "7",
            "8",
            "2"
        ],
        "voted_by": 3,
        "asigned_to": '0',
        "group_project_id": '0'
    },
    {
        "id": 2,
        "whishlist": [
            "3",
            "6",
            "2",
            "1",
            "9"
        ],
        "voted_by": 1,
        "asigned_to": '0',
        "group_project_id": '0'
    },
    {
        "id": 8,
        "whishlist": [
            "3",
            "2",
            "5",
            "6",
            "1"
        ],
        "voted_by": 26,
        "asigned_to": '0',
        "group_project_id": '0'
    },
    {
        "id": 11,
        "whishlist": [
            "4",
            "2",
            "7",
            "8",
            "1"
        ],
        "voted_by": 28,
        "asigned_to": '0',
        "group_project_id": '0'
    },
    {
        "id": 12,
        "whishlist": [
            "6",
            "2",
            "5",
            "1",
            "8"
        ],
        "voted_by": 29,
        "asigned_to": '0',
        "group_project_id": '0'
    },
    {
        "id": 13,
        "whishlist": [
            "5",
            "6",
            "7",
            "9",
            "2"
        ],
        "voted_by": 30,
        "asigned_to": '0',
        "group_project_id": '0'
    }
]

#print(dataigetfromget)
newdictfromget = {}

for i in dataigetfromget:
    UserIDFromRaw = i['voted_by']
    WishlistFromRaw = i['whishlist']

    print(UserIDFromRaw, WishlistFromRaw )
    newdictfromget[UserIDFromRaw] = WishlistFromRaw

#print(newdictfromget)

for i, users in enumerate(newdictfromget):
    # print(i, users)
    n_o_g_n = i/3
print('number of groups =', round(n_o_g_n))

#this should be looped
listofvalue = []
listOf1 = []
listOf2 = []
listOf3 = []
listOf4 = []
listOf5 = []
listOf6 = []

ListOfGroup = []


for i in (newdictfromget): #get all in data from users
    my_list = newdictfromget[i] 
    my_dict = dict() #make a new dictionary to give project id a value
    for index,value in enumerate(my_list):
        my_dict[index] = value

        if value == '1' and value in my_list:
            listOf1.append(index)
        elif '1' not in my_list:
            listOf1.append(1)
        if value == '2' and value in my_list:
            listOf2.append(index)
        elif '2' not in my_list:
            listOf2.append(1)
        if value == '3' and value in my_list:
            listOf3.append(index)
        elif '3' not in my_list:
            listOf3.append(1)
        if value == '4' and value in my_list:
            listOf4.append(index)
        elif '4' not in my_list:
            listOf4.append(1)
        if value == '5' and value in my_list:
            listOf5.append(index)
        elif '5' not in my_list:
            listOf5.append(1)
        if value == '6' and value in my_list:
            listOf6.append(index)
        elif '6' not in my_list:
            listOf6.append(1)
sumof6 = {'id':6, 'value': sum(listOf6) }
sumof5 = {'id':5, 'value': sum(listOf5) }
sumof4 = {'id':4, 'value': sum(listOf4) }
sumof3 = {'id':3, 'value': sum(listOf3) }
sumof2 = {'id':2, 'value': sum(listOf2) }
sumof1 = {'id':1, 'value': sum(listOf1) }

listofvalue.append(sumof1)
listofvalue.append(sumof2)
listofvalue.append(sumof3)
listofvalue.append(sumof4)
listofvalue.append(sumof5)
listofvalue.append(sumof6)

print(listofvalue) 


newlist = sorted(listofvalue, key=itemgetter('value')) 
newlist2 = newlist[:(round(n_o_g_n))]
idofprojectwekeep = []

for i in newlist2:
    idofprojectwekeep.append((i['id']))

print('id of the project we keep', idofprojectwekeep)  

#replace all the other id of project by 0
for i in (newdictfromget):
    listOfArray = newdictfromget[i]
    for x in listOfArray:
            if x != str(idofprojectwekeep[0]) and x != str(idofprojectwekeep[1]):
                listOfArray = list(map(lambda items: items.replace(str(x) ,"0"), listOfArray))

    if listOfArray[0] != '0':
        ListOfGroup.append({'userID': i, 'learner_project': listOfArray[0]})
        print(i, listOfArray[0])
    elif listOfArray[1] != '0':
        ListOfGroup.append({'userID': i, 'learner_project': listOfArray[1]})

        print(i, listOfArray[1])
    elif listOfArray[2] != '0':
        ListOfGroup.append({'userID': i, 'learner_project': listOfArray[2]})

        print(i, listOfArray[2])
    elif listOfArray[3] != '0':
        ListOfGroup.append({'userID': i, 'learner_project': listOfArray[3]})

        print(i, listOfArray[3])
    elif listOfArray[4] != '0':
        ListOfGroup.append({'userID': i, 'learner_project': listOfArray[4]})

        print(i, listOfArray[4])


OrderedListOfGroup = sorted(ListOfGroup, key=itemgetter('learner_project'))
#print(OrderedListOfGroup)

 # define a fuction for key
def key_func(k):
     return k['learner_project']
  
 # sort OrderedListOfGroup data by 'company' key.
OrderedListOfGroup = sorted(OrderedListOfGroup, key=key_func)

for key, value in groupby(OrderedListOfGroup, key_func):
    group1 = list(value)
    break

for key, value in groupby(OrderedListOfGroup, key_func):
    group2 = list(value)


print(group1)
print(group2)

for i in group1:
    print(i)
    valueOfLearnerProject1 = i['learner_project']
    break

for i in group2:
    print(i)
    valueOfLearnerProject2 = i['learner_project']
    break

valueOfUserInGroup1 = []
for i in group1:
    print(i)
    valueOfUserInGroup1.append(i['userID'])

valueOfUserInGroup2 = []
for i in group2:
    print(i)
    valueOfUserInGroup2.append(i['userID'])

print(valueOfLearnerProject1)
print(valueOfLearnerProject2)
print(valueOfUserInGroup1)
print(valueOfUserInGroup2)