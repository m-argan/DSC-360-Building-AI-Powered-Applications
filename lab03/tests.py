import search
import pandas as pd
import chunker
import json

#name = 'outputs/tests_mxbaimodel.csv'
#name = 'outputs/supertest_mxbaimodel.csv'
#name = 'outputs/tests_nomicmodel.csv'
name = 'outputs/supertest_nomicmodel.csv'
df = pd.read_csv(name)  # expects columns: review, sentiment
HIT1 = 0
HIT5 = 0
Hit5 = []
Hit1 = []
def compare(top5, expected):
    chunks = chunker.main()
    with open('index/chunks.jsonl', 'r') as book:
        isHit = False
        #hit1 = 0
        #hit5 = []
        global Hit5
        global HIT1
        global HIT5
        chunks = []
        for line in book:
            chunks.append(line)
        for elem in top5:
            #print(chunks[elem])
            current = json.loads(chunks[elem])
            print("curr ", current)
            first = json.loads(chunks[top5[0]])
            exp = json.loads(expected)
            print("exp ", exp)
            #is it in top5? id so, hit5 += 1
            if(current == exp):
                HIT5 += 1
                print("its the top5!")
                isHit = True

        Hit5.append(isHit)

        print("\nCURRHIT: ", Hit5)
        
        #currhit5 = 0
            #is it top? if so, hit1 += 1
        isHit = False
        if(first == exp):
            print("its in the top!")
            HIT1 += 1
            isHit = True
        
        Hit1.append(isHit)
        
        #df["Hit@1"] = HIT1
        #df.to_csv('tests.csv', index=False)
        #HIT5.to_csv('tests.csv', index=False)
        #hit1_result = hit1/5
        #hit5_result = hit5/5
        #print("expected: " , expected)

i = -1
for text in df["Prompt"]:
    i += 1
    print("-------")
    print(text)
    top5 = search.launch(text)
    #compare results to text in df["Expected"]
    expected = df["Expected"]
    print("expected: " , expected[i])
    hits = compare(top5, expected[i])
    


hit1_result = HIT1/11
hit5_result = HIT5/11
print("Hit@1: ", hit1_result)
print("Hit@5: ", hit5_result)
print("hit5: " , Hit5)
print("hit1: " , Hit1)
df["Is in top 5?"] = Hit5

df["Is in top 1?"] = Hit1
df.to_csv(name, index=False)

'''
df["Hit@1"] = hit1_result
df.to_csv('tests.csv', index=False)


df["Hit@5"] = hit5_result
df.to_csv('tests.csv', index=False)
'''
# append results to result_list (seperately)
    
#result_list.to_csv('tests.csv', index=False)

