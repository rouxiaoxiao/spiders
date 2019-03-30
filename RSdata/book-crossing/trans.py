# -*-coding:utf-8-*-

if __name__ == '__main__':
    file_in = open('BX-Book-Ratings.data')
    file_out = open('ratings.dat','a')
    file_out.truncate()
    for line in file_in:
        line_new = line.replace("\"", "").replace(";","::")
        file_out.write(line_new)
        file_out.flush()
    file_in.close()
    file_out.close()
