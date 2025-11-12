import sys

# Defining main function
def main():
    if len(sys.argv) != 2:
        print("Invalid syntax, the program needs a command")
        return
    if sys.argv[1] == "highlights":
        print("Getting highights")
        # getHighligths()
    elif sys.argv[1] == "detailed":
        print("Getting detailed")
        # getDetailed()
    else:
        print("The commands are 'highligts' or 'detailed'")

# Using the special variable
# __name__
if __name__=="__main__":
    main()
