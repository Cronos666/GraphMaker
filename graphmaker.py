import argparse
import sys
import os
import numpy as np
import matplotlib

if '--show' not in sys.argv:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter



#DATA HANDLER
class Data:
    def __init__(self, name, x_data, y_data, x_err=None, y_err=None, linear=False):

        self.name = str(name)
        self.x_data = np.asarray(x_data, dtype=np.float128)
        self.y_data = np.asarray(y_data, dtype=np.float128)
        if x_err is None:
            self.x_err = np.zeros(len(self.x_data), dtype=np.float128)
        else:
            self.x_err = np.asarray(x_err, dtype=np.float128)
        
        if y_err is None:
            self.y_err = np.zeros(len(self.y_data), dtype=np.float128)
        else:
            self.y_err = np.asarray(y_err, dtype=np.float128)


        self.linear=linear

        #LINEAR REG
        self.a = None
        self.da = None
        self.b = None
        self.db = None
        self.r = None

        if linear:
            self.linreg()

    def linreg(self):
        x = self.x_data
        y = self.y_data
        n = len(x)
        
        if n<3:
            raise ValueError(f"Linear regression needs at least 3 data points. There was only {n} provided.")


        sumX = np.sum(x)
        sumY = np.sum(y)
        sumXX = np.sum(x * x)
        sumXY = np.sum(x * y)

        denom = n*sumXX - (sumX*sumX)

        a = ((n*sumXY) - (sumX*sumY))/denom
        b = ((sumXX*sumY) - (sumX*sumXY))/denom

        sumAXB = np.sum( (y - (a*x +b))**2)

        da = np.sqrt((n*sumAXB)/ ((n-2)*denom))
        db = da*np.sqrt(sumXX/n);
    
        meanX = sumX / n
        meanY = sumY / n

        r1 = np.sum((x - meanX) * (y - meanY))
        r2 = np.sum((x - meanX)**2)
        r3 = np.sum((y - meanY)**2)
        
        rd = np.sqrt(r2*r3)
        if rd == 0:
            r = np.nan
        else:
            r = r1/rd

        #WRITE TO CLASS
        self.a = a
        self.da = da
        self.b = b
        self.db = db
        self.r = r

def plotf(data_array, x_label, y_label, x_exp=0, y_exp=0,
          use_tex_font='True',font_size=18,
          graph_x=10, graph_y=6, show_plot=False,
          msize=8, barsize=5, padding_m = 0.5):

    #FONT
    if(use_tex_font):
        plt.rcParams['text.usetex'] = True
        plt.rcParams['text.latex.preamble'] = r'\usepackage{mathptmx}'
        plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.size'] = font_size

    #COLOR PALETE
    color=[
        '#000000', # Black
        '#f37b21', # Half-Life Orange
        '#7d00ff', # Cool Purple
        '#0000ff', # Blue
        '#ff00ff'  # Magenta
    ]

    #FIG
    fig, ax = plt.subplots(figsize=(graph_x, graph_y))
    ax.grid(True, linestyle='-', alpha=0.7)

    #LABELS
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    
    #EXPONENTS
    x_scale = np.float128(10**x_exp)
    y_scale = np.float128(10**y_exp)

    for n, data in enumerate(data_array):
        c = color[n%len(color)]

        ax.errorbar(
                data.x_data/x_scale,
                data.y_data/y_scale,
                xerr=data.x_err/x_scale,
                yerr=data.y_err/y_scale,
                fmt='s',
                color=c, 
                markerfacecolor=c,
                markersize=msize,
                capsize=barsize,
                capthick=1.5,
                linestyle='None',
                label=data.name
                )

        if data.linear:
            x_min = min(data.x_data)
            x_max = max(data.x_data)
            padding = (x_max - x_min)*padding_m
            
            x_line = np.linspace(x_min - padding, x_max + padding, 100)
            y_line = data.a * x_line + data.b

            ax.plot(x_line/x_scale, y_line/y_scale, '--', color=c, linewidth=2)
    
    ax.legend(loc='best')
    plt.tight_layout()
    if show_plot:
        plt.show()
    else:
        counter = 1
        filename = f"fig{counter:02d}.png"
        while (os.path.exists(filename)):
            counter+=1
            filename = f"fig{counter:02d}.png"

        plt.savefig(filename, dpi=300)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="GraphMaker: Data plotting tool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('-f', '--files', type=str, nargs='+', required=True, 
                        help="Path to one or more CSV file")

    parser.add_argument('-n', '--names', type=str, nargs='+', help="Names of datasets")
    parser.add_argument('-xl', '--xlabel', type=str, default="x", help="Label for the X axis")
    parser.add_argument('-yl', '--ylabel', type=str, default="y", help="Label for the Y axis")

    parser.add_argument('-xe', '--x_exp', type=int, default=0, help="X axis exponent")
    parser.add_argument('-ye', '--y_exp', type=int, default=0, help="Y axis exponent")

    parser.add_argument('-l', '--linear', action='store_true', help="Calculate linear regression")
    parser.add_argument('-p', '--padding', type=float, default=0.1, help="Padding multiplier for the regression line")
    
    parser.add_argument('--show', action='store_true', help="Show GUI")

    parser.add_argument('--no-tex', action='store_false', dest='use_tex', help="Disable LaTeX font rendering")

    args = parser.parse_args()

    #IMPORT CSVs
    datasets = []

    for i, file_path in enumerate(args.files):
        try:
            raw_data = np.loadtxt(file_path, delimiter=',', skiprows=1)
        except FileNotFoundError:
            print(f"Error: Could not find the file '{file_path}'. Skipping file")
            continue # Skip to the next file instead of crashing the whole script
        except ValueError as e:
            print(f"Error reading '{file_path}': {e}. Skipping file")
            continue

        num_columns = raw_data.shape[1]
        
        if (num_columns >= 4):
            x = raw_data[:, 0]
            y = raw_data[:, 2]
            x_err = raw_data[:, 1]
            y_err = raw_data[:, 3]
        elif (num_columns > 1):
            x = raw_data[:,0]
            y = raw_data[:,1]
            x_err = None
            y_err = None
        else:
            print("Wrong CSV formatiing. Skipping file")
            continue

        if args.names and i < len(args.names):
            current_name = args.names[i]
        else:
            current_name = file_path.replace('.csv', '')

        try:
            dataset = Data(
                name=current_name,
                x_data=x,
                y_data=y,
                x_err=x_err,
                y_err=y_err,
                linear=args.linear
            )
            datasets.append(dataset) # Add the finished object to our list
        except ValueError as e:
            print(f"Error processing '{file_path}': {e}")

    if len(datasets) == 0:
        print("Error: No valid datasets were loaded.")
        sys.exit(1)

    if args.linear:
        for d in datasets:
            if d.a is not None:
                print(f"\n--- Linear Regression Results ({d.name}) ---")
                print(f"a  = {d.a:.8f} +/- {d.da:.8f}")
                print(f"b  = {d.b:.8f} +/- {d.db:.8f}")
                print(f"r  = {d.r:.8f}")
    #EXECUTION           
    plotf(datasets, args.xlabel, args.ylabel, args.x_exp, args.y_exp, show_plot=args.show,padding_m=args.padding, use_tex_font=args.use_tex)
