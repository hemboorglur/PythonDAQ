## NOAH ZEEMAN - 15494365
## NSP2 - ECPC - basisscript voor het experiment "drift"
## 3 Nov '26

# importeren van benodigde packages
import pyvisa
import matplotlib
matplotlib.use("WebAgg")
import matplotlib.pyplot as plt


# instellen van een webserver waar matplotlib de grafieken kan weergeven
plt.rcParams["webagg.address"] = "192.168.2.166"
plt.rcParams["webagg.port"] = 8988
plt.rcParams["webagg.open_in_browser"] = False
