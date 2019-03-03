import fileinput
import psycopg2
import ast
import os

try:
    db_endpoint = os.environ['papricacare_db_host']
    print(f'raw_analyzer is running at "{db_endpoint}".')
except KeyError:
    print('raw_analyzer is running locally.')
    db_endpoint = '127.0.0.1'

def filter_str(str, f_list ):
    temp_str = ''
    for c in str:
        if c not in f_list:
            temp_str = temp_str + c
    return temp_str

def list2parstr(cols, nested):
    r_cols = ''
    cnt = 0
    for col in cols:    
        cnt =  cnt + 1

        if '[' in col:
            print(f'=======> {col}')
            t_list = ast.literal_eval(col)
            temp =''
            for c in t_list:
                temp = temp + c
            col = temp
            
        col = col.replace("'","''") 
        
        if nested == None:
            if r_cols != '':
                r_cols = r_cols + ', ' + col
            else:
                r_cols = col
        else:
            if r_cols != '':
                r_cols = r_cols + ', ' + nested + col + nested
            else:
                r_cols = nested + col + nested           
        print(f'----> {cnt}:{col}')
        
    r_cols = '(' + r_cols + ')'
    return r_cols
    
def read_tsv(tsv_file, table_name, postgre_conn):
    fi = fileinput.input(tsv_file)
    cols = fi.readline()
    cols = cols.split('\t')
    cur = postgre_conn.cursor()
    cols = list2parstr(cols, None)
    line = fi.readline()
    
    while line:
        attrs = line.split('\t') # list of strings
        attrs = list2parstr(attrs, "'")
        ins_sql = 'INSERT INTO {} {} VALUES {}'.format(table_name, cols, attrs )
        
        cur.execute(ins_sql);
        postgre_conn.commit()
        line = fi.readline()
        
    postgre_conn.close()

conn = psycopg2.connect(database="papricacaredb", user = "onions", 
        password = "onions2018", host = db_endpoint, port = "5432")

if conn:
    read_tsv('DESC_ID.tsv', 'drug_ingredesc', conn)
    print('completed!')
else:
    print('error in connecting to the postgre db!')
