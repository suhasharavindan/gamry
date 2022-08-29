from gamry.data import load_signals
from gamry import plot

signals = load_signals()

plot.eispot_bode(signals, 'Test', 'Sample')
