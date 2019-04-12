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
        t_attrs = attrs
        attrs_alt = list(attrs)
        attrs_alt[-1] = 'NULL'
        attrs = list2parstr(attrs, "'")
        attrs_alt = list2parstr(attrs_alt, "'")
        ins_sql = 'INSERT INTO {} {} VALUES {}'.format(table_name, cols, attrs )
        ins_sql_alt = 'INSERT INTO {} {} VALUES {}'.format(table_name, cols, attrs_alt )
        #print(f'{ins_sql}') 
        
        try:
            cur.execute(ins_sql)
            row_cnt += 1
            postgre_conn.commit()
            if row_cnt % 100 == 0:
                print(f'\n# completed with rows: {row_cnt} and errors: {err_cnt} for table {table_name}!')
                 
        except psycopg2.IntegrityError as detail:
            postgre_conn.rollback()
            err_cnt += 1
            #print(f'-----> "{detail.args[0]}"')
            if 'duplicate key' in detail.args[0]: # duplicated pk
                print(f'# {err_cnt}-pk error: "{ins_sql}"')
            elif 'foreign key' in detail.args[0]: # no matched fk
                if t_attrs[-1] != '':
                    print(f'# {err_cnt}-db fk error: "{ins_sql}" and "{t_attrs[-1]}"')
                try:
                    cur.execute(ins_sql_alt)
                    postgre_conn.commit()
                    row_cnt += 1 
                    err_cnt -= 1
                    if t_attrs[-1] != '':
                        print(f'# {err_cnt}-fk warning: "{ins_sql}" -> by setting the foreign key null')
                except psycopg2.IntegrityError as detail:
                    postgre_conn.rollback()
                    if 'forein key' in detail.args[0]: # no present fk
                        print(f'# {err_cnt}-fk error: "{ins_sql_alt}"')
            else:
                print(f'# {err_cnt}-unhandled error: "{ins_sql}"')
        except psycopg2.InternalError as detail:
            postgre_conn.rollback()
            err_cnt += 1
            if 'aborted' in detail.args[0]: # duplicated pk
                print(f'# {err_cnt}-db aborted error: "{ins_sql}"')
            else:
                print(f'# {err_cnt}-unhandled internal error: "{ins_sql}"')

        line = fi.readline()
       
    print(f'\n# completed with rows: {row_cnt} and errors: {err_cnt} for table {table_name}!')

conn = psycopg2.connect(database="papricacare", user = "onions", 
        password = "onions2018", host = db_endpoint, port = "5432")

if conn:
    cur = conn.cursor()
  
    cur.execute('delete from drug_ingredesc')
    cur.execute('delete from drug_registration')
    cur.execute('delete from drug_ingreform')
    cur.execute('delete from drug_ingredient')
    cur.execute('delete from drug_product')
    conn.commit()
    print('# all rows deleted!')

    read_tsv('DESC_ID.tsv', 'drug_ingredesc', conn)
    read_tsv('REG_CODE.tsv', 'drug_registration', conn)
    read_tsv('ING_FORM_ID.tsv', 'drug_ingreform', conn)
    read_tsv('ING_CODE.tsv', 'drug_ingredient', conn)
 
    read_tsv('PROD_CODE.tsv', 'drug_product', conn)
    if conn.close():
        print('# all completed!')
else:
    print('# error in connecting to the postgre db!')
