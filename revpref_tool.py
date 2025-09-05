# -*- coding: utf-8 -*-
"""
Revealed Preference Analysis Tool (WARP, SARP, GARP, and CCEI)

This script performs revealed preference analysis on price/quantity data.
It includes an automatic shape alignment helper so P and Q inputs that are
transposed relative to each other are handled gracefully.

Usage:
- Run the script and follow the menu.
- For multiple-subject CSV input, provide the number of observations per subject.
"""
import csv
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import openpyxl as oe


class RevealedPreferenceAnalyser:
    """
    A class to perform revealed preference analysis on a set of price/quantity data.
    """

    def __init__(self, p: np.ndarray, q: np.ndarray):
        """
        Initializes the analyser with price and quantity data.
        """
        if p.shape != q.shape or p.ndim != 2:
            raise ValueError("Price and quantity matrices must be 2D and have the same shape.")
        self.p = p.astype(float)
        self.q = q.astype(float)
        self.num_observations = p.shape[0]
        # Pre-compute relationships
        self._compute_relations()

    def _warshall(self, relation_matrix: np.ndarray) -> np.ndarray:
        """Computes the transitive closure using Warshall's algorithm."""
        n = relation_matrix.shape[0]
        closure = relation_matrix.copy().astype(bool)
        for k in range(n):
            for i in range(n):
                if not closure[i, k]:
                    continue
                for j in range(n):
                    if closure[k, j]:
                        closure[i, j] = True
        return closure

    def _compute_relations(self, e: float = 1.0):
        """
        Internal method to compute the fundamental revealed preference relations.
        """
        if self.num_observations < 1:
            self.DRP = self.P0 = self.RP = self.bundles_are_different = np.array([])  # type: ignore
            return

        expenditures = self.p @ self.q.T
        actual_expenditures = np.diag(expenditures) * e

        self.DRP = (actual_expenditures[:, np.newaxis] >= expenditures).astype(bool)
        self.P0 = ((actual_expenditures[:, np.newaxis] - expenditures) > 1e-9).astype(bool)
        self.RP = self._warshall(self.DRP)
        self.bundles_are_different = np.any(self.q[:, np.newaxis, :] != self.q[np.newaxis, :, :], axis=2)

    def check_warp(self) -> int:
        """
        Counts WARP violations based on the number of violating observations.
        """
        if self.num_observations < 2:
            return 0
        violation_matrix = self.DRP & self.DRP.T & self.bundles_are_different
        np.fill_diagonal(violation_matrix, False)
        violating_rows = np.any(violation_matrix, axis=1)
        return int(np.sum(violating_rows))

    def check_sarp(self) -> int:
        """Counts the number of SARP violations."""
        if self.num_observations < 2:
            return 0
        violation_matrix = (self.RP & self.DRP.T & self.bundles_are_different).astype(bool)
        np.fill_diagonal(violation_matrix, False)
        return int(np.sum(np.any(violation_matrix, axis=1)))

    def check_garp(self) -> int:
        """Counts the number of GARP violations."""
        if self.num_observations < 1:
            return 0
        violation_matrix = (self.RP & self.P0.T).astype(bool)
        return int(np.sum(np.any(violation_matrix, axis=1)))

    def calculate_ccei(self) -> float:
        """Computes Afriat's Critical Cost Efficiency Index (CCEI)."""
        # If there are no violations at full efficiency, CCEI is exactly 1.0
        if self.check_garp() == 0:
            return 1.0

        lower_bound, upper_bound = 0.0, 1.0
        # Binary search for the highest 'e' that removes GARP violations
        for _ in range(100):
            e = (lower_bound + upper_bound) / 2.0
            if e == lower_bound or e == upper_bound: # Break if precision limit is reached
                break
                
            temp_analyser = RevealedPreferenceAnalyser(self.p, self.q)
            temp_analyser._compute_relations(e=e)
            
            if temp_analyser.check_garp() == 0:
                lower_bound = e
            else:
                upper_bound = e
        
        # The result of the search is the highest 'e' that passed (lower_bound)
        return float(lower_bound)

    def run_all_checks(self) -> Dict:
        """Runs all checks and returns a dictionary of results."""
        return {
            "WARP_Violations": self.check_warp(),
            "SARP_Violations": self.check_sarp(),
            "GARP_Violations": self.check_garp(),
            "CCEI_Score": self.calculate_ccei()
        }


# ---------------------------
# Helper: Shape alignment
# ---------------------------
def align_shapes(p: np.ndarray, q: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Ensure p and q have identical shape by trying sensible transposes.
    """
    p = np.array(p, dtype=float)
    q = np.array(q, dtype=float)
    if p.shape == q.shape: return p, q
    if p.shape == q.T.shape: return p, q.T
    if p.T.shape == q.shape: return p.T, q
    if p.T.shape == q.T.shape: return p.T, q.T
    raise ValueError(f"Incompatible shapes: p{p.shape} vs q{q.shape}. Please transpose one of the matrices.")


# ---------------------------
# Data I/O and UI
# ---------------------------
def parse_and_detect_dimensions(
    filepath: Path,
    num_observations_per_subject: int
) -> Tuple[Dict[int, np.ndarray], int, int, int]:
    """Parses a CSV file, automatically detecting the number of subjects and goods."""
    try:
        with filepath.open('r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            all_rows = [row for row in reader if any((field or "").strip() for field in row)]

        if not all_rows: raise ValueError("CSV file is empty or contains only empty rows.")

        total_data_rows, num_goods = len(all_rows), len(all_rows[0])

        if total_data_rows % num_observations_per_subject != 0:
            raise ValueError(
                f"Total data rows ({total_data_rows}) is not divisible by "
                f"observations per subject ({num_observations_per_subject})."
            )

        num_subjects = total_data_rows // num_observations_per_subject
        print(f"File read successfully. Detected {num_subjects} subjects and {num_goods} goods.")

        subjects_data: Dict[int, np.ndarray] = {}
        for i in range(num_subjects):
            start_idx, end_idx = i * num_observations_per_subject, (i + 1) * num_observations_per_subject
            block = all_rows[start_idx:end_idx]
            try:
                q_matrix = np.array([[float(x) for x in row] for row in block], dtype=float)
            except Exception as exc:
                raise ValueError(f"Invalid numeric data in subject block {i+1}: {exc}")

            if q_matrix.shape != (num_observations_per_subject, num_goods):
                raise ValueError(f"Inconsistent column count for subject {i+1}. Expected {num_goods}.")

            subjects_data[i + 1] = q_matrix

        return subjects_data, num_observations_per_subject, num_goods, num_subjects

    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return {}, 0, 0, 0
    except (ValueError, IndexError) as e:
        print(f"Error processing CSV: {e}")
        return {}, 0, 0, 0


def save_results_to_excel(results: List[Dict], output_path: Path):
    """Saves analysis results to a styled Excel file."""
    if not results: print("No results to save."); return
    wb = oe.Workbook()
    ws = wb.active
    ws.title = "Revealed Preference Results"
    headers = list(results[0].keys())
    ws.append(headers)
    for cell in ws[1]: cell.font = oe.styles.Font(bold=True)
    for res in results: ws.append(list(res.values()))
    for col in ws.columns:
        max_length = 0
        for cell in col:
            try: max_length = max(max_length, len(str(cell.value)))
            except: pass
        ws.column_dimensions[col[0].column_letter].width = (max_length + 2)
    try:
        wb.save(output_path)
        print(f"\nResults successfully saved to '{output_path}'")
    except Exception as e:
        print(f"\nError saving Excel file: {e}")


def get_positive_integer(prompt: str) -> int:
    """Loops until the user enters a positive integer."""
    while True:
        try:
            value = int(input(prompt))
            if value > 0: return value
            print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter an integer.")


def get_matrix_from_user(rows: int, cols: int, name: str) -> np.ndarray:
    """Prompts the user to enter a matrix of given dimensions (rows x cols)."""
    matrix = []
    print(f"\n--- Enter {name} Data ({rows} rows x {cols} columns) ---")
    for i in range(rows):
        while True:
            prompt = f"  Enter {name} for row {i+1} (space-separated {cols} values): "
            try:
                row = [float(x) for x in input(prompt).split()]
                if len(row) == cols: matrix.append(row); break
                print(f"Error: Please enter exactly {cols} values.")
            except ValueError: print("Invalid input. Please enter numbers only.")
    return np.array(matrix, dtype=float)


def get_filepath(prompt: str, extension: str, must_exist: bool) -> Path:
    """Prompts for a filepath, validates it, and returns a Path object."""
    while True:
        path_str = input(prompt)
        if not path_str: print("File path cannot be empty."); continue
        path = Path(path_str).with_suffix(extension)
        if must_exist and not path.exists():
            print(f"Error: File not found at '{path}'.")
        else:
            return path


def run_single_subject_ui():
    """UI flow for analyzing a single subject's data."""
    print("\n--- Single Subject Analysis ---")
    num_obs = get_positive_integer("Enter the number of observations (rows): ")
    num_goods = get_positive_integer("Enter the number of goods (columns): ")
    p = get_matrix_from_user(num_obs, num_goods, "prices")
    q = get_matrix_from_user(num_obs, num_goods, "quantities")

    try:
        p_aligned, q_aligned = align_shapes(p, q)
    except ValueError as e:
        print(f"Shape alignment error: {e}"); return

    analyser = RevealedPreferenceAnalyser(p_aligned, q_aligned)
    results = analyser.run_all_checks()

    print("\n--- Analysis Results ---")
    print(f"  - WARP Violations: {results['WARP_Violations']}")
    print(f"  - SARP Violations: {results['SARP_Violations']}")
    print(f"  - GARP Violations: {results['GARP_Violations']}")
    print(f"CCEI Score: {results['CCEI_Score']}")


def run_multi_subject_ui():
    """UI flow for analyzing multiple subjects with auto-detection."""
    print("\n--- Multiple Subject Analysis from CSV ---")

    csv_path = get_filepath("Enter source CSV file path for quantities: ", ".csv", must_exist=True)
    num_obs_per_subject = get_positive_integer("Enter the number of observations (rows) per subject: ")

    subjects_q_data, num_obs, num_goods, _ = parse_and_detect_dimensions(csv_path, num_obs_per_subject)

    if not subjects_q_data: print("\nAnalysis aborted due to CSV parsing errors."); return

    print("\n--- Enter price matrix P (same for all subjects) ---")
    p_input = get_matrix_from_user(num_obs, num_goods, "prices (P)")

    aligned_subjects: Dict[int, np.ndarray] = {}
    p_aligned_global = p_input.copy()
    for sid, q_matrix in subjects_q_data.items():
        try:
            p_aligned, q_aligned = align_shapes(p_aligned_global, q_matrix)
            p_aligned_global = p_aligned
            aligned_subjects[sid] = q_aligned
        except ValueError as e:
            print(f"Subject {sid}: {e} - skipping this subject."); continue

    if not aligned_subjects: print("\nNo data to analyze. Aborting."); return

    excel_path = get_filepath("Enter target Excel file name to save results: ", ".xlsx", must_exist=False)

    all_results = []
    print("\nAnalyzing data...")
    header = f"{'Subject':<10} | {'WARP':<7} | {'SARP':<7} | {'GARP':<7} | {'CCEI'}"
    print(header)
    print("-" * len(header))

    for subject_id, q_matrix in aligned_subjects.items():
        analyser = RevealedPreferenceAnalyser(p_aligned_global, q_matrix)
        res = analyser.run_all_checks()
        
        print(f"{subject_id:<10} | {res['WARP_Violations']:<7} | {res['SARP_Violations']:<7} | {res['GARP_Violations']:<7} | {res['CCEI_Score']}")

        all_results.append({
            'Subject_ID': subject_id,
            'WARP_Violations': res['WARP_Violations'],
            'SARP_Violations': res['SARP_Violations'],
            'GARP_Violations': res['GARP_Violations'],
            'CCEI_Score': res['CCEI_Score']
        })

    save_results_to_excel(all_results, excel_path)


def main_menu():
    """Displays the main menu and directs user to the chosen analysis."""
    print("=" * 60)
    print("      Revealed Preference Analysis Tool (WARP, SARP, GARP, CCEI)")
    print("=" * 60)

    while True:
        print("\n--- Main Menu ---")
        print("  1. Analyze a Single Subject (Manual Input)")
        print("  2. Analyze Multiple Subjects (from CSV)")
        print("  0. Exit")

        choice = input("Enter your choice (1, 2, or 0): ")

        if choice == '1': run_single_subject_ui()
        elif choice == '2': run_multi_subject_ui()
        elif choice == '0': print("\nExiting program."); break
        else: print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()