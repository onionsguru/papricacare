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
        ''' 내부 리스트 처리
        if '[' in col:
            #print(f'=======> {col}')
            t_list = ast.literal_eval(col)
            temp =''
            for c in t_list:
                temp = temp + c
            col = temp
        '''
            
        col = col.replace("'","''") # 내부 ' 처

        if nested == None or col == 'NULL':
            if r_cols != '':
                r_cols = r_cols + ', ' + col
            else:
                r_cols = col
        else:
            if r_cols != '':
                r_cols = r_cols + ', ' + nested + col + nested
            else:
                r_cols = nested + col + nested           
        #print(f'----> {cnt}:{col}')
        
    r_cols = '(' + r_cols + ')'
    return r_cols
    
def read_tsv(tsv_file, table_name, postgre_conn):
    fi = fileinput.input(tsv_file)
    cols = fi.readline()
    cols = cols.replace('\n', '')
    cols = cols.split('\t')
    cur = postgre_conn.cursor()
    cols = list2parstr(cols, None)
    line = fi.readline()
    row_cnt, err_cnt = 0, 0
    while line:
        line = line.replace('\n', '')
        attrs = line.split('\t') # list of strings
        attrs = list2parstr(attrs, "'")
        ins_sql = 'INSERT INTO {} {} VALUES {}'.format(table_name, cols, attrs )
        print(f'"{ins_sql}"')
        try:
            cur.execute(ins_sql);
            postgre_conn.commit()
            row_cnt += 1
        except psycopg2.IntegrityError:
            err_cnt += 1
            print(f'# {err_cnt}-db insert (fk) error: "{ins_sql}"')
        except psycopg2.InternalError:
            err_cnt += 1
            print(f'# {err_cnt}-db insert (pk) error: "{ins_sql}"')
            
        line = fi.readline()

    print(f'# completed with rows: {row_cnt} and errors: {err_cnt} for table {table_name}!')

conn = psycopg2.connect(database="papricacaredbmin", user = "onions", 
        password = "onions2018", host = db_endpoint, port = "5432")

if conn:
    read_tsv('DESC_H.tsv', 'drug_ingredesc', conn)
    read_tsv('REG.tsv', 'drug_registration', conn)
    read_tsv('ING_FORM.tsv', 'drug_ingreform', conn)
    read_tsv('ING_CODE.tsv', 'drug_ingredient', conn)
    read_tsv('PROD_NULL.tsv', 'drug_product', conn)
    print('# all are completed!')
    conn.close()
else:
    print('# error in connecting to the postgre db!')
