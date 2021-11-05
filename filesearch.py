import os
from os import listdir
from os.path import isfile, isdir, join
import sys

def listdir_nohidden(path):
    return [f for f in os.listdir(path) if not f.startswith('.')]

def filesearch(filename, dirname):
    #print("Searching",filename,"in",dirname,"...")
    if len(listdir_nohidden(dirname)) != 0:
        for f in listdir_nohidden(dirname):
            if isdir(join(dirname, f)):
                filesearch(filename, join(dirname, f))
            else:
                if isfile(join(dirname, f)):
                    if filename in f:
                        print("\nFOUND:")
                        print(dirname+"\\"+f)
                        print()

def textsearch(text, dirname):
    #print("Searching text",text,"in",dirname,"...")
    if len(listdir_nohidden(dirname)) != 0:
        for f in listdir_nohidden(dirname):
            if isdir(join(dirname, f)):
                textsearch(text, join(dirname, f))
            else:
                if isfile(join(dirname, f)):
                    file1 = open(join(dirname, f), "r")
                    try:                        
                        contents = file1.read()
                        if (text.upper() in contents.upper()):
                            print("\nFOUND:")
                            print(dirname+"\\"+f)
                            print()
                    except:
                        pass
                    file1.close()

def show_help():    
    print("\n--- Simple Recursive File Search -----------------------")
    print("\nSYNTAX 1 - File Search")
    print("  FROM CURRENT DIR:") 
    print("    filesearch -f filename")
    print("  FROM OTHER DIR:") 
    print("    filesearch -f filename directory")
    print("\nSYNTAX 2 - Text Search")
    print("  FROM CURRENT DIR:") 
    print('    filesearch -s "text"')
    print("  FROM OTHER DIR:") 
    print('    filesearch -s "text" directory\n')

def main():
    args = sys.argv[1:]
 
    if len(args) == 2:
        if args[0] == "-f":
            # Find file by name from current directory
            filename = args[1]
            dirname = os.curdir
            filesearch(filename, dirname)
        elif args[0] == "-s":
            text = args[1]
            dirname = os.curdir
            textsearch(text, dirname)
        else:
            show_help()

    elif len(args) == 3:
        if args[0] == "-f":        
            # Find file from specified directory
            filename = args[1]
            dirname = args[2]
            filesearch(filename, dirname)
        elif args[0] == "-s":
            text = args[1]
            dirname = args[2]
            textsearch(text, dirname)
        else:
            show_help()
    else:
        show_help()

if __name__ == "__main__":
    main()