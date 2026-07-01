def classify_dataset(S: float, E: float, tau_s: float = 0.0, tau_e: float = 0.5) -> str:
    if S <= tau_s:
        return "Void"
    elif E <= tau_e:
        return "Fragile"
    else:
        return "Reliable"
