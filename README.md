# GraphMaker

CLI, multiplatform data plotting and linear regression tool. Built natively for the Unix terminal, GraphMaker parses laboratory CSV data, calculates linear regression using 128-bit floating-point math, and generates publication-ready graphs.

By default, GraphMaker runs completely headless and features saving plots with incrementing names (`fig01.png`, `fig02.png`, etc.).

## Requirements & Installation

### Linux
GraphMaker requires Python 3, `numpy`, and `matplotlib`. For the highest quality fonts, a local LaTeX distribution is highly recommended.

**1.1 Fedora**
`sudo dnf install python3 python3-pip`
optional:
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

To run GraphMaker from any folder on your system without typing `python3 path/to/graphmaker.py`, copy a bash wrapper and script to your home directory:

1. Copy scripts:
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
* `--no-tex` : Disable LaTeX font rendering (required for machines without TeX installed).
* `-le`, `--legend` : Show the legend box on the graph (hidden by default).

### Label & Scaling Flags
* `-xl`, `--xlabel` : Custom label for the X axis (Default: "x").
* `-yl`, `--ylabel` : Custom label for the Y axis (Default: "y").
* `-xe`, `--x_exp` : Divide X data by 10^exp for the graph (
