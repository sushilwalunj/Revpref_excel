# **Revealed Preference Analysis Toolkit** 

A robust Python toolkit for non-parametric analysis of consumer choice data, specifically designed for datasets from economics experiments. This script automates reading complex data files, applying revealed preference tests (GARP, SARP, WARP), calculating the Afriat Efficiency Index, validating HARP and generating a clean summary report.

## **The Problem This Solves**

Economics choice experiments often produce large, stacked CSV files where choice data from numerous subjects—each making a series of decisions—is appended one after another. Manually separating and analysing the data for each individual is tedious and error-prone.

This toolkit streamlines that entire workflow. It intelligently parses the source file, automatically detects the number of subjects and goods, runs all necessary calculations, and compiles a final, publication-ready report.

## **Key Features**

* **Comprehensive Revealed Preference Tests**:  
  * Counts violations of the **Generalised Axiom of Revealed Preference (GARP)**.  
  * Counts violations of the **Strong Axiom of Revealed Preference (SARP)**.  
  * Counts violations of the **Weak Axiom of Revealed Preference (WARP)**.  
  * Calculate **Afriat’s critical cost efficiency index.**  
  * Validates the **Houthakker's Axiom of Revealed Preference (HARP)**.  
* **Efficiency Measurement**:  
  * The Afriat Efficiency Index (CCEI) is used to measure the severity of GARP violations, where a value of 1.0 reflects perfect consistency with rational choice and no GARP violations. Lower values indicate the extent to which budget constraints would need to be relaxed to eliminate all GARP violations. For instance, a CCEI score of 0.90 means that the observed choices are 90% consistent with GARP, and a 10% relaxation of the budget would be sufficient to remove all violations.  
* **Intelligent Data Processing**:  
  * **Automatically detects** the number of subjects and goods directly from your CSV file.  
  * Reads and parses stacked CSV files containing data for multiple subjects.  
  * Gracefully handles empty rows or separator lines within the CSV.  
* **Report Generation**:  
  * Creates a final summary report in an Excel (.xlsx) file, with each row corresponding to a single subject's complete results.

## **Installation**
All Executable files are located in the executables folder. Please select appropriate folder for your system. For example, if you have a Windows system, use the executable file from the Executables/Windows folder.
#### **For Windows:**

Use the revpreftool.exe file for windows.  
Once you extract the files, simply double click on the revpreftool.exe file.

If you wish to run the script using python, refer to the steps below.  
\[**Note:** This script requires Python 3.12+ and a few common libraries.\]

1. **Install Python**: If you don't have it, download Python from [python.org](https://python.org).  
2. **Install Libraries**: Open your terminal or command prompt and install the required packages using pip.  
   pip install numpy openpyxl

#### **For Linux:**

Go to the location where you have downloaded the file.  
Once there, open the file location in the terminal and run the following command.  
chmod \+x revpreftool  
./revpreftool

#### **For Macintosh (only for apple silicon):**
Locate the downloaded file and run it.

## **Input Data Format (Crucial\!)**

The script requires two inputs: a **Quantity Data File** (a CSV file) and a **Price Matrix** (entered in the terminal).

### **1\. Quantity Data (CSV File)**

The script is designed to parse a CSV file where quantity data for multiple subjects is stacked vertically in clean blocks.

* The file should **only contain the numerical quantity data**.  
* Each subject's data must be in a contiguous block.  
* The number of rows in each block must be the same for all subjects.  
* Empty rows or rows with just commas (separators) between subject blocks will be automatically ignored.  
* When pasting the location of csv file, make sure that the location is not enclosed within double or single inverted comma’s.

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

![alt text](https://github.com/sushilwalunj/Revpref_excel/blob/main/assets/quantity_img_exc.jpg "Excel") 

The above example is created using Microsoft Excel. From this image it can be inferred that there are 3 participants with 11 observations for 2 goods, hence a 11 x 2 matrix for 3 participants. Now each participant is separated by a blank unmerged row. Once the excel file is ready you can go to File \-\> Save As \-\> select your location of storage \-\> Give the save type as ‘CSV (Comma delimited)’.    
If using Microsoft Excel you need not worry about reconverting your file to xlsx format for modifying the file, you can simply open the file and make changes.  
However, if viewing outside of a spreadsheet application, the csv file will look like the following image.  
![alt text](https://github.com/sushilwalunj/Revpref_excel/blob/main/assets/quantity_img_csv.jpg "CSV") 

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

#### **Running the executable**

* ##### **For Windows**

  * Double click on the revpreftool.exe.

* ##### **For Linux**

  * Go to the location where you have downloaded the file.  
  * Once there, open the file location in the terminal and run the following command.  
    chmod \+x revpreftool  
    ./revpreftool  
* **For Macintosh (only apple silicon)**

The script  runs from your terminal and will interactively prompt you for all necessary parameters.

1. Open your terminal (Command Prompt, PowerShell, or Terminal).  
2. Navigate to the directory where you saved the script.  
3. Run the script using the python command:  
   python revpreftool.py or python3 revpreftool.py

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

* ##### **For CSV analysis**

![alt text](https://github.com/sushilwalunj/Revpref_excel/blob/main/assets/multi_op.jpg "CSV analysis OP") 
![alt text](https://github.com/sushilwalunj/Revpref_excel/blob/main/assets/multi_op_xl.jpg "CSV analysis OP excel") 

* ##### **For manual input**

![alt text](https://github.com/sushilwalunj/Revpref_excel/blob/main/assets/single_op.jpg "Single input analysis OP excel") 

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

