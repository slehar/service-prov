print '===[ running subtest ]==='

x=5
y=4

def change():
    global x,y
    x = 15
    y = 14

def output():
    print 'x = %d'%x
    print 'y = %d'%y
    
change()
output()