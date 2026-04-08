# GraphMaker

CLI, multiplatform data plotting and linear regression tool. Built natively for the Unix terminal, GraphMaker parses laboratory CSV data, calculates linear regression using 128-bit floating-point math, and generates publication-ready graphs.

By default, GraphMaker runs completely headless and features saving plots wiht incementing names (`fig01.png`, `fig02.png`, etc.).

## Requirements & Installation

### Linux
GraphMaker requires Python 3, `numpy`, and `matplotlib`. For the highest quality fonts, a local LaTeX distribution is highly recommended.

**1.1 Fedora**
`sudo dnf install python3 python3-pip`
optional
`sudo dnf install texlive-scheme-full`

**1.2 Arch Linux**
`sudo pacman -S python python-pip texlive-full`

**1.3 Debian**
`sudo apt update`
`sudo apt install python3 python3-pip texlive-full dvipng ghostscript`

**2. Install Python libraries**
`pip3 install numpy matplotlib`

### Windows
Figure it out yourself. 

---

## Quick Setup (Global Command)

To run GraphMaker from any folder on your system without typing `python3 path/to/graphmaker.py`, copy a bash wrapper with script you your home directory:

1. Copy sctipts:
   `cp graphmaker ~/.bin/`
   `cp graphmaker.py ~/.bin/`
   
2. Make it executable:
   `chmod +x ~/.bin/graphmaker`

3. Refresh your shell
    `source ~/.bashrc`
    `source ~/.zshrc`
---

## CSV Format Expectation

GraphMaker automatically detects your data format based on the number of columns in your `.csv` file. **The first row is always skipped** (reserved for headers).

* **2 Columns:** `X, Y` (Uncertainties default to 0)
* **4 Columns:** `X, X_err, Y, Y_err` 

---

## Usage & Examples

Call `graphmaker` followed by your desired flags. 

### Core Flags
* `-f`, `--files` : Path to one or more CSV files (Required).
* `-n`, `--names` : Custom names for the legend. Defaults to the filename if omitted.
* `-l`, `--linear` : Calculate and plot linear regression.
* `--show` : Open the interactive GUI instead of saving silently to disk.
* `--no-tex` : Disable LaTeX font rendering (rquired for machines without TeX installed).

### Label & Scaling Flags
* `--xlabel`, `--ylabel` : Custom axis labels.
* `--x_exp`, `--y_exp` : Divide data by 10^exp for the graph (`--x_exp 3` converts meters to kilometers on the plot, while keeping terminal math in base SI units).
* `-p`, `--padding` : Padding multiplier for the regression line extension (Default: 0.1).

### Examples

**1. The Quick Check (Silent)**
Reads a single file, calculates linear regression, and saves `fig01.png` in the current directory.
`graphmaker -f data.csv -l`

**2. Interactive Mode with Labels**
Opens the Matplotlib GUI window and sets custom axis labels.
`graphmaker -f curietemp.csv -l --xlabel "Inductance [H]" --ylabel "Temperature [K]" --show`

**3. Multi-File Comparison with Unit Scaling**
Plots three datasets on the same graph, scales the X-axis by 10^-3 (to show millimeters instead of meters), customizes the legend names, and saves silently.
`graphmaker -f data1.csv data2.csv data3.csv -n "Spring A" "Spring B" "Spring C" --x_exp -3 --xlabel "Distance [mm]"`

**4. The "No LaTeX" Fallback**
If you are running this on a fresh machine that doesn't have TeX Live installed, use this flag to prevent crashes and fall back to standard fonts.
`graphmaker -f data.csv --no-tex --show`

