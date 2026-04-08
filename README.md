# GraphMaker

CLI, multiplatform data plotting and linear regression tool. Built natively for the Unix terminal, GraphMaker parses laboratory CSV data, calculates linear regression using 128-bit floating-point math, and generates publication-ready graphs.

By default, GraphMaker runs completely headless and features saving plots with incrementing names (`fig01.png`, `fig02.png`, etc.).

## Requirements & Installation

### Linux
GraphMaker requires Python 3, `numpy`, and `matplotlib`. For the highest quality fonts, a local LaTeX distribution is highly recommended.

**1.1 Fedora**
```
sudo dnf install python3 python3-pip
```
optional:
```
sudo dnf install texlive-scheme-full
```
**1.2 Arch Linux**
```
sudo pacman -S python python-pip
```
optional:

```
sudo pacman -S texlive-full
```

**1.3 Debian**
```
sudo apt update
```
```
sudo apt install python3 python3-pip
```
optional:

```
sudo apt install texlive-full dvipng ghostscript
```
**2. Install Python libraries**
```
pip3 install numpy matplotlib
```

### Windows
Figure it out yourself. 

---

## Quick Setup (Global Command)

To run GraphMaker from any folder on your system without typing `python3 path/to/graphmaker.py`, copy a bash wrapper and script to your home directory:

1. Copy scripts:
```
cp graphmaker ~/.bin/
```
```
cp graphmaker.py ~/.bin/
```

2. Make it executable:
```
chmod +x ~/.bin/graphmaker
```

3. Refresh your shell
```
source ~/.bashrc
```
or
```
source ~/.zshrc
```
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
* `--no-tex` : Disable LaTeX font rendering (required for machines without TeX installed).
* `-le`, `--legend` : Show the legend box on the graph (hidden by default).

### Label & Scaling Flags
* `-xl`, `--xlabel` : Custom label for the X axis (Default: "x").
* `-yl`, `--ylabel` : Custom label for the Y axis (Default: "y").
* `-xe`, `--x_exp` : Divide X data by 10^exp for the graph (`-xe 3` converts meters to kilometers on the plot, while keeping terminal math in base SI units).
* `-ye`, `--y_exp` : Divide Y data by 10^exp for the graph.
* `-p`, `--padding` : Padding multiplier for the regression line extension (Default: 0.1).

### Examples

**1. The Quick Check (Silent)**
Reads a single file, calculates linear regression, and saves `fig01.png` in the current directory.
```
graphmaker -f data.csv -l
```
**2. Interactive Mode with Labels**
Opens the Matplotlib GUI window and sets custom axis labels.
```
graphmaker -f curietemp.csv -l -xl "Inductance [H]" -yl "Temperature [K]" --show
```
**3. Multi-File Comparison with Unit Scaling & Legend**
Plots three datasets on the same graph, scales the X-axis by 10^-3 (to show millimeters instead of meters), customizes the legend names, toggles the legend ON, and saves silently.
```
graphmaker -f data1.csv data2.csv data3.csv -n "Spring A" "Spring B" "Spring C" -xe -3 -xl "Distance [mm]" -le
```
**4. The "No LaTeX" Fallback**
If you are running this on a fresh machine that doesn't have TeX Live installed, use this flag to prevent crashes and fall back to standard fonts.
```
graphmaker -f data.csv --no-tex --show
```
