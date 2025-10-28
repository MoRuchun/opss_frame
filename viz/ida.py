"""
IDA plotter. Should be run before postprocessor
"""
import matplotlib.pyplot as plt


class IDA:
    def __init__(self):

        # Default color patterns
        self.color_grid = ['#840d81', '#6c4ba6', '#407bc1', '#18b5d8', '#01e9f5',
                           '#cef19d', '#a6dba7', '#77bd98', '#398684', '#094869']
        self.grayscale = ['#111111', '#222222', '#333333', '#444444', '#555555',
                          '#656565', '#767676', '#878787', '#989898', '#a9a9a9']
        self.FONTSIZE = 10
        self.markers = ["o", "v", "^", "<", ">", "s", "*", "D", "+", "X", "p"]

    def disp_vs_im(self, data):
        """
        IDA plotter, displacement versus Intensity Measure
        :param data: pickle
        :return: figure object
        """
        disp_range = data["mtdisp"]
        im_qtile = data["im_qtile"]
        im = data["im"]
        im_spl = data["im_spl"]
        mtdisp = data["disp"]

        fig, ax = plt.subplots(figsize=(5, 3), dpi=200)
        for rec in range(im_spl.shape[0]):
            plt.plot(mtdisp[rec], im[rec], self.grayscale[-1], marker='o', linewidth=0.2, markersize=2)
            plt.plot(disp_range, im_spl[rec], self.grayscale[-1], linewidth=0.2)
        plt.plot(disp_range, im_qtile[2], color=self.color_grid[8], label="84th quantile", ls="-.")
        plt.plot(disp_range, im_qtile[1], color=self.color_grid[6], label="50th quantile", ls="--")
        plt.plot(disp_range, im_qtile[0], color=self.color_grid[3], label="16th quantile", ls="-")
        plt.xlim(0.0, max(disp_range))
        plt.ylim(0.0, max(im_qtile[2]) + 0.5)
        plt.xlabel("Top displacement, [m]", fontsize=self.FONTSIZE)
        plt.ylabel("Sa, [g]", fontsize=self.FONTSIZE)
        plt.rc('xtick', labelsize=self.FONTSIZE)
        plt.rc('ytick', labelsize=self.FONTSIZE)
        plt.grid(True, which="major", ls="--", lw=0.8, dashes=(5, 10))
        plt.legend(frameon=False, loc='upper right', fontsize=self.FONTSIZE, bbox_to_anchor=(1.5, 1))

        return fig

