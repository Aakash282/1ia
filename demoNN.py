# NN demo
from NN import bpnn

if __name__ == "__main__":
    # Teach network XOR function
    pat = [
        [[0,0], [0]],
        [[0,1], [1]],
        [[1,0], [1]],
        [[1,1], [0]]
    ]

    # create a network with two input, two hidden, and one output nodes
    n = bpnn.BPNN([2, 2, 1])
    # train it with some patterns
    n.train(pat, iterations=1000, L=.5)
    # test it
    
    for p in pat: 
        print str(p[0]) + " -> %f" % (n.predict(p[0]))
