"""Driver"""

from alarmNetwork import AlarmNetwork
from alarmNetwork import psuedorandom
from inference import Inference

def main():
    print ("Enter input query (of the form '[<E,t> <J,t>][M, A]' ): ")
    #input_query = input()
    #input_query = '[<A,f>][B, J]'
    #input_query = '[<J,t> <E,f>][B, M]'
    input_query = '[<M,t> <J,f>][B, E]'
    print ('Inference by Enumeration: ')
    net = AlarmNetwork()
    random = psuedorandom()
    exactInfer = Inference(net, 0, 0, random )
    print ( exactInfer.infer(input_query)[0])
    print ("Enter sample count: ")
    #s = input()
    s = 10000
    NoOfSamples = int(s)
    print ('Inference by prior sampling: ')
    priorSamplingInfer = Inference(net, 1, NoOfSamples, random)
    print (priorSamplingInfer.infer(input_query)[0])
    print ('Inference by Rejection sampling: ')
    rejectionSamplingInfer = Inference(net, 2, NoOfSamples, random)
    print (rejectionSamplingInfer.infer(input_query)[0])
    print ('Inference by likelihood sampling: ')
    likelihoodInfer = Inference(net, 3, NoOfSamples, random)
    print (likelihoodInfer.infer(input_query)[0])


main()
