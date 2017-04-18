import numpy as np
import xml
import subprocess

points = "40.34214 3.5625 -219.1813 -60.08951 3.5625 -219.1813 40.34214 3.5625 -202.3688 -60.08951 3.5625 -202.3688 -71.15786 3.5625 -213.4372 -71.15786 3.5625 -219.1813 -60.08951 3.5625 -249.9313 -71.08951 3.5625 -249.9313 -71.08951 3.5625 -219.1813"
points = points.split()
points = np.array(list(map(float, points))).\
    reshape(len(points)//3, 3)

idx = "1 0 0 2 2 3 3 4 4 5 6 1 7 6 8 7"
idx = idx.split()
idx = np.array(list(map(int, idx))).reshape(len(idx)//2, 2)

xs =0.0254 * points[idx, 0].T
zs =0.0254* points[idx, 2].T

points = "-212.999 4.6875 156.2939 -196.991 4.6875 159.6128 -227.6025 4.6875 148.9449 -239.8063 4.6875 138.0667 -248.7788 4.6875 124.4005 -253.9086 4.6875 108.8777 -254.8459 4.6875 92.5562 -251.527 4.6875 76.54823 -244.178 4.6875 61.94471 -233.2997 4.6875 49.74086 -219.6335 4.6875 40.76835 -204.1108 4.6875 35.63863 -187.7893 4.6875 34.7013 -171.7813 4.6875 38.02022 -157.1778 4.6875 45.36922 -144.9739 4.6875 56.24747 -136.0014 4.6875 69.91365 -130.8717 4.6875 85.43642 -129.9344 4.6875 101.7579 -133.2533 4.6875 117.7659 -140.6023 4.6875 132.3694 -151.4805 4.6875 144.5733 -165.1467 4.6875 153.5458 -180.6695 4.6875 158.6755"
points = points.split()
points = np.array(list(map(float, points))).\
    reshape(len(points)//3, 3)

idx = "1 0 0 2 2 3 3 4 4 5 5 6 6 7 7 8 8 9 9 10 10 11 11 12 12 13 13 14 14 15 15 16 16 17 17 18 18 19 19 20 20 21 21 22 22 23 23 1"
idx = idx.split()
idx = np.array(list(map(int, idx))).reshape(len(idx)//2, 2)

xs = np.append(xs, 0.0254 * points[idx, 0].T, 1)
zs = np.append(zs, 0.0254* points[idx, 2].T, 1)

points = "-208.3777 5.0625 124.8484 -200.6659 5.0625 128.0427 -215 5.0625 119.7669 -220.0815 5.0625 113.1447 -223.2758 5.0625 105.4329 -224.3653 5.0625 97.15706 -223.2758 5.0625 88.88127 -220.0815 5.0625 81.16946 -215 5.0625 74.54718 -208.3777 5.0625 69.46572 -200.6659 5.0625 66.27138 -192.3901 5.0625 65.18185 -184.1143 5.0625 66.27138 -176.4025 5.0625 69.46572 -169.7802 5.0625 74.54718 -164.6988 5.0625 81.16946 -161.5044 5.0625 88.88127 -160.4149 5.0625 97.15706 -161.5044 5.0625 105.4329 -164.6988 5.0625 113.1447 -169.7802 5.0625 119.7669 -176.4025 5.0625 124.8484 -184.1143 5.0625 128.0427 -192.3901 5.0625 129.1323"
points = points.split()
points = np.array(list(map(float, points))).\
    reshape(len(points)//3, 3)

idx = "1 0 0 2 2 3 3 4 4 5 5 6 6 7 7 8 8 9 9 10 10 11 11 12 12 13 13 14 14 15 15 16 16 17 17 18 18 19 19 20 20 21 21 22 22 23 23 1"
idx = idx.split()
idx = np.array(list(map(int, idx))).reshape(len(idx)//2, 2)

xs = np.append(xs, 0.0254 * points[idx, 0].T, 1)
zs = np.append(zs, 0.0254* points[idx, 2].T, 1)

points = "31.24837 38.6137 81.18934 31.24837 38.6137 41.40468 -11.77235 38.6137 81.18934 -11.77235 38.6137 41.40468 -43.43998 38.6137 41.40468 -43.43998 38.6137 -12.37988 2.782208 38.6137 -12.37988 8.216041 38.6137 -12.37988 8.216041 38.6137 18.88516 -18.05325 38.6137 18.88516 -18.05325 38.6137 24.71702 8.216041 38.6137 24.71702 8.216041 38.6137 41.40468"
points = points.split()
points = np.array(list(map(float, points))).\
    reshape(len(points)//3, 3)

idx = "1 0 0 2 2 3 3 4 4 5 5 6 6 7 7 8 9 8 10 9 11 10 11 12 12 1"
idx = idx.split()
idx = np.array(list(map(int, idx))).reshape(len(idx)//2, 2)

xs = np.append(xs, 0.0254 * points[idx, 0].T, 1)
zs = np.append(zs, 0.0254* points[idx, 2].T, 1)

def collide(x, z, vx, vz, ignore = -1):
    np.seterr(divide="ignore")
    vx = -vx
    vz = -vz
    trans_xs = xs - x
    trans_zs = zs - z
    x1 = trans_xs[0]
    x2 = trans_xs[1]
    z1 = trans_zs[0]
    z2 = trans_zs[1]

    denom = ((x1 - x2) * vz - (z1 - z2) * vx)

    t = ((-x2 * vz - -z2 * vx)) / denom
    a = ((x1 - x2) * -z2  - (z1 - z2) * - x2) / denom
    #print (t)
    #print(a)

    a [np.logical_not (np.logical_and(t > 0.001, np.logical_and(t < 1, a > 0)))] = 99
    if ignore != -1:
        a[ignore] = 99
    return np.argmin(a), np.min(a)

def reflect(vx, vz, n):
    #maths
    nz = xs[1][n] - xs[0][n]
    nx = -zs[1][n] + zs[0][n]

    mul = 1.8 * (nx * vx + nz * vz) / (nx * nx + nz * nz)

    return vx - mul * nx, vz - mul * nz

slow = .005
timestep = .01
def path(x,z, vx, vz):

    while vx * vx + vz * vz > slow * slow:
        n, tiem = collide(x, z, vx, vz)
        if tiem < timestep:
            subprocess.Popen(['play', '-q', '../boop.wav'])
            timeleft = timestep
            while tiem < timeleft:
                x += vx * tiem
                z += vz * tiem
                vx, vz = reflect(vx, vz, n)
                n, tiem = collide(x, z, vx, vz, n)

            x += vx * (timeleft)
            z += vz * (timeleft)
        else:
            x += vx * timestep
            z += vz * timestep

        l = np.sqrt(vx * vx + vz * vz)
        vx -= slow * vx/l
        vz -= slow * vz/l

        yield x, z
