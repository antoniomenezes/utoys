#!/usr/bin/python
# coding=utf-8

import os
import cx_Oracle
from os import listdir
from os.path import isfile, join
import hashlib

cx_Oracle.init_oracle_client()

def connect_db(p_username, p_password, p_tns):
    # Create the connection
    conn = cx_Oracle.connect(user=p_username, password=p_password, dsn=p_tns)
    print("Database version:", conn.version)
    print("Oracle Python version:", cx_Oracle.version,"\n")
    return conn

def hash_file(filename):
    # Adjust BUF_SIZE according to your needs
    BUF_SIZE = 65536  # 64KB chunks

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()

    with open(filename, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
            sha1.update(data)

    hash_values = "MD5: {0}".format(md5.hexdigest())+"\n"+"SHA1: {0}".format(sha1.hexdigest())
    return hash_values

# Read the binary file
def write_to_db(conn, dir_in, tablename, col_id, col_blob):
    cur = conn.cursor()
    filenames = [f for f in listdir(dir_in) if isfile(join(dir_in, f))]
    for filename_in in filenames:
        print("Importing", dir_in+"/"+filename_in)
        print("HASH",hash_file(dir_in+"/"+filename_in))
        # If binary object greater than 1 GB
        nome_arq = os.path.basename(dir_in+"/"+filename_in)
        lob_var = cur.var(cx_Oracle.DB_TYPE_BLOB)
        cur.execute("insert into "+tablename+" ("+col_id+", "+col_blob+") values (:1, empty_blob()) returning "+col_blob+" into :2", [nome_arq, lob_var])
        blob, = lob_var.getvalue()
        offset = 1
        num_bytes_in_chunk = 65536
        with open(dir_in+"/"+filename_in, "rb") as f:
            while True:
                data = f.read(num_bytes_in_chunk)
                if data:
                    blob.write(data, offset)
                if len(data) < num_bytes_in_chunk:
                    break
                offset += len(data)

        conn.commit()
    cur.close()


######################### FOR TEST PURPOSES: CREATE THIS TABLE ON HR SCHEMA ##########################
# CREATE TABLE HR.DOCUMENTS (
#   FILENAME VARCHAR2(1000) NOT NULL PRIMARY KEY,
#   DATA BLOB
# );
######################################################################################################

# Input directory
directory_in = "."

# Connection to oracle sample schema (HR)
conn = connect_db('HR', 'HR', 'XE')
cur = conn.cursor()

# Importing binary data to oracle database
write_to_db(conn, directory_in, "HR.DOCUMENTS", "FILENAME", "DATA")

# Close and finish
cur.close() # Close the cursor
conn.close() # Close the database connection
