from math import sqrt
import numpy as np
from Wavelets import Wavelet

class Daubechies40Wavelet(Wavelet):
  _waveLength = 40
  _dec_l = np.array([
  -2.9988364896157532e-10,
  4.05612705554717e-09,
  -1.8148432482976221e-08,
  2.0143220235374613e-10,
  2.633924226266962e-07,
  -6.847079596993149e-07,
  -1.0119940100181473e-06,
  7.2412482876637907e-06,
  -4.3761438621821972e-06,
  -3.7105861833906152e-05,
  6.7742808283730477e-05,
  0.00010153288973669777,
  -0.0003851047486990061,
  -5.3497598443404532e-05,
  0.0013925596193045254,
  -0.00083156217287724745,
  -0.003581494259744107,
  0.0044205423867663502,
  0.0067216273018096935,
  -0.013810526137727442,
  -0.0087893249245557647,
  0.032294299530119162,
  0.0058746818113949465,
  -0.061722899624668884,
  0.0056322468576854544,
  0.10229171917513397,
  -0.024716827337521424,
  -0.15545875070604531,
  0.039850246458519104,
  0.22829105082013823,
  -0.016727088308801888,
  -0.32678680043353758,
  -0.13921208801128787,
  0.36150229873889705,
  0.61049323893785579,
  0.47269618531033147,
  0.21994211355113222,
  0.063423780459005291,
  0.010549394624937735,
  0.00077995361366591117
  ]) * sqrt(2)
  _dec_h = np.array([
  -0.00077995361366591117,
  0.010549394624937735,
  -0.063423780459005291,
  0.21994211355113222,
  -0.47269618531033147,
  0.61049323893785579,
  -0.36150229873889705,
  -0.13921208801128787,
  0.32678680043353758,
  -0.016727088308801888,
  -0.22829105082013823,
  0.039850246458519104,
  0.15545875070604531,
  -0.024716827337521424,
  -0.10229171917513397,
  0.0056322468576854544,
  0.061722899624668884,
  0.0058746818113949465,
  -0.032294299530119162,
  -0.0087893249245557647,
  0.013810526137727442,
  0.0067216273018096935,
  -0.0044205423867663502,
  -0.003581494259744107,
  0.00083156217287724745,
  0.0013925596193045254,
  5.3497598443404532e-05,
  -0.0003851047486990061,
  -0.00010153288973669777,
  6.7742808283730477e-05,
  3.7105861833906152e-05,
  -4.3761438621821972e-06,
  -7.2412482876637907e-06,
  -1.0119940100181473e-06,
  6.847079596993149e-07,
  2.633924226266962e-07,
  -2.0143220235374613e-10,
  -1.8148432482976221e-08,
  -4.05612705554717e-09,
  -2.9988364896157532e-10,
  ]) * sqrt(2)
  _rec_l = np.array([
  0.00077995361366591117,
  0.010549394624937735,
  0.063423780459005291,
  0.21994211355113222,
  0.47269618531033147,
  0.61049323893785579,
  0.36150229873889705,
  -0.13921208801128787,
  -0.32678680043353758,
  -0.016727088308801888,
  0.22829105082013823,
  0.039850246458519104,
  -0.15545875070604531,
  -0.024716827337521424,
  0.10229171917513397,
  0.0056322468576854544,
  -0.061722899624668884,
  0.0058746818113949465,
  0.032294299530119162,
  -0.0087893249245557647,
  -0.013810526137727442,
  0.0067216273018096935,
  0.0044205423867663502,
  -0.003581494259744107,
  -0.00083156217287724745,
  0.0013925596193045254,
  -5.3497598443404532e-05,
  -0.0003851047486990061,
  0.00010153288973669777,
  6.7742808283730477e-05,
  -3.7105861833906152e-05,
  -4.3761438621821972e-06,
  7.2412482876637907e-06,
  -1.0119940100181473e-06,
  -6.847079596993149e-07,
  2.633924226266962e-07,
  2.0143220235374613e-10,
  -1.8148432482976221e-08,
  4.05612705554717e-09,
  -2.9988364896157532e-10,
  ]) * sqrt(2)
  _rec_h = np.array([
  -2.9988364896157532e-10,
  -4.05612705554717e-09,
  -1.8148432482976221e-08,
  -2.0143220235374613e-10,
  2.633924226266962e-07,
  6.847079596993149e-07,
  -1.0119940100181473e-06,
  -7.2412482876637907e-06,
  -4.3761438621821972e-06,
  3.7105861833906152e-05,
  6.7742808283730477e-05,
  -0.00010153288973669777,
  -0.0003851047486990061,
  5.3497598443404532e-05,
  0.0013925596193045254,
  0.00083156217287724745,
  -0.003581494259744107,
  -0.0044205423867663502,
  0.0067216273018096935,
  0.013810526137727442,
  -0.0087893249245557647,
  -0.032294299530119162,
  0.0058746818113949465,
  0.061722899624668884,
  0.0056322468576854544,
  -0.10229171917513397,
  -0.024716827337521424,
  0.15545875070604531,
  0.039850246458519104,
  -0.22829105082013823,
  -0.016727088308801888,
  0.32678680043353758,
  -0.13921208801128787,
  -0.36150229873889705,
  0.61049323893785579,
  -0.47269618531033147,
  0.21994211355113222,
  -0.063423780459005291,
  0.010549394624937735,
  -0.00077995361366591117,
  ]) * sqrt(2)