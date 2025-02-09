from build123d import *
from ocp_vscode import *

try:
    print(40*'-^')
    with ParameterGroup('Par1') as Par:
        IntParameter('a', 3)
        IntParameter('b', 2)
        IntParameter('c', 4)
        IntParameter('w', 1)
        StringParameter('box',  "Box")
        StringParameter('color', "#aaaaaaff")

    print(f"Parameters are available:")
    print(f'{Par.a=}, {Par.b=}, {Par.c=}, {Par.w=}')    
    print(f'{Par.color=}')

except e:
    print(f"{e=}")

try: 
    # Create a new part
    inner = Box( Par.a - Par.w, Par.b- Par.w, 2*Par.c)
    inner.name = 'inner'
    main = Box( Par.a, Par.b, Par.c) \
          - inner
    main.name = Par.box 
    main.color = Par.color
except e:
    print(f"{e=}")
    
show(main, inner)


