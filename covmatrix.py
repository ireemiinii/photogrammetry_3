import matplotlib.pyplot as plt
import numpy as np


def AdjustmentResult(file1path, file2path):
    """
     This function compare the results in terms of sigma naught parameter correlations,
    and standard deviations of the points’ coordinates .

    Sample use: AdjustmentResult("coordinates1.txt", "coordinates2.txt")

    """
    # read the txt files
    file1 = open(file1path, 'r')
    file2 = open(file2path, 'r')

    # read all lines of files
    in_file = file1.readlines()
    in_file2 = file2.readlines()

    # split strings and return a list of strings
    data1 = [[float(i) for i in r.split()] for r in in_file]
    data2 = [[float(i) for i in r.split()] for r in in_file2]

    # takes the lists and returns an array that contains all the elements of the list
    data1 = np.array(data1)
    data2 = np.array(data2)
    x_size = data1.size

    data1 = data1.reshape(1, x_size)
    data2 = data2.reshape(1, x_size)
    A = np.vstack([data1, data2])

    # Create a variance/covariance matrix of observations
    def CovarianceMatrix(obs):
        mean_obs = np.mean(obs, axis=0)
        len_obs = obs.shape[0]
        obs = obs - mean_obs
        covariance_mat = obs.T.dot(obs) / len_obs
        return covariance_mat

    cov_mat = CovarianceMatrix(A)
    print("Variance-Covariance Matrix:", "\n", cov_mat)

    # Take the diagonal indices of the covariance matrix
    dia = np.diagonal(cov_mat)

    # Calculate a priori standard error of observation using the formula
    def Standard_Error(mat):
        se_of_o = np.sqrt(dia)
        return se_of_o

    s_e = Standard_Error(cov_mat)
    print("Standard Error of Observation:", "\n", s_e)

    # Calculate sigma naught using the formula
    def SigmaNaught(y):
        square_sigma_naught = sum(s_e) / (x_size - 1)
        sigma_naught = np.sqrt(square_sigma_naught)
        return sigma_naught

    sigma = SigmaNaught(s_e)
    print("Sigma Naught:", "\n", sigma)

    # Calculate correlation between observations
    def CorrelationCoff(x):
        cor_cof = cov_mat / np.sqrt(np.multiply.outer(dia, dia))
        return cor_cof

    corr = CorrelationCoff(dia)
    print("Correlation Coefficient:", "\n", corr)

    # Calculate a priori standard deviation of unit weight using the formula
    def StandardDeviation(z):
        stand_devi = np.sqrt(sum(dia) / x_size - 1)
        return stand_devi

    stdev=StandardDeviation(dia)
    print("Standard Deviation:", "\n", stdev)


    # Plot the correlation coeff.
    names = ['1', '2', '3', '4', '5', '6','7','8']
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(corr, vmin=-1, vmax=1)
    fig.colorbar(cax)
    ticks = np.arange(0, x_size, 1)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(names)
    ax.set_yticklabels(names)
    plt.show()



#  ------------------------- Sample use ----------------------------
# filepath --- > " Where are your first image coordinates, you should write its path."
# file_path --- > "Where are your second image coordinates, you should write its path."

if __name__ == "__main__":
    filepath = "coordinates1.txt"
    file_path = "coordinates2.txt"

    AdjustmentResult(filepath, file_path)
