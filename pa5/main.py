import sys
import reader as rd

def main():
    global class_map
    global imp_map
    global parent_map
    global aast
    if len(sys.argv) < 2:
        print("Specify .cl-ast input file.")
        exit()
    class_map, imp_map, parent_map, aast = rd.read_type_file(sys.argv[1])


if __name__ == "__main__":
    main()
