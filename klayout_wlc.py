import linecache
import os.path

def confirm():

    a=raw_input("Do you have the required Data.txt file? [y/n]")
    if(a == "y"):
        run()
    elif(a == "n"):
        raw_input("save the file and press enter to continue")
        print ""
        confirm()
    elif(a == "Exit" or a == "exit"):
        None
    else:
        print "invalid option, please try again"
        print ""
        confirm()

def run():
    

    ln = 0
    store = []
    Area = 0
    nofile = 0

    start = 0
    while True:
         #   print ln
            if(os.path.isfile("Data.txt")==False):
                print "Data file is not found"
                nofile = 1
                break     
            a = linecache.getline('Data.txt', ln)
            a = str(a)
            
         #   print a

            if(start == 1):
                    if(str(a[0]+a[1]+a[2]+a[3]+a[4])!="ENDEL"):
                            a = a.replace("X","")
                            a = a.replace("Y","")
                            a = a.replace(" ","")
                            a = a.replace("\n","")
                            b = a.split(":")
                            c = (int(b[0]),int(b[1]))
                            store.append(c)
                    else:
                            break
            if(len(a)>2):
                if(str(a[0]+a[1]+a[2]+a[3]+a[4])=="XY 0:"):
                    None
                elif(str(a[0]+a[1])=="XY" and (int(str(a[3]+a[4]+a[5]))>0)):
                    start = 1
                    print a
            ln = ln+1
              
    #'50.45000\t137.20000\n55.45000\t137.20000\n55.45000\t122.70000\n45.45000\t122.70000\n45.45000\t112.70000\n60.95000\t112.70000\n60.95000\t147.70000\n60.95000\t147.70000\n60.95000\t147.70000'


    def parea(corners):
        n = len(corners) # of corners
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += corners[i][0] * corners[j][1]
            area -= corners[j][0] * corners[i][1]
        area = abs(area) / 2.0
        return area


    if(nofile == 0):
        
        Area = parea(store)
        print "Area =",Area

        line = 0
        e = ""
        Width = 0
        trials = 0
        while True:
            a = linecache.getline('Data.txt', line)
            a = str(a)
           # print a
            if("w="in a):
                    #print 
                    a = linecache.getline('Data.txt', line)
                    b = linecache.getline('Data.txt', line+1)
                    c = str(a+b)
                    d = c.index("w=")
                    while (c[d]!=" "):
                        e = e+c[d]
                        d=d+1
                    
            if("w=" in e):
                f = e.index("w")
                e = e[f+2:]
                Width = float(e)
                print "Width =",Width
                break    
            line=line+1
        #Width = 0.5
        if(Width !=0):
            Length = Area/Width
            Length = Length/1000000
            print "Length = ",Length
    raw_input("press enter if you want to process another file.")
    print ""
    confirm()

confirm()
