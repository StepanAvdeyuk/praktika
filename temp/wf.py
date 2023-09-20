import matplotlib.pyplot as plt
import RigolWFM.wfm as rigol

filename = 'example.wfm'
scope = 'MSO1104'

w = rigol.Wfm.from_file(filename, scope)
w.plot()
plt.show()