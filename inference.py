"""
Authors :
Aashaar Panchalan - adp170630
Manish Biyani - mxb172930
"""

import copy
class Inference:
    """Inference for Bays Net."""



    def __init__(self, net, type, noOfSamples, random):
        """Type 0: enum, 1: prior sampling, 2: rejection sampling, 3: likelihood weighting."""
        self.net = net
        self.type_ = type
        self.noOfSamples = noOfSamples
        self.random = random

    def infer(self, query):
        """Runs the inference on the query and returns the.

        Args:
            query (string) String with List of evidence and the query nodes
                           Example: [<E,t> <J,t>][M, A]
        """
        strings = query.strip("[").strip("]").split("][")
        process = self.processStr(strings[0], strings[1])
        prior = process[0]
        postList = process[1]
        inferred_prob = []
        for posterior in postList:
            prob = self.doInference[self.type_](self, posterior, prior)
            inferred_prob.append("<" + posterior + ", " + str(prob) + ">")
        return inferred_prob, prob

    def processStr(self, strE, strQ):
        """Return the evidence list and query list for given strings."""
        eList = {}
        e = strE.replace("<", "").replace(">", "").split(" ")
        for x_ in e:
            x = x_.split(",")
            truthValue = 0
            if(x[1] == "t"):
                truthValue = 1
            eList[x[0]] = truthValue
        qList = [y.strip() for y in strQ.split(",")]
        return(eList, qList)



    def enumeration(self, query, evidence):
        """Infer the exact probability of the query by enumeration."""
        # Your code goes here
        Qx= {}

        boolSet = [1,0]
        #print(self.net.nodes())
        for x_i in boolSet:
            evidence[query] = x_i;
            #print("query ", query)
            #print("evidence ", evidence)
            nodes = self.net.nodes()
                # Qx[x_i] = enumerateAll(evidence)
            Qx[x_i] = self.enumerateAll(evidence, nodes)

            del evidence[query]
        return self.normalize(Qx)


    def enumerateAll(self, evidence, nodes):
        #print("here")
        if len(nodes) == 0 or nodes is None:
            return 1.0
        Y = nodes[0]
        parents = self.net.parent(Y)
        parentTruthValues = [evidence[parent] for parent in parents]
        if (Y in evidence):
            #print("01 ", evidence)
            # print("02 ", evidence[Y])
            # print("03 ", self.net.parent(Y))
            result = self.net.probOf((Y, evidence[Y]), parentTruthValues) * self.enumerateAll(evidence, nodes[1:])
            return result
        else:
            #summing out
            result = 0
            evidence[Y] = 1 # first initialize evidence of Y to True and add it to the evidence[] for calculation
            result += self.net.probOf((Y, 1), parentTruthValues) * self.enumerateAll(evidence, nodes[1:])
            evidence[Y] = 0  # first initialize to True
            result += self.net.probOf((Y, 0), parentTruthValues) * self.enumerateAll(evidence, nodes[1:])
            del evidence[Y] # remove evidence[Y] to restore evidence back to its original value
            return result


    def normalize(self, Qx):
        """
        Simple function to normalize
        :param Qx:
        :return:
        """
        total = 0.0
        for val in Qx.values():
            total += val
        for key in Qx.keys():
            Qx[key] /= total
        return Qx


    def formatEvidence(self, evidence):
        """
        This function gives the topological index number of the evidence elements
        For nodes = ["B", "E", "A", "J", "M"] & evidence = {'A': 0, 'J': 1}
        function will produce : result = {2: 0, 3: 1} & evidence_sample =[None, None, 0, 1, None]
        'evidence_sample' is a list of evidence truth values 0/1 in toplogical order. None implies that corresponding element is not present in the evidence
        :param evidence
        :return: 'result' - a dictionary - Key is topological index of the evidence in self.net.nodes(alarm.py) and Value is 0/1 value from the evidence

        """
        nodes = self.net.nodes()#["B", "E", "A", "J", "M"]
        #evidence = {'B': 0, 'M': 0}
        keys = evidence.keys()
        # size = len(evidence)
        # print(keys)
        result = {}
        evidence_sample = [None, None, None, None, None]
        for x in keys:
            # print("x= ",x)
            for i, y in enumerate(nodes):
                # print(" i= ",i)
                # print(" y= ",y)
                if x == y:
                    result[i] = evidence.get(x)
                    evidence_sample[i] = evidence.get(x)
        # print(result)
        #print(evidence_sample)

        #return evidence_sample
        return result


    def getIndex(self, node):
        """
        This function will return the topological index value (referring to the nodes() function in alarmNetwork.py) of the node in the argument
        :param node:
        :return: index value
        """
        nodes = self.net.nodes()
        for i, x in enumerate(nodes):
            if (x == node):
                #print(i)
                return i

    def priorSampling(self, query, evidence):
        """
        Calculate the probability of query using prior sampling.
        :param query:
        :param evidence:
        :return: probability of query = 1(True)
        """
        # Your code goes here
        nSamples = self.getNSamples(evidence)
        formattedEvidence = self.formatEvidence(evidence)
        keys = formattedEvidence.keys()  # [2,3]
        evidenceList = [] # list that will contain only the samples that satisfy the evidence
        # code inside for loop - to
        for i in nSamples:
            # print(i)
            flag = True
            for j in keys:
                if i[j] != formattedEvidence[j]:
                    flag = False
            if (flag == True):
                evidenceList.append(i)

        #print(final)
        evidenceCount = len(evidenceList)
        #print(evidenceList)
        if(evidenceCount ==0):
            return 0.0
        queryIndex = self.getIndex(query)
        trueCount = 0 # no. of samples (which satisfy the evidence &) for which query node is True
        for k in evidenceList:
            if (k[queryIndex] == 1):
                trueCount += 1

        #print(trueCount)

        return trueCount/evidenceCount
        #return trueCount / self.noOfSamples


    def getNSamples(self, evidence):
        """
        Generates n samples for given evidence
        :param evidence:
        :return: list of n samples. ex. - [[1,0,0,1,0], [0,0,0,1,0], [1,0,1,1,1], ......n]
        """
        list = []
        n = self.noOfSamples
        for i in range(1, n):
            sampleList = self.getSample(evidence)
            list.append(sampleList)
        return list


    def getSample(self, evidence):
        """
        Generates 1 sample for given evidence
        :param evidence:
        :return: sample in list[] format. ex - [1,0,0,1,0]
        """
        list = []
        tempEvidence = copy.deepcopy(evidence)
        nodes = self.net.nodes()
        for node in nodes:
            parents = self.net.parent(node)
            parentTruthValues = [tempEvidence[parent] for parent in parents]
            #result = self.net.probOf((node, evidence[node]), parentTruthValues)
            result = self.net.probOf((node, 1), parentTruthValues)
            if float(self.random.uniform()) <= result:
                list.append(1) # node is evaluated to be True, so add '1' to the list
                tempEvidence[node] = 1 # add that node to evidence with a True value for it's child's CPT computation
            else:
                list.append(0)  # node is evaluated to be False, so add '0' to the list
                tempEvidence[node] = 0 # add that node to evidence with a False value for it's child's CPT computation
        return list



    def rejectionSampling(self, query, evidence):
        """Calculate the probability of query using rejection sampling.

           Find the probability of query being true given the evidence
           values using rejection sampling algo and the no of Samples mentioned.

           Args:
            noOfSamples (int)   No of samples
            evidence (dict)     Evidence dictionary with nodes as key and respective
                                truthvalues as value.
            query (string)      Name of node queried
        """
        # Your code goes here

        formattedEvidence = self.formatEvidence(evidence)
        keys = formattedEvidence.keys()
        #######################
        evidenceList = []  # list that will contain only the samples that satisfy the evidence

        # print(i)
        n = self.noOfSamples
        #for i in range(1, n):
        i=0
        while(i<n):
            sample = self.getSample(evidence)
            flag = True
            for j in keys:
                if sample[j] != formattedEvidence[j]:
                    flag = False
            if (flag == True):
                evidenceList.append(sample)
                i += 1

            # print(final)
        evidenceCount = len(evidenceList)
        # print(evidenceList)
        if (evidenceCount == 0):
            return 0.0
        queryIndex = self.getIndex(query)
        trueCount = 0  # no. of samples (which satisfy the evidence &) for which query node is True
        for k in evidenceList:
            if (k[queryIndex] == 1):
                trueCount += 1

        # print(trueCount)

        return trueCount / evidenceCount

        #########################
    def likelihoodWeighting(self, query, evidence):
        """
        Calculate the probability of query using likelihood weighted sampling.
        :param query:
        :param evidence:
        :return: probability of query = 1(True)
        """
        # Your code goes here
        trueProb = 0.0
        falseProb = 0.0
        formattedEvidence = self.formatEvidence(evidence)
        keys = formattedEvidence.keys()
        evidenceList = []

        n = self.noOfSamples
        for i in range(1, n):
            x, w = self.weightedSample(evidence)
            ############ A: starts : to filter out samples which are consistent with the evidence
            flag = True
            for j in keys:
                if x[j] != formattedEvidence[j]:
                    flag = False
            if (flag == True):
                evidenceList.append(x)
            ################## A: ends

            queryIndex = self.getIndex(query)
            for k in evidenceList:
                if (k[queryIndex] == 1):
                    trueProb += w
                else:
                    falseProb += w

        total = trueProb + falseProb
        if total == 0.0:
            return 0.0
        else:
            return trueProb/total


    def weightedSample(self, evidence):
        """
        Generate sample and its corresponding weight
        :param evidence:
        :return: sample & weight - x & w
        """
        w = 1.0
        x = []
        tempEvidence = copy.deepcopy(evidence)
        nodes = self.net.nodes()
        # starting from the first node, start calculating samples for all nodes
        for node in nodes:
            keys = tempEvidence.keys()
            parents = self.net.parent(node)
            parentTruthValues = [tempEvidence[parent] for parent in parents]

            if (node in keys): # if node is in evidence
                x.append(tempEvidence[node]) # take node's truth value from the evidence

                w *= self.net.probOf((node, tempEvidence[node]), parentTruthValues) # add node's probabilty to the weight
                #w = w * weight
            else:   # if node is not in evidence, just sample it like prior or rejection sampling
                result = self.net.probOf((node, 1), parentTruthValues)
                if float(self.random.uniform()) <= result:
                    x.append(1) # add '1(True)' at the index position of the node in the sample
                    tempEvidence[node] = 1  # add that node to evidence with a True value for it's child's CPT computation

                else:
                    x.append(0) # add '0(False)' at the index position of the node in the sample
                    tempEvidence[node] = 0  # add that node to evidence with a False value for it's child's CPT computation
        return x, w





# map the inference to the function blocks
    doInference = {0: enumeration,
    1: priorSampling,
    2: rejectionSampling,
    3: likelihoodWeighting
    }