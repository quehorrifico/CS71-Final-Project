import pandas as pd
import glob

def main():

    # Search for a .xlsx file in repository
    i = 0
    for file in glob.glob('*.xlsx'):
        i += 1
        print("Found file:",file)
    if i != 1:
        print("Please make sure that there is only one .xlsx file in the repository.")
        quit()
    df = pd.read_excel(file)

    # Removes extra columns and repeated courses
    labels = ["DEPT","SUBJ","CRSE"]
    for col in df.columns:
        if col not in labels:
            del df[col]
    if len(df.columns) != 3:
        print("Please adjust columns to match \'DEPT\', \'SUBJ\', and \'CRSE\'.")
        quit()
    df.drop_duplicates(subset=['SUBJ','CRSE'],inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Writes to courses.txt
    label = ""
    f = open("courses.txt", "w")
    f.write(str(len(df.DEPT.unique())))
    for i in range(df.shape[0]):
        if df["DEPT"][i] != label:
            label = str(df["DEPT"][i])
            f.write("\n"+label+"\n")
        f.write(str(df["SUBJ"][i]) + str(df["CRSE"][i]) + ",")
    f.close()


main()
