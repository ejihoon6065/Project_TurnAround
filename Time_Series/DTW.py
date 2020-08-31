import numpy as np
import pandas as pd

""" my dtw """
def mydtw (x1, x2, window_size):
    x1 = x1[~np.isnan(x1)]
    x2 = x2[~np.isnan(x2)]
    if len(x1)>=len(x2):
        xx1 = x2; xx2 = x1
    else:
        xx1 = x1; xx2 = x2
    x1 = xx1; x2 = xx2;
    nx = len(x1); ny = len(x2)
    dmatrix = np.repeat(0, nx*ny).reshape(nx, ny)
    slope = min([nx/ny, ny/nx])
    nmax = max([nx, ny])
    row = np.round(slope*np.round(range(1,nmax+1)))
    col = np.round(range(1,nmax+1))
    
    for i in range(nx):
        r = col[row==(i+1)]
        if len(r)!=0:
            rmin = min(r); rmax = max(r)
            rlist = np.round(range(rmin-window_size), (rmax+window_size)+1)
            r = set(range(1, rmax+1))-set(rlist)
            for rr in r:
                dmatrix[i, int(rr-1)] = 1
    dmatrix[0,0] = 0; dmatrix[nx-1, ny-1] = 0
    np.abs(np.repeat(x1[0], ny))
    row1 = np.cumsum(np.abs(np.repeat(x1[0], ny)-x2))[np.where(dmatrix[0,]==0)[0]]
    col1 = np.cumsum(np.abs(x1-np.repeat(x2[0], nx)))[np.where(dmatrix[:,0]==0)[0]]
    dvalue = np.repeat(np.inf, nx*ny).reshape(nx, ny)
    dvalue[0, range(len(row1))] = row1;
    dvalue[range(len(col1)), 0] = col1;
    
    for i in range(1, nx):
        for j in range(1, ny):
            if (dmatrix[i,j]!=1):
                d = np.abs(x1[i]-x2[j])
                dist = [dvalue[i-1, j-1]+2*d, dvalue[i-1, j]+d, dvalue[i, j-1]+d]
                dist = min(dist)
                dvalue[i, j] = dist
    route_row, route_col = np.where(dmatrix!=1)
    distance = dvalue[max(route_row), max(route_col)]
    n = max(route_row)+max(route_col)+2
    normalizedDistance = distance/n
    
    result = { 'distanceMatrix' : dvalue, 'distance' : distance, 'normalizedDistance' : normalizedDistance }
    return result
[출처] DTW(Dynamic Time Wrapping) 방법에 대해 알아봅시다(R, Python 코드 첨부)|작성자 plastic code
