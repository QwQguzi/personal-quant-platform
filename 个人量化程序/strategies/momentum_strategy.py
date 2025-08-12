def generate_signal_momentum(mom_z):
    signal = (mom_z > 0).astype(int).fillna(0)
    return signal