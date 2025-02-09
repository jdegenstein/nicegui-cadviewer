from build123d import *
from ocp_vscode import *

try:
    print(40*'-^')
    with ParameterGroup('P') as par:
        P = par
        IntParameter('a', 3)
        IntParameter('b', 2)
        IntParameter('c', 4)
        IntParameter('w', 1)
        StringParameter('box',  "Box")
        StringParameter('color', "#aa0000ff")
        
    print(f"Parameters are available:")
    print(f'{P.a=}, {P.b=}, {P.c=}, {P.w=}')    
    print(f'{P.color=}')

except ImportError:
    print("Parameters are not available")

# Create a new part
inner = Box( P.a - P.w, P.b- P.w, 2*P.c)
inner.name = 'inner'
main = Box( P.a, P.b, P.c) \
      - inner
main.name = P.box 
main.color = P.color

show(main, inner)
