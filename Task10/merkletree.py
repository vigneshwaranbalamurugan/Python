import hashlib

def merkle_root(transactions):
    if not transactions:  
        return "0"  

    hashes = [hash(tx) for tx in transactions]
    while len(hashes) > 1:
        temp = []
        for i in range(0, len(hashes), 2):
            if i + 1 < len(hashes):
                temp.append(hash(hashes[i] + hashes[i + 1]))
            else:
                temp.append(hash(hashes[i]))
        hashes = temp
    return hashes[0]