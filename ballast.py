# This script plots the operating range of a seaglider 
# given a CVBD, sigma during ballast, and hardware/software VBD limits

# constansts
CC_SIGMA = 49.5
AD_CC = 4.077
# Seaglider physical parameters
vbdVolMax = 830 # vol max VBD
vbd_adMax = 3900 # software max AD count
vbd_adMin = 600 # software min AD count
# Parameters obtained during ballasting in water
vbd_adCVBD = 2700 # C_VBD determined during ballast
sigmaBallast = 22.8 # water density obtained during ballast
# Mission parameters
sigmaMinRequired = 16 # min water density required (lightest water expected)
sigmaMaxRequired = 27.5 # max water density required (densest water expected)



############################################################################# 

# libraries
import numpy as np
import matplotlib.pyplot as plt

deltaAD = vbd_adMax - vbd_adMin

# Functions
def ad_to_volume(vbd_ad_x):
    vol = vbdVolMax * (vbd_adMax - vbd_ad_x)/ deltaAD
    return vol

def volume_to_ad(vol):
    ad = vbd_adMax - vol * deltaAD / vbdVolMax
    return ad 

def relative_to_center_volume(vbd_ad_x):
    rvol = -vbdVolMax * (vbd_adMax - vbd_ad_x)/ deltaAD + ad_to_volume(vbd_adCVBD)
    return rvol


## CODE ##

# VBD volume vs sigma
#sigma_x = np.linspace(sigmaMinRequired,sigmaMax,100)
#volVBD_sigma_x = -CC_SIGMA * sigma_x + CC_SIGMA * sigmaBallast + vbdVolMax * (vbd_adMax - vbd_adCVBD) / deltaAD

# PLOT 1
# Sigma vs VBD AD
vbd_ad_x = np.arange(vbd_adMin, vbd_adMax, 1)  #np.linspace(vbd_adMin,vbd_adMax,100)

fig, ax = plt.subplots()

for i in range(-600,600+1,100):
    globals()['sigma_vbdAD_%s' % i] = vbdVolMax * (vbd_ad_x - vbd_adCVBD+i ) / (deltaAD * CC_SIGMA) + sigmaBallast
    if i ==0:
        ax.plot(vbd_ad_x,globals()['sigma_vbdAD_%s' % i], lw=1.25, color='b')
    else:
        ax.plot(vbd_ad_x,globals()['sigma_vbdAD_%s' % i], lw=0.25, color='grey')
        t = str(i) if i <= 0 else "+" + str(i)
        ax.annotate(t, xy=(vbd_adCVBD+i,sigmaBallast+0.1), fontsize=7, color='grey', rotation=40)


#sigma_vbdAD = vbdVolMax * (vbd_ad_x - vbd_adCVBD ) / (deltaAD * CC_SIGMA) + sigmaBallast
#sigma_vbdAD2 = vbdVolMax * (vbd_ad_x - (vbd_adCVBD+200) ) / (deltaAD * CC_SIGMA) + sigmaBallast
#sigma_vbdAD3 = vbdVolMax * (vbd_ad_x - (vbd_adCVBD-200) ) / (deltaAD * CC_SIGMA) + sigmaBallast

#fig, ax = plt.subplots()

#ax.plot(vbd_ad_x,sigma_vbdAD)
#ax.plot(vbd_ad_x,sigma_vbdAD2)
#ax.plot(vbd_ad_x,sigma_vbdAD3)

# determine min and max achievable sigmas
sigmaMinPossible = vbdVolMax * (vbd_adMin - vbd_adCVBD ) / (deltaAD * CC_SIGMA) + sigmaBallast
sigmaMaxPossible = vbdVolMax * (vbd_adMax - vbd_adCVBD ) / (deltaAD * CC_SIGMA) + sigmaBallast

# plt.legend(["CVBD ("+str(vbd_adCVBD)+")","CVBD+200 ("+str(vbd_adCVBD+200)+")" , "CVBD-200 ("+str(vbd_adCVBD-200)+")"], loc ="best")
plt.axvline(x = vbd_adCVBD, color = 'b', ls=':', lw=1 , label = 'CVBD') # sigma during ballast
plt.axhline(y = sigmaBallast, color = 'b',ls=':',lw=1 , label = 'ballast') # cvbd obtained with sigma ballast
ax.annotate("CVBD="+str(vbd_adCVBD), xy=(vbd_adCVBD-50,sigmaMinPossible+0.25), fontsize=6, color='b', rotation=90)

plt.axhline(y = sigmaMinRequired, color = 'm',ls='-.',lw=0.5 , label = 'minSigmaReq') # min sigma required
plt.axhline(y = sigmaMaxRequired, color = 'm',ls='-.',lw=0.5 , label = 'MaxSigmaReq') # max sigma required
ax.annotate("max water density: "+str(sigmaMaxRequired), xy=(vbd_adCVBD-1000,sigmaMaxRequired+0.25), fontsize=6, color='m')
ax.annotate("min water density: "+str(sigmaMinRequired), xy=(vbd_adCVBD+100,sigmaMinRequired+0.25), fontsize=6, color='m')
#plt.axvline(x = vbd_adMax, color = 'r', label = 'ADMax') # AD Max
#plt.vlines(vbd_adCVBD, 0, sigmaBallast)

# display equivalent VBD volume
ax.secondary_xaxis('top', functions=(ad_to_volume,volume_to_ad))

# configure axis plot 1
plt.xlim(vbd_adMin,vbd_adMax)
plt.ylim(sigmaMinPossible,sigmaMaxPossible)

plt.xticks(rotation = 25)
ax.set_xlabel('VBD AD count')
ax.set_ylabel(r'$\sigma$')
ax.set_title("SeaGlider Ballast chart - Operation ranges")

plt.locator_params(axis='x', nbins=15)
plt.locator_params(axis='y', nbins=30)

ax.grid(visible=True, which='both', axis='both', color='grey', linestyle=':', linewidth=0.5)


# PLOT 2
# Volume displacement relative to center - second axis
ax2 = ax.twinx()
#ax2.plot(vbd_ad_x,relative_to_center_volume(vbd_ad_x), ':r', lw=0.5)
ax2.set_ylabel('VBD displaced volume [cc]', color='r')
ax2.tick_params(axis='y', colors='red')

rvol = vbdVolMax * (vbd_adMax - vbd_ad_x)/ deltaAD - ad_to_volume(vbd_adCVBD)
ax2.fill_between(vbd_ad_x, rvol, alpha=0.2, color='r')
plt.locator_params(axis='y', nbins=20)

# Plot Vol max horizontal line vbd_ad_x=0
rvolMax = vbdVolMax * (vbd_adMax - vbd_adMin)/ deltaAD - ad_to_volume(vbd_adCVBD)
rvolMin = vbdVolMax * (vbd_adMax - vbd_adMax)/ deltaAD - ad_to_volume(vbd_adCVBD)
#plt.axhline(y = rvolMax, color = 'r',ls=':',lw=0.5 , label = 'volMax') # rel vol max
#plt.axhline(y = rvolMin, color = 'r',ls=':',lw=0.5 , label = 'volMin') # rel vol min
#vmaxText = str(round(rvolMax,0)) + 'cc'
#vminText = str(round(rvolMin,0)) + 'cc'
#ax2.annotate(vmaxText, xy=(vbd_adCVBD+100, rvolMax-30), color='r')
#ax2.annotate(vminText, xy=(vbd_adCVBD+100, rvolMin+8), color='r')
# adjust axis to align with sigma
plt.ylim(rvolMin,rvolMax)
#ax2.set_yticklabels([f"{(-1)*x}" for x in ax2.get_yticks()])

# VBD relative vol required to expose antenna
vol_antenna = rvolMax - 150 # this is the volume that remains usable for stratification
ax2.fill_between(vbd_ad_x,vol_antenna,rvolMax ,alpha=0.2, color='g')
ax2.annotate(str(int(vol_antenna)) + " cc (Vmax-150)", xy=(vbd_adCVBD+50,vol_antenna+30), color='g')
ax2.annotate("PUMP\nREGION", xy=(vbd_adMin+400, 100), fontsize=7, color='r')
ax2.annotate("BLEED\nREGION", xy=(vbd_adMax-400, -50), fontsize=7, color='r')
plt.gca().invert_yaxis()

# Annotate stroke %
stroke = 100*vbd_adCVBD/deltaAD
text = "Stroke=" + str(round(stroke,1)) + "% ->"
if stroke > 70:
    text = text + " glider is light"
elif stroke < 70:
    text = text + " glider is heavy"
else :
    text = text + " glider is perfect"

ax.annotate(text, xy=(vbd_adMin+100, sigmaBallast+0.5), fontsize=8)


plt.show()





