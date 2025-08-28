import numpy as np
import csv
import openpyxl as oe

def warshall(R0):
    """
    Computes the transitive closure of a binary matrix R0 using Warshall's algorithm.
    R0: 2D numpy array (binary: 0/1) where R0[i,j]=1 means observation i is directly revealed preferred to j.
    Returns: Transitive closure matrix R.
    """
    T = R0.shape[0]
    R = R0.copy()
    for k in range(T):
        for i in range(T):
            if i == k:
                continue
            if R[i, k] > 0:
                for j in range(T):
                    if j == k:
                        continue
                    if R[i, j] == 0:
                        R[i, j] = R[k, j]
    return R

def warshall_sum(R0):
    """
    Computes the shortest path cost matrix using a variant of Warshall's algorithm.
    R0: 2D numpy array of costs.
    Returns: Matrix R with the shortest path costs.
    """
    T = R0.shape[0]
    R = R0.copy()
    for k in range(T):
        for i in range(T):
            for j in range(T):
                R[i, j] = min(R[i, k] + R[k, j], R[i, j])
    return R

def nwarpviol(p, q):
    """
    Counts the number of WARP (Weak Axiom of Revealed Preference) violations.
    p, q: 2D numpy arrays of shape (T, N) for prices and quantities.
    """
    T = p.shape[0]
    # Initialize Direct Revealed Preference (DRP) as identity.
    DRP = np.eye(T, dtype=int)
    for i in range(T):
        for j in range(T):
            if i != j:
                # If the expenditure of i's own bundle (at its own prices) is at least that of j's bundle evaluated at i's prices:
                if np.dot(p[i], q[i]) >= np.dot(p[i], q[j]):
                    DRP[i, j] = 1

    nviol = 0
    for t in range(T):
        for v in range(T):
            if t != v:
                # WARP violation if both observations directly reveal each other and their bundles differ.
                if DRP[t, v] == 1 and DRP[v, t] == 1 and not np.array_equal(q[t], q[v]):
                    nviol += 1
                    break  # Count only one violation per observation.
    return nviol

def nsarpviol(p, q):
    """
    Counts the number of SARP (Strong Axiom of Revealed Preference) violations.
    p, q: 2D numpy arrays (T observations × N goods).
    """
    T = p.shape[0]
    # Build the Direct Revealed Preference (DRP) matrix using the '≥' condition.
    DRP = np.eye(T, dtype=int)
    for i in range(T):
        for j in range(T):
            if i != j:
                if np.dot(p[i], q[i]) >= np.dot(p[i], q[j]):
                    DRP[i, j] = 1

    # Compute transitive closure.
    RP = warshall(DRP)
    nviol = 0
    for t in range(T):
        for v in range(T):
            if t != v:
                # SARP violation: t is indirectly revealed preferred to v and v is directly revealed preferred to t, and the bundles differ.
                if RP[t, v] == 1 and DRP[v, t] == 1 and not np.array_equal(q[t], q[v]):
                    nviol += 1
                    break
    return nviol

def ngarpviol(p, q):
    """
    Counts the number of GARP (Generalized Axiom of Revealed Preference) violations.
    p, q: 2D numpy arrays (prices and quantities, shape (T,N)).
    """
    T = p.shape[0]
    # Initialize DRP (using ≥) and P0 (using >) matrices.
    DRP = np.eye(T, dtype=int)
    P0 = np.zeros((T, T), dtype=int)
    for i in range(T):
        for j in range(T):
            if i != j:
                exp_i = np.dot(p[i], q[i])
                exp_ij = np.dot(p[i], q[j])
                if exp_i >= exp_ij:
                    DRP[i, j] = 1
                    if exp_i > exp_ij:
                        P0[i, j] = 1

    # Compute the transitive closure.
    RP = warshall(DRP)
    nviol = 0
    for t in range(T):
        for v in range(T):
            # GARP violation: if t is indirectly revealed preferred to v and v is strictly directly revealed preferred to t.
            if RP[t, v] == 1 and P0[v, t] == 1:
                nviol += 1
                break
    
    return nviol

def garp(p, q):
    """
    Returns 1 if the data satisfy GARP (i.e. no GARP violations), else 0.
    """
    return 1 if ngarpviol(p, q) == 0 else 0

def garpe(p, q, e):
    """
    Checks whether the data satisfy the adjusted GARP condition for a given efficiency parameter e.
    The self-expenditure is scaled by e.
    Returns 1 if the adjusted GARP is satisfied, else 0.
    """
    T = p.shape[0]
    DRP = np.eye(T, dtype=int)
    for i in range(T):
        for j in range(T):
            if i != j:
                if e * np.dot(p[i], q[i]) >= np.dot(p[i], q[j]):
                    DRP[i, j] = 1
    RP = warshall(DRP)
    
    P0 = np.zeros((T, T), dtype=int)
    for i in range(T):
        for j in range(T):
            if i != j:
                if e * np.dot(p[i], q[i]) > np.dot(p[i], q[j]):
                    P0[i, j] = 1
    # Check for any violation in the adjusted data.
    for t in range(T):
        for v in range(T):
            if RP[t, v] == 1 and P0[v, t] == 1:
                return 0
    return 1

def emax(p, q):
    """
    Computes the highest Afriat Efficiency parameter (critical cost index) such that the data satisfy GARP.
    Uses a binary search between 0 and 1.
    """
    if garp(p, q) == 1:
        e = 1.0
    else:
        eupper = 1.0
        elower = 0.0
        tol = 1e-6
        # Binary search loop; avoid division by zero by using max(elower, tol)
        while (eupper - elower) / max(elower, tol) >= tol:
            eevaluate = (eupper + elower) / 2.0
            if garpe(p, q, eevaluate) == 1:
                elower = eevaluate
            else:
                eupper = eevaluate
        e = eevaluate
    
    return e

def file_wk(p,m,dist,tsn,srsc,nq=1):

    def data_entry(m,p,no_q,dist):
        temp_arr_1=[]
        temp_arr_2=[]
        main_dict={}
        o=0
        for i in range(1,m):
                main_dict[i]={
                    'ngarpviol':{},
                    #'nsarpviol':{},
                    #'nwarpviol':{},
                    'ccei':{},
                    'q':{},
                }
            
        for i in range(1,m):
            if o >= 588:  # Prevent IndexError
                break 
            main_dict[i] = {
                'ngv':{},
                #'nsv':{},
                #'nwv':{},
                'ccei':{},
                'q': {},
            }
            o += dist  # Move to the next subject block            
            for int_lop in range(1,no_q): #default case is 1 for the number of quantity matrices, i.e, 1 experiment with 1 quantity matrix of mxn size
                main_dict[i]['q'][int_lop]=[]
        k=0
        for i in range(1,m):
                for l in range(1,no_q):
                    while k < len(rows_1):
                        k+=1
                        for r in rows_1[k]:
                            temp_arr_1.append(r)
                        k+=1
                        for r_1 in rows_1[k]:
                            temp_arr_2.append(r_1)
                        temp_arr_1.pop(0)
                        temp_arr_2.pop(0)
                        for it in temp_arr_1:
                            temp_arr_1[temp_arr_1.index(it)]=int(it)
                        for it_2 in temp_arr_2:
                            temp_arr_2[temp_arr_2.index(it_2)]=int(it_2)
                        k+=1
                        break
                    main_dict[i]['q'][l]=np.column_stack((temp_arr_1, temp_arr_2))
                    temp_arr_1.clear()
                    temp_arr_2.clear()
                k+=1
        main_dict=calc_for_vals(m,p,dict_data=main_dict)
        file_maker(main_dict,m)

    def calc_for_vals(m,p,dict_data):
        p_mat_cnst=p
        for i in range(1,m):
            for j in range(1,no_q):
                dict_data[i]['ngv'][j]=ngarpviol(p_mat_cnst,(dict_data[i]['q'][j]))
                #dict_data[i]['nsv'][j]=nsarpviol(p_mat_cnst,(dict_data[i]['q'][j]))
                #dict_data[i]['nwv'][j]=nwarpviol(p_mat_cnst,(dict_data[i]['q'][j]))
                dict_data[i]['ccei'][j]=emax(p_mat_cnst,(dict_data[i]['q'][j]))
        return dict_data

    def safe_get(value):
        """DONT CALL|Ensure no empty lists go into the Excel file."""
        return None if isinstance(value, list) and not value else value

    def safe_get(value):
        """DONT CALL|Ensure no empty lists go into the Excel file."""
        return None if isinstance(value, list) and not value else value

    def file_maker(dict_file,m):
        """Create an Excel file with one row per subject including all 3 experiment results."""
        wb = oe.Workbook()
        ws = wb.active
        ws.title = "Results"
        headers = ['NGV', 'CCEI']
        ws.append(headers)

        for i in range(1, m):
            print(dict_file[i])
            subj = dict_file.get(i, {})
            row_data = [
                safe_get(subj.get('ngv', {}).get(1)),  
                #safe_get(subj.get('nwv', {}).get(1)), 
                #safe_get(subj.get('nsv', {}).get(1)),  
                safe_get(subj.get('ccei', {}).get(1)), 
            ]
            ws.append(row_data)
        wb.save(tsn)
        print("Excel file ",tsn," created successfully.")

    p=np.array(p)  #price matrix
    m=m  #number of subjects +1
    tsn=tsn  #target save name
    srsc=srsc  #source csv file name
    dist=dist  #distance between subjects in the csv file
    no_q=nq #number of quantity matrices per subject
    file_work=open(srsc,mode='r')
    rows_1=[]
    with open(srsc,'r') as file_work:
        csv_reader=csv.reader(file_work)
        for row in csv_reader:
            rows_1.append(row)
    data_entry(m,p,no_q,dist)

p=[]
n=int(input("Enter number of observations: "))
for i in range(n):
    p_1 = list(map(int, input(f"Enter prices for observation {i+1} (space-separated): ").split()))
    p.append(p_1)
nq=int(input("Enter the number of quantity matrices per subject (default is 1): ") or 1)
m=int(input("Enter the number of subjects +1: "))
dist=int(input("Enter the distance between subjects in the csv file: ") )
wrk_bk_src=input("Enter the source file path (.csv extension only, default src: CWD): ")
wrk_bk_trg=input("Enter the target file path (.xlsx extension only, default save: CWD): ")
dict_val=file_wk(p=p,m=m,dist=dist,tsn=wrk_bk_trg,srsc=wrk_bk_src,nq=nq)