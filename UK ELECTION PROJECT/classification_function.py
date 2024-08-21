def classify(party):
    parties_to_look_for = ["Lab", "Con", "LD", "SNP", "SF"]
    if party in parties_to_look_for:
        return party
    else:
        return "OTHER"