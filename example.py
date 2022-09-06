from gamry.data import load_signals, filter_signals
from gamry import plot

signals = load_signals()

s1_02mm = filter_signals(signals, label='S1-0.2mm')
s1_05mm = filter_signals(signals, label='S1-0.5mm')
s1_1mm = filter_signals(signals, label='S1-1.0mm')
s2_02mm = filter_signals(signals, label='S2-0.2mm')
s2_05mm = filter_signals(signals, label='S2-0.5mm')
s2_1mm = filter_signals(signals, label='S2-1.0mm')
s5_1mm = filter_signals(signals, label='S5-1.0mm')

names = [
    'S1-0.2mm',
    'S1-0.5mm',
    'S1-1.0mm',
    'S2-0.2mm',
    'S2-0.5mm',
    'S2-1.0mm',
    'S5-1.0mm',
]

cnt = 0
for signals in [s1_02mm, s1_05mm, s1_1mm, s2_02mm, s2_05mm, s2_1mm, s5_1mm]:
    plot.eispot_bode(signals, names[cnt], 'Samples', theme='plain').show()
    cnt +=  1
