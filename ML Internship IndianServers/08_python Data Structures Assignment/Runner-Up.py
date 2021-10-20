# rows = 5
#
# # b = 0
# # # print(range(5,b))
# # # for i in range(5,b,-1):
# # #     print(i)
# #
# # #range(starting,value)
# #
# # for i in range(1,rows+1):
# #     for j in range(1,i+1):
# #         print('*',end='')
# #     print('\r')
# #
# # for i in range(rows,0,-1):
# #     for j in range(1,i+1):
# #         print('*',end='')
# #     print('\r')
# #
# # print('----------------------------')
# for i in range(rows,0,-1):
#     # print(i)
#     for k in range(0,rows-i):
#         print(' ',end='')
#     for j in range(1,i+1):
#         print('*',end='')
#     print('\r')
# for i in range(1,rows+1):
#     for k in range(1,rows+1-i):
#         print(" ",end="")
#     for j in range(1,i+1):
#         print("*",end="")
#     print('\r')

# rows=int(input())
# rows=(rows*2)-1
# for i in range(rows,0,-1):
#     # print(i)
#     for k in range(0,rows-i):
#         print(' ',end='')
#     for j in range(1,i+1):
#         print('*',end='')
#     print('\r')
# for i in range(2,rows+1):
#     for k in range(1,rows+1-i):
#         print(" ",end="")
#     for j in range(1,i+1):
#         print("*",end="")
#     print('\r')
#
# n,m=map(int,input().split())#5
# for i in range(n):#5
#     for j in range(i)

N, M = map(int,input().split())
for i in range(1,N,2):
    print(i)