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
  * Calculates the **Afriat Efficiency Index (CCEI)** to quantify the severity of GARP violations. A score of 1.0 indicates perfect consistency, while a lower score indicates the percentage by which budget constraints must be relaxed to remove all violations.  
* **Intelligent Data Processing**:  
  * **Automatically detects** the number of subjects and goods directly from your CSV file.  
  * Reads and parses stacked CSV files containing data for multiple subjects.  
  * Gracefully handles empty rows or separator lines within the CSV.  
* **Report Generation**:  
  * Creates a final summary report in an Excel (.xlsx) file, with each row corresponding to a single subject's complete results.

## **Installation**

This script requires Python 3.7+ and a few common libraries.

1. **Install Python**: If you don't have it, download Python from [python.org](https://python.org).  
2. **Install Libraries**: Open your terminal or command prompt and install the required packages using pip.  
   pip install numpy openpyxl

## **Input Data Format (Crucial\!)**

The script requires two inputs: a **Quantity Data File** (a CSV file) and a **Price Matrix** (entered in the terminal).

### **1\. Quantity Data (CSV File)**

The script is designed to parse a CSV file where quantity data for multiple subjects is stacked vertically in clean blocks.

* The file should **only contain the numerical quantity data**.  
* The data for each subject must be in a contiguous block.  
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
3. Enter the number of observations (rows) per subject: This is the only dimension you need to provide. For the example above, you would enter **10**.

The script will then automatically detect the number of subjects and goods and prompt you to enter the correctly sized price matrix.

## **Output Format**

The script generates an Excel file (.xlsx) containing a clean summary of the analysis and will give you a CLI summary of the generated data. Each row in the Excel file corresponds to one subject from the source CSV. 

The main outputs that you can obtain from this is the number of GARP, SARP and WARP violations and the CCEI score for each subject.

#### **Example Output:**

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
* **Working:** It identifies a violation if **A is revealed preferred to B (possibly indirectly)** AND **B is *strictly directly* revealed preferred to A**. This is the most general axiom. The matrix check is for where `RP` and `P0.T` are both true.

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

* **Purpose:** These functions define the step-by-step logic for the two main modes of the program.  
* **Working:** They call the various `get_*` helper functions to gather all the necessary information from the user (like file paths and the price matrix). They then create the `RevealedPreferenceAnalyser` object and call its `run_all_checks` method to get the results, which are then printed to the screen and passed to the Excel saver.

**`main_menu()`**

* **Purpose:** The entry point of the script.  
* **Working:** It prints the welcome message and enters an infinite loop that displays the menu options. Based on the user's choice (`1`, `2`, or `0`), it calls the appropriate function (`run_single_subject_ui`, `run_multi_subject_ui`) or breaks the loop to exit the program.

## **License**

This project is licensed under the MIT License.

