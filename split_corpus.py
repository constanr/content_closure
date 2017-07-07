def split(corpus_name):
    with open(corpus_name,"r") as corpus:
        lines = corpus.readlines()
    print(len(lines))
    delimiter = "---END.OF.DOCUMENT---"
    document_started = False
    document_ended = False
    k = 0
    file_text = ""
    for line in lines:
        if document_started:
            if delimiter in line:
                document_ended = True
                document_started = False
                with open("corpus/" + corpus_name + "-" + str(k).zfill(3) + ".txt") as target:
                    target.write(file_text)
                k += 1
            else:
                file_text += line
        else:
            if delimiter in line:
                document_started = True
                file_text += line
                target = open("corpus/"+corpus_name+"-"+str(k).zfill(3)+".txt")
                target.write(line)







for line in lines:
        if hello1Found == True :
            if line[0:5] == "hello":
                hello2Found = True
                hello1Found = False
                break ## When second hello is found looping/saving to file is stopped
                  ##(though using break is not a good practice here it suffice your simple requirement
            else:
                print(line) #write the line to new file
                target.write(line)
        if hello1Found == False:
            if line[0:5] == "hello": ##find first occurrence of hello
                hello1Found = True
                print(line)
                target = open("filename" + str(k) + ".txt")
                target.write(line)      ##if hello is found for the first time write the
                                        ##line/subsequent lines to new file till the occurrence of second hello

split("WestburyLab.Wikipedia.Corpus.txt")