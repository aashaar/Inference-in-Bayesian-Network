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
        def asss():
            print();
            x= self.net



    def priorSampling(self, query, evidence):
        """Calculate the probability of query using prior sampling."""
        # Your code goes here

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



    def likelihoodWeighting(self, query, evidence):
        """Calculate the probability of query using likelihood weighted sampling."""
        # Your code goes here



# map the inference to the function blocks
    doInference = {0: enumeration,
    1: priorSampling,
    2: rejectionSampling,
    3: likelihoodWeighting
    }