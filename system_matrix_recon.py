import numpy as np

class SM_recon(object):
    def __init__(self,Message,Iterations=20,Lambda=1e-6):
        self._Image_data = []
        self._Iterations = Iterations
        self._Lambda = Lambda
        self._ImageRecon(Message['Measurement']['Auxiliary_Signal'],Message['Measurement']['Measure_Signal'],Message['Measurement']['Voxel_Number'])

    def get_Image(self):
        return self._Image_data
    
    def _ImageRecon(self,A,b,size):
        self._Image_data.append(self._Kaczmarz(A,b,self._Iterations,self._Lambda))
        self._Image_data.append(self._ImageReshape(self._Image_data[0],size))

        
    def _ImageReshape(self,c,size):
        x = size[0]
        y = size[1]
        z = 1 if len(size) <= 2 else size[2]
        if x == 1 or y == 1 or z == 1:
            c = np.real(np.reshape(c,(x,y)))
            c = c[1:-1,1:-1]
            c = c / np.max(c)
            return c, None, None
        else:
            c = np.real(np.reshape(c,(x,y,z)))
            Ixy = np.zeros((x,y))
            Iyz = np.zeros((y,z))
            Ixz = np.zeros((x,z))
            for i in range(x-1):
                for j in range(x-1):
                    Ixy[i,j] = max(c[i,j,:])
                    Ixz[i,j] = max(x[i,:,j])
                    Iyz[i,j] = max(x[:,i,j])
            Ixy /= np.max(Ixy)
            Iyz /= np.max(Iyz)
            Ixz /= np.max(Ixz)

            return np.real(Ixy), np.real(np.transpose(Ixz)), np.real(np.transpose(Iyz)) 
    
    def _RowEnergy(self,A):
        M = A.shape[0]
        energy = np.zeros(M, dtype = np.double)

        for m in range(M):
            energy[m] = np.linalg.norm(A[m,:])
        return energy
    
    def _Kaczmarz(self,A,b,iteration = 10,lambd = 0,enforceReal = False, enforcePositive = False, shuffle = False):
        M = A.shape[0]
        N = A.shape[1]

        x = np.zeros(N, dtype = b.dtype)
        residual = np.zeros(M, dtype =x.dtype)

        energy = self._RowEnergy(A)

        rowIndexCycle = np.arange(0,M)

        if shuffle:
            np.random.shuffle(rowIndexCycle)

        lambdIter = lambd

        for l in range(iteration):
            for m in range(M):
                k = rowIndexCycle[m]
                if energy[k] > 0:
                    beta = (b[k] - A[k,:].dot(x) - np.sqrt(lambdIter) * residual[k]) / (energy[k] ** 2 + lambd)

                    x[:] += beta * A[k,:].conjugate()

                    residual[k] += np.sqrt(lambdIter) * beta

            if enforceReal and np.iscomplexobj(x):
                x.imag = 0
            if enforcePositive:
                x = x * (x.real > 0)

        return x  
    
    
