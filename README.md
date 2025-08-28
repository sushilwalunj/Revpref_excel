
# **Revealed Preference Analysis Toolkit for Experimental Data**

## **Overview**

This repository contains a Python script designed to perform non-parametric analysis of consumer choice data, specifically tailored for datasets from behavioral economics experiments. The toolkit automates the process of reading complex experimental data files, applying established revealed preference tests, and generating a clean, summarized report.

The primary goal of this software is to test whether the observed choices of participants are consistent with the theory of utility maximization. It calculates the number of violations of key economic axioms and measures the degree of any inconsistency using the Afriat Efficiency Index.

The script is particularly useful for a common experimental data structure where the choice data for multiple subjects, potentially from multiple experimental conditions, is stacked vertically in a single CSV file.

## **Features**

* **Revealed Preference Tests**:  
  * Counts violations of the **Generalized Axiom of Revealed Preference (GARP)**.  
  * Counts violations of the **Strong Axiom of Revealed Preference (SARP)**.  
  * Counts violations of the **Weak Axiom of Revealed Preference (WARP)**.  
* **Efficiency Measurement**:  
  * Calculates the **Afriat Efficiency Index (CCEI)**, also known as emax, to quantify the severity of GARP violations. A score of 1.0 indicates perfect consistency.  
* **Automated Data Processing**:  
  * Reads and parses complex CSV files containing data for multiple subjects and multiple quantity sets per subject.  
  * Iterates through each subject, performs the analysis, and aggregates the results.  
* **Report Generation**:  
  * Creates a final summary report in an **Excel (.xlsx) file**, with each row corresponding to a single subject's results.

## **The Problem This Solves**

In many economic experiments, data is collected from numerous subjects who each make a series of choices under different conditions (e.g., different prices). This often results in a large data file where each subject's block of choices is appended one after another.

Manually separating the data for each subject—especially when there are multiple sets of choices per subject—is tedious and prone to error. This toolkit automates that entire workflow. It intelligently navigates the source CSV based on user-provided parameters, extracts the data for each individual, runs all the necessary calculations, and compiles a final report.

## **Installation & Dependencies**

This script is written in Python and relies on a few common libraries.

1. **Prerequisites**:  
   * Python 3.7 or newer.  
2. **Required Libraries**:  
   * numpy: For numerical operations and matrix manipulation.  
   * openpyxl: For writing data to Excel files.  
3. Installation:  
   You can install the required libraries using pip:  
   pip install numpy openpyxl

## **Input Data Format (Crucial\!)**

The script requires two sets of inputs: a **price matrix** provided via the command line, and a **quantity data file** in a specific CSV format.

### **1\. Price Matrix (Command-Line Input)**

* You will be prompted to enter the prices for each choice situation.  
* This price matrix is assumed to be **constant for all subjects and all quantity sets**.  
* It should be a T x N matrix, where T is the number of observations (choices) and N is the number of goods.

### **2\. Quantity Data (CSV File)**

This is the most critical part of the setup. The script is designed to parse a CSV file with a specific, structured format.

* The file can contain header information for each subject, but the script will **skip these rows** based on the dist parameter.  
* The data for all subjects is contained in a single file.  
* For each subject, there can be multiple sets of quantity choices (e.g., choices under different experimental treatments). The number of sets is defined by the nq parameter.  
* Each set of quantity choices consists of two rows: a label row (e.g., "Treatment\_A\_Choices") and a data row containing the actual quantity values.  
* The data block for one subject must be separated from the next by a consistent number of rows.

#### **Conceptual CSV Structure:**

To understand the structure, consider an experiment with many subjects. Each subject provides **nq** sets of quantity choices. The entire block of data for one subject is separated from the next by some separator rows. The script navigates the file using the dist parameter, which is the total number of rows from the start of one subject's data to the start of the next.

generic\_data\_file.csv:

Subject 1 Demographics and other info...,,,,,,  \# Row 1: Subject 1 Header (skipped by the script)  
Label for Quantity Set 1,q1,q2,q3,...          \# Row 2: Subject 1, Quantity Set 1  
Label for Quantity Set 2,q1,q2,q3,...          \# Row 3: Subject 1, Quantity Set 2  
...                                            \# (if nq \> 2\)  
Separator Row (can be blank or contain other data),,, \# Row 4: Separator  
Subject 2 Demographics and other info...,,,,,,  \# Row 5: Subject 2 Header (skipped)  
Label for Quantity Set 1,q1,q2,q3,...          \# Row 6: Subject 2, Quantity Set 1  
Label for Quantity Set 2,q1,q2,q3,...          \# Row 7: Subject 2, Quantity Set 2  
...                                            \# ...and so on

In this structure, dist would be **4** (1 header row \+ 2 quantity set rows \+ 1 separator row). The script uses this number to jump from the start of Subject 1's block (Row 1\) to the start of Subject 2's block (Row 5).

## **How to Run the Script**

You execute the script from your terminal. It will interactively prompt you for all the necessary parameters.

1. Open your terminal or command prompt.  
2. Navigate to the directory where the script is saved.  
3. Run the script using the python command:  
   python your\_script\_name.py

4. The script will then ask you for the following information, one by one:  
   * **Enter number of observations**: The number of choices each subject made (T).  
   * **Enter prices for observation...**: You will enter the prices for each good for each observation, separated by spaces.  
   * **Enter the number of quantity matrices per subject**: The number of choice sets per subject (nq).  
   * **Enter the number of subjects \+1**: If you have 148 subjects, you enter 149\.  
   * **Enter the distance between subjects...**: The crucial dist parameter described above.  
   * **Enter the source file path**: The name of your input CSV file (e.g., source\_data.csv).  
   * **Enter the target file path**: The desired name for your output Excel file (e.g., results.xlsx).

#### **Example Terminal Session:**

$ python your\_script\_name.py  
Enter number of observations: 11  
Enter prices for observation 1 (space-separated): 10 15  
... (enter prices for all 11 observations) ...  
Enter the number of quantity matrices per subject (default is 1): 2  
Enter the number of subjects \+1: 149  
Enter the distance between subjects in the csv file: 4  
Enter the source file path (.csv extension only, default src: CWD): my\_experiment\_data.csv  
Enter the target file path (.xlsx extension only, default save: CWD): analysis\_output.xlsx

After you provide the last input, the script will process the data and generate the Excel file.

## **Output Format**

The script will create an Excel file (.xlsx) with the name you specified. The file will contain a single sheet with the following columns:

| NGV | CCEI |
| :---- | :---- |
| 0 | 1.0 |
| 2 | 0.9542 |
| 0 | 1.0 |
| ... | ... |

* **NGV**: The total number of **GARP Violations** for that subject. A value of 0 means the subject's choices were perfectly consistent.  
* **CCEI**: The **Critical Cost Index** (Afriat Efficiency) for that subject. A value of 1.0 indicates perfect consistency. Values less than 1.0 indicate the degree of inconsistency.

Each row in the Excel file corresponds to one subject from the source CSV, in the order they appeared.

## Acknowledgements

Credit to **@Girono-Joestar** for their help in developing the algorithms and for their insightful feedback throughout this project. This assistance is greatly appreciated.

## **License**

This project is licensed under the MIT License. See the LICENSE file for details.

