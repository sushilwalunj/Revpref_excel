# **Revealed Preference Analysis Toolkit for Experimental Economics Data**

A robust Python toolkit for non-parametric analysis of consumer choice data, specifically designed for datasets from economics experiments. This script automates reading complex data files, applying revealed preference tests (GARP, SARP, WARP), calculating the Afriat Efficiency Index, and generating a clean summary report.

## **The Problem This Solves**

Economics experiments often produce large, stacked CSV files where choice data from numerous subjects—each making a series of decisions—is appended one after another. Manually separating and analyzing the data for each individual is tedious and error-prone.

This toolkit streamlines that entire workflow. It intelligently parses the source file, automatically detects the number of subjects and goods, runs all necessary calculations, and compiles a final, publication-ready report.

## **Key Features**

* **Comprehensive Revealed Preference Tests**:  
  * Counts violations of the **Generalized Axiom of Revealed Preference (GARP)**.  
  * Counts violations of the **Strong Axiom of Revealed Preference (SARP)**.  
  * Counts violations of the **Weak Axiom of Revealed Preference (WARP)**.  
* **Efficiency Measurement**:  
  * The Afriat Efficiency Index (CCEI) is used to measure the severity of GARP violations, where a value of 1.0 reflects perfect consistency with rational choice and no GARP violations. Lower values indicate the extent to which budget constraints would need to be relaxed to eliminate all observed violations. For instance, a CCEI score of 0.90 means that the observed choices are 90% consistent with GARP, and a 10% relaxation of the budget would be sufficient to remove all violations.  
* **Intelligent Data Processing**:  
  * **Automatically detects** the number of subjects and goods directly from your CSV file.  
  * Reads and parses stacked CSV files containing data for multiple subjects.  
  * Gracefully handles empty rows or separator lines within the CSV.  
* **Report Generation**:  
  * Creates a final summary report in an Excel (.xlsx) file, with each row corresponding to a single subject's complete results.

## **Installation**

#### **For Windows:**

Use the RevPref\_Tool.exe file for windows.  
Once you extract the files, simply double click on the RevPref\_Tool.exe file.

#### **For MacOS:**

Use the RevPref\_Tool.app file for windows.  
Once you extract the files, simply double click on the RevPref\_Tool.exe file.

#### **For Linux:**

Use the revpref\_tool.exe file for windows.  
Once you extract the files, simply double click on the RevPref\_Tool.exe file.

If you wish to run the script using python, refer to the steps below.  
\[**Note:** This script requires Python 3.12+ and a few common libraries.\]

1. **Install Python**: If you don't have it, download Python from [python.org](https://python.org).  
2. **Install Libraries**: Open your terminal or command prompt and install the required packages using pip.  
   pip install numpy openpyxl

## **Input Data Format (Crucial\!)**

The script requires two inputs: a **Quantity Data File** (a CSV file) and a **Price Matrix** (entered in the terminal).

### **1\. Quantity Data (CSV File)**

The script is designed to parse a CSV file where quantity data for multiple subjects is stacked vertically in clean blocks.

* The file should **only contain the numerical quantity data**.  
* Each subject's data must be in a contiguous block.  
* The number of rows in each block must be the same for all subjects.  
* Empty rows or rows with just commas (separators) between subject blocks will be automatically ignored.

**Example\_Quantities.csv:**

An experiment with **N subjects**, each making **2 choices** (observations) over **11 goods**.

1,3  
2,2  
2,3  
2,2  
2,4  
2,3  
3,1  
2,2  
2,4  
2,3  
3,2  
,  
1,3  
2,2  
2,3  
2,2  
3,2  
3,2  
0,2  
4,1  
3,3  
4,2  
3,2  
,  
\# ...and so on for more subjects...  
If you want to generate a CSV file, ensure that your data is in the format similar to the image below.  
![][image1]  
The above example is created using Microsoft Excel. From this image it can be inferred that there are 3 participants with 11 observations for 2 goods, hence a 11 x 2 matrix for 3 participants. Now each participant is separated by a blank unmerged row. Once the excel file is ready you can go to File \-\> Save As \-\> select your location of storage \-\> Give the save type as ‘CSV (Comma delimited)’.    
If using Microsoft Excel you need not worry about reconverting your file to xlsx format for modifying the file, you can simply open the file and make changes.  
However, if viewing outside of a spreadsheet application, the csv file will look like the following image.  
![][image2]  
The above image is from when the CSV file is opened using Notepad application (Microsoft’s default notepad application). 

### **2\. Price Matrix (Command-Line Input)**

* After the script reads your quantity file, you will be prompted to enter the prices.  
* This price matrix is assumed to be **constant for all subjects**.  
* Its dimensions must match the data from the quantity file. For the example above, you would need to enter a **11 x 2** price matrix.  
* Example Price matrix:

      15 5

      10 5

      15 5

      5 5

      10 5

      5 5

      5 15

      5 10

      5 5

      5 10

      5 15

### **3\. Quantity Matrix (Command-Line Input)**

* After you select the Manual Input option, you will be prompted to enter the number of rows and columns which will dictate how the price and quantity matrix dimension will be.  
* This matrix format with dimension of rows x columns is considered common for both price and quantity matrices.  
* Similar to the price matrix input method from point 2 Price Matrix (Command-Line Input) .  
* Example Quantity matrix:

      1 3

      2 2

      2 3

      2 2

      2 4

      2 3

      3 1

      2 2

      2 4

      2 3

      3 2

## **How to Run the Script**

The script is run from your terminal and will interactively prompt you for all necessary parameters.

1. Open your terminal (Command Prompt, PowerShell, or Terminal).  
2. Navigate to the directory where you saved the script.  
3. Run the script using the python command:  
   python Revpref.py or python3 Revpref.py

#### **Interactive Prompts**

The script will then guide you through the simplified setup process:

1. Enter source CSV file path for quantities: The path to your input CSV file (e.g., Example\_Quantities.csv).  
2. The path given can be a relative or complete path for the source file and the target file retrieval and storage respectively.  
3. Enter the number of observations (rows) per subject: This is the only dimension you need to provide. For the example above, you would enter **11**.

The script will then automatically detect the number of subjects and goods and prompt you to enter the correctly sized price matrix.

## **Output Format**

The script generates an Excel file (.xlsx) containing a clean summary of the analysis and will give you a CLI summary of the generated data. Each row in the Excel file corresponds to one subject from the source CSV. 

The main outputs that you can obtain from this is the number of GARP, SARP and WARP violations and the CCEI score for each subject.

#### **Example Output:**

For CSV analysis

\============================================================  
      Revealed Preference Analysis Tool (WARP, SARP, GARP, CCEI)  
\============================================================

\--- Main Menu \---  
  1\. Analyze a Single Subject (Manual Input)  
  2\. Analyze Multiple Subjects (from CSV)  
  0\. Exit  
Enter your choice (1, 2, or 0): 2

\--- Multiple Subject Analysis from CSV \---  
Enter source CSV file path for quantities:Book2.csv  
Enter the number of observations (rows) per subject: 11  
File read successfully. Detected 5 subjects and 2 goods.

\--- Enter price matrix P (same for all subjects) \---

\--- Enter prices (P) Data (11 rows x 2 columns) \---  
  Enter prices (P) for row 1 (space-separated 2 values): 15 5  
  Enter prices (P) for row 2 (space-separated 2 values): 10 5  
  Enter prices (P) for row 3 (space-separated 2 values): 15 5  
  Enter prices (P) for row 4 (space-separated 2 values): 5 5  
  Enter prices (P) for row 5 (space-separated 2 values): 10 5  
  Enter prices (P) for row 6 (space-separated 2 values): 5 5  
  Enter prices (P) for row 7 (space-separated 2 values): 5 15  
  Enter prices (P) for row 8 (space-separated 2 values): 5 10  
  Enter prices (P) for row 9 (space-separated 2 values): 5 5  
  Enter prices (P) for row 10 (space-separated 2 values): 5 10  
  Enter prices (P) for row 11 (space-separated 2 values): 5 15  
Enter target Excel file name to save results: Book2\_r.csv

Analyzing data...  
Subject    | WARP    | SARP    | GARP    | CCEI  
\-----------------------------------------------  
1          | 0       | 0       | 0       | 1.0  
2          | 0       | 0       | 0       | 1.0  
3          | 2       | 3       | 1       | 0.9999999999999999  
4          | 0       | 0       | 0       | 1.0  
5          | 2       | 4       | 2       | 0.9999999999999999

Results successfully saved to 'Book2\_r.xlsx'  
Book2\_r.xlsx \[The CCEI is rounded off as 0.9999999999999 is quite close to 1\]   
![][image3]  
For manual input  
\============================================================  
      Revealed Preference Analysis Tool (WARP, SARP, GARP, CCEI)  
\============================================================

\--- Main Menu \---  
  1\. Analyze a Single Subject (Manual Input)  
  2\. Analyze Multiple Subjects (from CSV)  
  0\. Exit  
Enter your choice (1, 2, or 0): 1

\--- Single Subject Analysis \---  
Enter the number of observations (rows): 11  
Enter the number of goods (columns): 2

\--- Enter prices Data (11 rows x 2 columns) \---  
  Enter prices for row 1 (space-separated 2 values): 15 5  
  Enter prices for row 2 (space-separated 2 values): 10 5  
  Enter prices for row 3 (space-separated 2 values): 15 5  
  Enter prices for row 4 (space-separated 2 values): 5 5  
  Enter prices for row 5 (space-separated 2 values): 10 5  
  Enter prices for row 6 (space-separated 2 values): 5 5  
  Enter prices for row 7 (space-separated 2 values): 5 15  
  Enter prices for row 8 (space-separated 2 values): 5 10  
  Enter prices for row 9 (space-separated 2 values): 5 5  
  Enter prices for row 10 (space-separated 2 values): 5 10  
  Enter prices for row 11 (space-separated 2 values): 5 15

\--- Enter quantities Data (11 rows x 2 columns) \---  
  Enter quantities for row 1 (space-separated 2 values): 1 3  
  Enter quantities for row 2 (space-separated 2 values): 2 2  
  Enter quantities for row 3 (space-separated 2 values): 2 3  
  Enter quantities for row 4 (space-separated 2 values): 2 2  
  Enter quantities for row 5 (space-separated 2 values): 2 4  
  Enter quantities for row 6 (space-separated 2 values): 2 3  
  Enter quantities for row 7 (space-separated 2 values): 3 1  
  Enter quantities for row 8 (space-separated 2 values): 2 2  
  Enter quantities for row 9 (space-separated 2 values): 2 4  
  Enter quantities for row 10 (space-separated 2 values): 2 3  
  Enter quantities for row 11 (space-separated 2 values): 3 2

\--- Analysis Results \---  
  \- WARP Violations: 0  
  \- SARP Violations: 0  
  \- GARP Violations: 0  
CCEI Score: 1.0

## **How it works**

### **1\. The `RevealedPreferenceAnalyser` Class**

This class is an object-oriented way to bundle the data (`p` and `q` matrices) with all the functions that operate on that data. When you create an instance of this class, it immediately pre-calculates the fundamental relationships between the choices, making the subsequent tests very efficient.

#### **Class Variables**

* `self.p`: A NumPy array representing the **price matrix** (T rows x N columns).  
* `self.q`: A NumPy array for the **quantity matrix** (T rows x N columns).  
* `self.num_observations`: An integer (`T`) for the number of rows (choices).  
* `self.DRP`: The **Directly Revealed Preferred** matrix. `DRP[i, j]` is `True` if choice `i` is directly revealed preferred to choice `j`.  
* `self.P0`: The **Strictly Directly Revealed Preferred** matrix. `P0[i, j]` is `True` if choice `i` is strictly directly revealed preferred to `j`.  
* `self.RP`: The **Revealed Preferred** matrix. This is the transitive closure of `DRP`, meaning `RP[i, j]` is `True` if there is any chain of preferences leading from `i` to `j`.  
* `self.bundles_are_different`: A boolean matrix where `[i, j]` is `True` if the quantity bundles for choice `i` and choice `j` are not identical.

#### **Methods (Functions within the Class)**

**`__init__(self, p, q)`**

* **Purpose:** The constructor. It runs automatically when you create a new `RevealedPreferenceAnalyser` object.  
* **Working:** It takes the price (`p`) and quantity (`q`) matrices as input, verifies they have the same shape, stores them as class variables, and then immediately calls `_compute_relations()` to do the essential pre-calculations.

**`_warshall(self, relation_matrix)`**

* **Purpose:** A classic graph theory algorithm to find the transitive closure of a relation.  
* **Working:** It takes a matrix (like `DRP`) and figures out all indirect relationships. For example, if A is preferred to B, and B is preferred to C, this algorithm determines that A is preferred to C. It is the engine that turns "directly preferred" (`DRP`) into "indirectly preferred" (`RP`).

**`_compute_relations(self, e=1.0)`**

* **Purpose:** The most important pre-computation step. It calculates the core preference matrices (`DRP`, `P0`, `RP`).  
* **Working:**  
  1. It first calculates the `expenditures` matrix, where `expenditures[i, j]` is the cost of buying bundle `j` at the prices of choice `i` (`pᵢ * qⱼ`).  
  2. `DRP` is calculated by checking where the actual money spent on a bundle (`pᵢ * qᵢ`) was greater than or equal to the cost of other bundles at those same prices.  
  3. `P0` is calculated similarly, but for a strict inequality (`>`).  
  4. It then calls `_warshall()` on the `DRP` matrix to get the `RP` matrix.  
  5. The parameter `e` (efficiency) is used to scale the actual expenditures, which is critical for the `calculate_ccei` method.

**`check_warp(self)`**

* **Purpose:** Counts the number of **Weak Axiom of Revealed Preference (WARP)** violations.  
* **Working:** It identifies a violation if **A is directly preferred to B** AND **B is directly preferred to A**, for two different bundles. In matrix form, this is a vectorized check for where `DRP` and its transpose (`DRP.T`) are both true. It then counts how many observations are involved in such a cycle.

**`check_sarp(self)`**

* **Purpose:** Counts the number of **Strong Axiom of Revealed Preference (SARP)** violations.  
* **Working:** It identifies a violation if **A is revealed preferred to B (possibly indirectly)** AND **B is *directly* revealed preferred to A**, for two different bundles. The matrix implementation checks where `RP` and `DRP.T` are both true.

**`check_garp(self)`**

* **Purpose:** Counts the number of **Generalized Axiom of Revealed Preference (GARP)** violations.  
* **Working:** It identifies a violation if **A is revealed preferred to B (possibly indirectly)** AND **B is *strictly directly* revealed preferred to A**. This is the most general axiom. The matrix check is where `RP` and `P0.T` are both true.

**`calculate_ccei(self)`**

* **Purpose:** Calculates the **Critical Cost Efficiency Index (Afriat Efficiency)**.  
* **Working:**  
  1. It first checks if there are any GARP violations with perfect efficiency (`e=1.0`). If not, it returns `1.0`.  
  2. If there are violations, it performs a **binary search**. It repeatedly asks, "If we pretend the consumer only spent 90% of their budget (e=0.9), are there still violations? What about 95% (e=0.95)?"  
  3. It hones in on the highest possible efficiency level `e` (between 0 and 1\) at which all GARP violations just disappear. This value is the CCEI.

**`run_all_checks(self)`**

* **Purpose:** A convenience method to run all the violation checks at once.  
* **Working:** It calls `check_warp()`, `check_sarp()`, `check_garp()`, and `calculate_ccei()` and returns the results neatly in a dictionary.

### **2\. Helper Functions (Outside the Class)**

These functions handle the "user-facing" parts of the script.

**`align_shapes(p, q)`**

* **Purpose:** To prevent crashes if the user enters a price matrix that is the transpose of the quantity matrix.  
* **Working:** It checks if `p` and `q` have the same shape. If not, it tries transposing `q`, then `p`, then both, to see if it can find a match. If no valid alignment is found, it raises an error.

**`parse_and_detect_dimensions(...)`**

* **Purpose:** To intelligently read the user's CSV file without asking for all the dimensions upfront.  
* **Working:**  
  1. It reads all non-empty rows from the CSV file.  
  2. It uses the `num_observations_per_subject` provided by the user to calculate the total number of subjects (`total_rows / obs_per_subject`).  
  3. It determines the number of goods by counting the columns in the first row.  
  4. It loops through the data, slicing it into blocks for each subject, and stores it in a dictionary.

**`save_results_to_excel(...)`**

* **Purpose:** To write the final analysis results into a clean `.xlsx` file.  
* **Working:** It uses the `openpyxl` library to create a new workbook, write the headers, loop through the results dictionary, and write each subject's data to a new row. It also auto-fits the column widths.

**`get_positive_integer(prompt)`**, **`get_matrix_from_user(...)`**, **`get_filepath(...)`**

* **Purpose:** These are all user-input functions.  
* **Working:** They display a `prompt` to the user and loop until the user provides valid input (e.g., a number that is actually a positive integer, or a file path that actually exists). This makes the script robust and prevents crashes from user typos.

### **3\. Main Program Flow**

This is the code at the end of the script that runs when you execute the file.

**`run_single_subject_ui()` and `run_multi_subject_ui()`**

* **Purpose:** These functions define the step-by-step logic for the program's two main modes.  
* **Working:** They call the various `get_*` helper functions to gather all the necessary information from the user (like file paths and the price matrix). They then create the `RevealedPreferenceAnalyser` object and call its `run_all_checks` method to get the results, which are then printed to the screen and passed to the Excel saver.

**`main_menu()`**

* **Purpose:** The entry point of the script.  
* **Working:** It prints the welcome message and enters an infinite loop that displays the menu options. Based on the user's choice (`1`, `2`, or `0`), it calls the appropriate function (`run_single_subject_ui`, `run_multi_subject_ui`) or breaks the loop to exit the program.

## **License**

This project is licensed under the MIT License.  
MIT License  
Copyright (c) 2025 Sushil walunj  
Permission is hereby granted, free of charge, to any person obtaining a copy  
of this software and associated documentation files (the "Software"), to deal  
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:  
The above copyright notice and this permission notice shall be included in all  
copies or substantial portions of the Software.  
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  
SOFTWARE.

[image1]: <data:image/png;base64,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>

[image2]: <data:image/png;base64,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>

[image3]: <data:image/png;base64,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>
