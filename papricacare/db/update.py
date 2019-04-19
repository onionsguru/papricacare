import fileinput
import psycopg2
import ast
import os

try:
    db_endpoint = os.environ['papricacare_db_host']
    print(f'import is running at "{db_endpoint}".')
except KeyError:
    print('import is running locally.')
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
    
def read_tsv(csv_file, table_name, postgre_conn):
    fi = fileinput.input(csv_file)
    cols = fi.readline()
    
    #cols = cols + '\t' + 'created' + '\t' + 'modified' + '\t' + 'is_rx' + '\t' + 'is_combination'
    
    cols = cols.replace('\n', '').replace("'", '"').split('\t')
    cur = postgre_conn.cursor()
    cols = list2parstr(cols, None)

    line = fi.readline()
    row_cnt, err_cnt = 0, 0
    while line:
        #line = line + '\t' + '2019-04-18' + '\t' + '2019-04-18' + '\t' + 'true' + '\t' + 'true'
        
        attrs = line.replace('\n', '').replace("'", '"').split('\t') # list of strings
        #attrs = list2parstr(attrs, "'")
        ins_sql = 'UPDATE {} SET image_url = \'{}\' WHERE kd_code={}'.format(table_name, attrs[1], attrs[0] )
                
        try:
            cur.execute(ins_sql)

            row_cnt += 1
            if row_cnt % 1000 == 0:
                print(f'{row_cnt} completed!')   
                postgre_conn.commit()    

        except psycopg2.IntegrityError as detail:
            postgre_conn.rollback()
            err_cnt += 1
            #print(f'-----> "{detail.args[0]}"')
            if 'duplicate key' in detail.args[0]: # duplicated pk
                print(f'# {err_cnt}-pk error: "{ins_sql}"')
            elif 'foreign key' in detail.args[0]: # no matched fk
                # print(f'# {err_cnt}-db fk error: "{ins_sql}"')
                try:
                    cur.execute(ins_sql_alt)
                    postgre_conn.commit()
                    row_cnt += 1 
                    err_cnt -= 1
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

        line = fi.readline()

    postgre_conn.commit()    
    print(f'\n# completed with rows: {row_cnt} and errors: {err_cnt} for table {table_name}, with file:{csv_file}!')


#conn = psycopg2.connect(database="papricacare", user = "onions", password = "onions2018", host = db_endpoint, port = "5432")

conn = psycopg2.connect(database="pcare_db", user = "onns", 
        password = "ghdtmddyd", host = 'pcaredb.ce6uph5ztrl3.ap-northeast-2.rds.amazonaws.com', port = "5432")

if conn:
    cur = conn.cursor()

    #read_tsv('h1.tsv', 'hospital_hospital', conn)
    # read_tsv('d.tsv', 'disease_disease', conn)
    
    read_tsv('DRUG_update.tsv', 'drug_drug', conn)
    
    
    if conn.close():
        print('# all completed!')
else:
    print('# error in connecting to the postgre db!')

