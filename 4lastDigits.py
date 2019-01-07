# I am aware that this could be solved in one line with pow(n,n,10000), but I guess this is not what you expect.

import numpy as np

def lastDigits(n):
    # Let's break n into sums of powers of 2.
    # To do that, we need to find the highest power p of two such as 2^p > n/2
    max_p = 0
    p = 0
    max_p_found = False
    while not max_p_found:
        if 2**p > n//2 :
            max_p_found = True
            max_p = p
        else:
            p+=1
    
    # Now, we need to know precisely which powers of 2 are going to be in this sum.
    power_array = np.array(max_p)       
    k = 1
    temp = n - 2**max_p
    while max_p - k != 0:
        if temp - 2**(max_p - k) >= 0:
            power_array = np.append(power_array, max_p - k)
            temp = temp - 2**(max_p - k)    
        k +=1

    
    if n%2 != 0 : # Checking if n is odd and add 2^0 if so.
        power_array = np.append(power_array,0)
    
    # To illustrate this result with n=52, this gives us 52 = 2^5 + 2^4 + 2^2
        
    # %%
    # At this point, we can write n^n as a product of n^(2^k), for k in power_array.
    # With n=52, this gives 52^52 = 52^(2^5) * 52^(2^4) * 52^(2^2)
    """
    We will use the fact that n^(2^k) = (n^2)^k
    The trick is to perform the computations only on the last 4 digits of any intermediate result.
    For example:
        - n=468532 (arbitrary choice) , we will keep the number 8532 for the computations.
        - Then, we compute 8532^2 and keep the last 4 digits of the results : 5024
        - Then, we compute 5024^2, etc..., and we do this k times for each k in power_array
        - We save the result of each k in an array called product_array
        With n=468532, power_array = [18, 17, 16, 13, 10,  9,  5,  4,  2] 
                       product_array = [2576,   976,   176,  6976,  6576,  2976,  8976,  4176,  576]
    Handling squares of 4 digits number is way less computationnally expensive than directly computing n^n for large n
    """
    product_array = np.array([])
    for k in power_array:
        last4digits = n%10000 #Modulo 10000 keeps the last 4 digits.
        for i in range(k):
            last4digits = pow(last4digits,2,10000)
        product_array = np.append(product_array,last4digits)
    
    """
    Now, we simply compute the product of all then numbers in product_array.
    To remain optimized and to save ourselves from long number errors,
    we will manually calculate each product one by one and still keep the last 4 digits after each product.
    With n=468532 :
        - 2576 * 976 = 2514176, we keep 4176
        - 4176 * 176 = 734976, we keep 4976
        ...
        At the end of this loop, we obtain the last 4 digits of n^n.
        
    """
    # Let's manually compute the product while only keeping the last 4 digits of the intermediate results
    inter_prod = 1 # stands for "intermediate product"
    for i in range(len(product_array)):
        inter_prod = (inter_prod*product_array[i])%10000
    
    result = inter_prod
    
    return result
# %%
# For the sake of presentation, let's display the zeros if the result is something like 0XXX, 00XX, etc.
def add_zeros(result):
    displayed_result = str(int(result))
    missing_zeros = 4 - len(displayed_result)

    for i in range(missing_zeros):
        displayed_result = '0' + displayed_result    
    
    return(displayed_result)
        
# Let's test this algorithm on 10 large random examples:
import random
for i in range(10):
    random_length = random.randint(50,60) #We randomly pick a length for n
    random_n = random.randint(10**random_length,10**(random_length+1))
    algo_result = lastDigits(random_n)
    print("n =",random_n)
    print("This algorithm :",add_zeros(algo_result))
    pow_result = pow(random_n,random_n,10000)

    print("The built-in function 'pow' :", add_zeros(pow_result))
    print('')
