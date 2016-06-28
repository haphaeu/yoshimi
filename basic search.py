from OrcFxAPI import *
model = Model()
env = model.environment
env.WaveType = 'Jonswap'
env.WaveSearchFrom = 10800.0
env.WaveSearchDuration = 10800.0
model.SaveWaveSearchSpreadsheet('Example Search.xls')
