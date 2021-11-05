#!/usr/bin/python
# coding=utf-8

import os
import cx_Oracle
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

def write_to_filesystem(conn, dir_out, tablename, col_id, col_blob):
    cur = conn.cursor()
    cur.execute("select "+col_id+", "+col_blob+" from "+tablename+" order by upper("+col_id+")")
    while True:
        row = cur.fetchone()
        if row is None:
            break
        filename_out = dir_out+"/"+row[0]
        blob = row[1]
        print("Exporting to ", filename_out)
        offset = 1
        num_bytes_in_chunk = 65536
        with open(filename_out, "wb") as f:
            while True:
                data = blob.read(offset, num_bytes_in_chunk)
                if data:
                    f.write(data)
                if len(data) < num_bytes_in_chunk:
                    break
                offset += len(data)
        print("HASH",hash_file(filename_out))
    cur.close()



######################### FOR TEST PURPOSES: CREATE THIS TABLE ON HR SCHEMA ##########################
# CREATE TABLE HR.DOCUMENTS (
#   FILENAME VARCHAR2(1000) NOT NULL PRIMARY KEY,
#   DATA BLOB
# );
######################################################################################################

# Output directory
dir_out = "."

# Connection to oracle sample schema (HR)
conn = connect_db('HR', 'HR', 'XE')
cur = conn.cursor()

# Exporting binary data to filesystem
write_to_filesystem(conn, dir_out, "HR.DOCUMENTS", "FILENAME", "DATA")

# Close and finish
cur.close() # Close the cursor
conn.close() # Close the database connection
