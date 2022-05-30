# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 16:02:34 2022

@author: rz7954

this is a script to estimate single variable, definite integrals for polynomial and trigonometric functions using Gauss-Legendre quadrature 
"""
from sympy import * 
from sympy.parsing.sympy_parser import parse_expr
#import Parser as ps - the program currently relies on the sympy library to interpret and substitute values into the user input function,
#in a future excercise sympy will be replaced by a custum parser
def legendre():
    x = symbols("x")
    
    func=input("Function to be evaluated:(Note: exponents are to be entered as '**', and variables in trig functions need to be bracketed.')\n")
    while True:
        try:
            func_parsed=parse_expr(func)
            break
        except:
            print('Function syntax error')
            pass #currently certain inputs causes sympy to continuously print out the error message (ie: inputting cos x instead of cos (x)), a solution is needed to make it ask for user input again
    while True: 
        try:
            a=float(input("What is the lower bound of the domain?\n"))
            break
        except ValueError:
            print('Lower bound must be a number!')

    while True:
        try:
            b=float(input("What is the upper bound of the domain?\n")) #can the upper bound be smaller than lower?
            break
        except ValueError:
            print('Upper bound must be a number!')
            
    while True:
        try:    
            nodes=int(input("Enter the # of nodes(an integer between 1 and 20; more nodes will yield a more accurate result)\n"))
            if nodes > 20 or nodes < 1:
                print('This number of nodes is not supported, try an integer between 1 and 20')
                continue
            else:
                break
        except ValueError:
            print('The number of nodes must be an integer!')

    #matrices comprised of gauss-legendre weights and xi values up to 20 nodes, upcoming updates will attempt to replace these with algorithms to 
    #calculate the weights and points so the support for nodes will be above 20, at the cost of computation time
    weights=[ 
        [2],
        [1,1],
        [0.555555556,0.888888889,0.555555556],
        [0.347854845,0.652145155,0.652145155,0.347854845],
        [0.236926885,0.47862867,0.568888889,0.47862867,0.236926885],
        [0.171324492,0.360761573,0.467913935,0.467913935,0.360761573,0.171324492],
        [0.129484966,0.279705391,0.381830051,0.417959184,0.381830051,0.279705391,0.129484966],
        [0.101228536,0.222381034,0.313706646,0.362683783,0.362683783,0.313706646,0.222381034,0.101228536],
        [0.081274388,0.180648161,0.260610696,0.312347077,0.330239355,0.312347077,0.260610696,0.180648161,0.081274388],
        [0.066671344,0.149451349,0.219086363,0.269266719,0.295524225,0.295524225,0.269266719,0.219086363,0.149451349,0.066671344],
        [0.055668567,0.125580369,0.186290211,0.233193765,0.262804545,0.272925087,0.262804545,0.233193765,0.186290211,0.125580369,0.055668567],
        [0.047175336,0.106939326,0.160078329,0.203167427,0.233492537,0.249147046,0.249147046,0.233492537,0.203167427,0.160078329,0.106939326,0.047175336],
        [0.040484005,0.0921215,0.13887351,0.178145981,0.207816048,0.22628318,0.232551553,0.22628318,0.207816048,0.178145981,0.13887351,0.0921215,0.040484005],
        [0.03511946,0.080158087,0.121518571,0.157203167,0.185538397,0.205198464,0.215263853,0.215263853,0.205198464,0.185538397,0.157203167,0.121518571,0.080158087,0.03511946],
        [0.030753242,0.070366047,0.10715922,0.139570678,0.166269206,0.186161,0.198431485,0.202578242,0.198431485,0.186161,0.166269206,0.139570678,0.10715922,0.070366047,0.030753242],
        [0.027152459,0.062253524,0.095158512,0.124628971,0.149595989,0.169156519,0.182603415,0.18945061,0.18945061,0.182603415,0.169156519,0.149595989,0.124628971,0.095158512,0.062253524,0.027152459],
        [0.024148303,0.055459529,0.085036148,0.111883847,0.135136368,0.154045761,0.168004102,0.176562705,0.17944647,0.176562705,0.168004102,0.154045761,0.135136368,0.111883847,0.085036148,0.055459529,0.024148303],
        [0.021616014,0.049714549,0.07642573,0.100942044,0.122555207,0.140642915,0.154684675,0.164276484,0.169142383,0.169142383,0.164276484,0.154684675,0.140642915,0.122555207,0.100942044,0.07642573,0.049714549,0.021616014],
        [0.019461788,0.044814227,0.069044543,0.091490022,0.111566646,0.128753963,0.142606702,0.152766042,0.158968843,0.16105445,0.158968843,0.152766042,0.142606702,0.128753963,0.111566646,0.091490022,0.069044543,0.044814227,0.019461788],
        [0.017614007,0.04060143,0.062672048,0.083276742,0.10193012,0.118194532,0.131688638,0.142096109,0.149172986,0.152753387,0.152753387,0.149172986,0.142096109,0.131688638,0.118194532,0.10193012,0.083276742,0.062672048,0.04060143,0.017614007]]
  
    domain_pts=[ 
        [0],
        [-0.577350269,0.577350269],
        [-0.774596669,0,0.774596669],
        [-0.861136312,-0.339981044,0.339981044,0.861136312],
        [-0.906179846,-0.53846931,0,0.53846931,0.906179846],
        [-0.932469514,-0.661209386,-0.238619186,0.238619186,0.661209386,0.932469514],
        [-0.949107912,-0.741531186,-0.405845151,0,0.405845151,0.741531186,0.949107912],
        [-0.960289856,-0.796666477,-0.52553241,-0.183434642,0.183434642,0.52553241,0.796666477,0.960289856],
        [-0.96816024,-0.836031107,-0.613371433,-0.324253423,0,0.324253423,0.613371433,0.836031107,0.96816024],
        [-0.973906529,-0.865063367,-0.679409568,-0.433395394,-0.148874339,0.148874339,0.433395394,0.679409568,0.865063367,0.973906529],
        [-0.978228658,-0.8870626,-0.730152006,-0.519096129,-0.269543156,0,0.269543156,0.519096129,0.730152006,0.8870626,0.978228658],
        [-0.981560634,-0.904117256,-0.769902674,-0.587317954,-0.367831499,-0.125233409,0.125233409,0.367831499,0.587317954,0.769902674,0.904117256,0.981560634],
        [-0.984183055,-0.917598399,-0.801578091,-0.642349339,-0.448492751,-0.230458316,0,0.230458316,0.448492751,0.642349339,0.801578091,0.917598399,0.984183055],
        [-0.986283809,-0.928434884,-0.827201315,-0.687292905,-0.515248636,-0.319112369,-0.108054949,0.108054949,0.319112369,0.515248636,0.687292905,0.827201315,0.928434884,0.986283809],
        [-0.987992518,-0.937273392,-0.848206583,-0.724417731,-0.570972173,-0.394151347,-0.201194094,0,0.201194094,0.394151347,0.570972173,0.724417731,0.848206583,0.937273392,0.987992518],
        [-0.989400935,-0.944575023,-0.865631202,-0.755404408,-0.617876244,-0.458016778,-0.281603551,-0.09501251,0.09501251,0.281603551,0.458016778,0.617876244,0.755404408,0.865631202,0.944575023,0.989400935],
        [-0.990575475,-0.950675522,-0.880239154,-0.781514004,-0.657671159,-0.512690537,-0.351231763,-0.178484181,0,0.178484181,0.351231763,0.512690537,0.657671159,0.781514004,0.880239154,0.950675522,0.990575475],
        [-0.991565168,-0.95582395,-0.892602466,-0.803704959,-0.691687043,-0.559770831,-0.411751161,-0.251886226,-0.084775013,0.084775013,0.251886226,0.411751161,0.559770831,0.691687043,0.803704959,0.892602466,0.95582395,0.991565168],
        [-0.992406844,-0.960208152,-0.903155904,-0.822714657,-0.720966177,-0.600545305,-0.464570741,-0.3165641,-0.160358646,0,0.160358646,0.3165641,0.464570741,0.600545305,0.720966177,0.822714657,0.903155904,0.960208152,0.992406844],
        [-0.993128599,-0.963971927,-0.912234428,-0.839116972,-0.746331906,-0.636053681,-0.510867002,-0.373706089,-0.227785851,-0.076526521,0.076526521,0.227785851,0.373706089,0.510867002,0.636053681,0.746331906,0.839116972,0.912234428,0.963971927,0.993128599]]
 
    #Changing the domain to 1 and -1 to match the Gauss-Legendre boundary
    du=(b-a)/2
    estimate = 0
    for i in range(nodes):
        x_sub=float((a+b)/2)+float(du)*float(domain_pts[nodes-1][i])
        estimate += float(du)*float(weights[nodes-1][i]*func_parsed.subs(x,x_sub)) 

    print('The function is:',func,'\nwithin bounds:',a,'and',b,'\nthe number of nodes used is',nodes)
    print('The nodes are at points x=',domain_pts[nodes-1],'\nwith weights:',weights[nodes-1])
    print ('The integration is estimated to be',estimate)

     
    
