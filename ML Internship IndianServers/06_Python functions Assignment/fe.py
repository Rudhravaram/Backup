# Program to display the Fibonacci sequence up to n-th term

nterms = int(input("How many terms? "))

n1, n2 = 0, 1
l=[]
count = 0
if nterms <= 0:
   print("Please enter a positive integer")
elif nterms == 1:
   print("Fibonacci sequence upto",nterms,":")
   print(n1)
else:
   print("Fibonacci sequence:")
   while count < nterms:
       l.append(n1)
       print(n1)
       nth = n1 + n2
       # update values
       n1 = n2
       n2 = nth
       count += 1