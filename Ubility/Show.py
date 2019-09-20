import matplotlib.pyplot as plt


def ShowFromPd(pd, x_index, y_index, value_index):
    sub_pd = pd[[x_index, y_index, value_index]]
    # sub_array = sub_pd.getvalues()

    plt.plot(sub_pd[x_index])

