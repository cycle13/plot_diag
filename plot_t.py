#!/usr/bin/env python 
from __future__ import print_function
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import read_diag
import numpy as np

fig = plt.figure(figsize=(16,8))

m = Basemap(lon_0=180)
m.drawmapboundary(fill_color='#A6CAE0',linewidth=0)
m.fillcontinents(color='grey',alpha=0.7,lake_color='grey',zorder=10)
m.drawcoastlines(linewidth=0.1,color="white")


dtg = '2018051312'
platform = 'conv'
obsfile = 'diag_'+platform+'_ges.'+dtg

# read header 
diag_conv = read_diag.diag_conv(obsfile,endian='big')
print('total number of obs = ',diag_conv.nobs)

# read data 
diag_conv.read_obs()



#instrumentlist = ['  v','  u','  t','  q','gps']
instrumentlist = ['  t']
for instrument in instrumentlist:

  if instrument == '  v':
    obsname = 'V-Wind'
  elif instrument == '  u':
    obsname = 'U-Wind'
  elif instrument == '  t':
    obsname = 'Temperature'
  elif instrument == '  q':
    obsname = 'Specific Humidity'
  elif instrument == 'gps':
    obsname = 'GPS Radio Occultation'

  reptypelist =[120,130,180]
# reptypelist =[120,130,131,132,133,180,182]
  for reptype in reptypelist:
    indx = np.logical_and(np.logical_and(diag_conv.obtype == instrument, diag_conv.used == 1), diag_conv.code == reptype)
    nobs = indx.sum()
    print('total number of obs',reptype,' = ',nobs)
    if nobs == 0 :
      cycle

    if reptype == 120 or reptype == 132: 
      color='b'
      platformname='ADPUPA('+str(reptype)+')'
    elif reptype == 130 or reptype == 131: 
      color='r'
      platformname='AIRCFT('+str(reptype)+')'
    elif reptype == 133: 
      color='g'
      platformname='AIRCAR('+str(reptype)+')'
    elif reptype == 180: 
      color='g'
      platformname='SFCSHP('+str(reptype)+')'
    else: 
      color='k'
      platformname='UNKNOWN('+str(reptype)+')'

    x,y = m(diag_conv.lon[indx],diag_conv.lat[indx])
    m.scatter(x,y,4,color=color,marker='o',edgecolors='none',zorder=20,label=platformname+' - '+str(nobs))

  plt.legend(ncol=7,loc=8,bbox_to_anchor=(0.5,-0.1),markerscale=2)
  plt.title(' %s   %s  Assimilated '% (dtg,obsname),fontsize=25)
  plt.savefig('T'+'_'+str(dtg)+'.png',dpi=100)
  plt.show()


