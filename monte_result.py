import importlib.util
import numpy as np
import glob
import configparser as cg

config = cg.ConfigParser()
config.read('config.ini')

lumpath = config['COMMON']['lum_path']
if not lumpath:
    raise ValueError('Lumerical API path is empty, please update it in config.ini!')

filepath = config['MONTE_ANALYSIS']['filepath']
if not filepath:
    raise ValueError('No basis file path provided, please update it in config.ini!')
outpath = config['MONTE_ANALYSIS']['outpath']
outname = config['MONTE_ANALYSIS']['outname']
if not outname:
    outname = "monte"

spec_lin = importlib.util.spec_from_file_location('lumapi', lumpath)
lumapi = importlib.util.module_from_spec(spec_lin)
spec_lin.loader.exec_module(lumapi)

with lumapi.FDTD(hide=True) as fdtd:
    filelist = glob.glob(filepath+"*.fsp")
    filelist = sorted(filelist, key=lambda x: int(x.split('_')[-1].partition('.')[0]))
    xpos = []
    ypos = []
    srcphi = []
    maxpur = []
    restrans = []
    for file in filelist:
        fdtd.load(file)
        fdtd.select("source")
        xpos.append(fdtd.get("x"))
        ypos.append(fdtd.get("y"))
        srcphi.append(fdtd.get("phi"))

        purcell = fdtd.getresult("source", "purcell")
        maxpur.append(np.max(purcell['purcell']))
        indmaxpur = np.argmax(purcell['purcell'])
        maxpurwvl = purcell['lambda'][indmaxpur]
        maxpurf = purcell['f'][indmaxpur]

        trans = fdtd.getresult("PhC_T", "T")
        idx = (np.abs(trans['lambda'] - maxpurwvl)).argmin()
        restrans.append(trans['T'][idx])

    data = np.array([xpos, ypos, srcphi, maxpur, restrans]).T
    np.savetxt(outpath+outname+'.csv', data, delimiter=",", header="X, Y, Phi, Purcell, Transmission")