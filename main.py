from inputs import get_inputs
from process import process_inputs, start

a, b ,c  = get_inputs()
i1, i2, i3 = process_inputs(a,b,c)
start(i1, i2, i3)