def get_median(buckets, row):
    ordered = list(buckets.keys())
    N = row[ordered].sum()
    C = 0
    i = 0
    while C <= N/2 and i<=len(buckets.keys())-1:
        C += int(row[ordered[i]])
        i += 1
    i = i-1
    if i == 0:
        median = list(buckets.values())[0][1]
    elif C == 0: 
        median =0
    elif i == len(buckets.keys())-1:
        median = list(buckets.values())[-1][0]
    else: 
        C = C - int(row[ordered[i]])
        L = buckets[ordered[i]][0]
        F = int(row[ordered[i]])
        W = buckets[ordered[i]][1] - buckets[ordered[i]][0]
        median = L + (N/2 - C)*W/F
    return median