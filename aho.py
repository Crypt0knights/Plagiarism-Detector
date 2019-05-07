class ahoh:
    def __init__(self):
        self.maxs=5000
        self.maxc=27
        self.out=[0]*self.maxs
        self.f=[-1]*self.maxs
        self.g=[]

        for i in range(self.maxs):
            self.g.append([])
            for j in range(self.maxc):
                self.g[i].append(-1)

    def buildMatchingMachine(self,arr,k):
        states=1
        for i in range(k):
            word=arr[i]
            currentState=0
            for j in range(len(word)):
                if word[j]!=' ':
                    ch=ord(word[j])-ord('A')
                else:
                    ch=26
                if(self.g[currentState][ch]==-1):
                    self.g[currentState][ch]=states;
                    states+=1
                currentState=self.g[currentState][ch]
            self.out[currentState] |= (1<<i)

        # for i in range(maxc):
        #print(out)
        for ch in range(self.maxc):
            if (self.g[0][ch]==-1):
                self.g[0][ch]=0
        q=[]

        for ch in range(self.maxc):
            if self.g[0][ch]!=0:
                self.f[self.g[0][ch]]=0
                q.append(self.g[0][ch])

        while(len(q)):
            state=q.pop(0)
            for ch in range(self.maxc):
                if(self.g[state][ch]!=-1):
                    failure=self.f[state]
                    while(self.g[failure][ch]==-1):
                        failure=self.f[failure]
                    failure=self.g[failure][ch]
                    self.f[self.g[state][ch]]=failure
                    self.out[self.g[state][ch]] |= self.out[failure]
                    q.append(self.g[state][ch])

        return states

    def findNextState(self,currentState,nextInput):
        answer=currentState
        if nextInput!=' ':
            ch=ord(nextInput)-ord('A')
        else:
            ch=26
        while(self.g[answer][ch]==-1):
            answer=self.f[answer]
        return self.g[answer][ch]

    def searchWords(self,arr,k,text):
        input_phrase=[]
        input_phrases_indx=[]
        self.buildMatchingMachine(arr,k)
        currentState=0
        for i in range(len(text)):
            currentState=self.findNextState(currentState,text[i])
            if(self.out[currentState]==0):
                continue
            for j in range(k):
                if (self.out[currentState] & (1<<j) ):
                    input_phrase.append(arr[j])
                    input_phrases_indx.append([i-len(arr[j])+1,i])
        return input_phrase,input_phrases_indx