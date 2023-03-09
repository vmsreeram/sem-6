from scipy.fft import fft, ifft
import time


# assumed that the given large numbers are in string format
def fastMultLargeNums(a,b):
    nDigits = len(str(a))+len(str(b))
    
    # extracting digits to list
    a_,b_=a,b
    xa,xb=[],[]
    for i in range(nDigits):
        xa.append(a_%10)
        xb.append(b_%10)
        a_//=10
        b_//=10
    
    # computing fft of both the lists
    xa=fft(xa)
    xb=fft(xb)
    
    # performing multiplication
    pdt = xa*xb
    
    # computing inverse fft
    pdt = ifft(pdt)
    ans = 0
    for i,v in enumerate(pdt):
        ans+=round(v.real) * (10**i)
        #    ^ -- we have to round() here so that the accuracy is preserved

    return int (ans)

# naïve O(n^2) method
def school_product(str1, str2):
    if type(str1) != str or (not str1.isnumeric()) or type(str2) != str or (not str2.isnumeric()):
        raise Exception('Expected strings of numbers as args')
    
    len1, len2 = len(str1), len(str2)
    result = [0] * (len1 + len2)
    for i in range(len1):
        digit1 = int(str1[len1 - 1 - i])
        carry = 0
        for j in range(len2):
            digit2 = int(str2[len2 - 1 - j])
            product = digit1 * digit2 + carry
            carry = product // 10
            result[i + j] += product % 10
            if result[i + j] > 9:
                result[i + j] -= 10
                carry += 1
        if carry > 0:
            result[i + len2] += carry
            if result[i + len2] > 9:
                result[i + len2] -= 10
                result[i + len2 + 1] += 1
    result_str = ''.join(str(d) for d in result[::-1])
    return result_str.lstrip('0') or '0'


a=223153122414
b=31231231325523


iter = 100000
start = time.time()
for _ in range(iter):
    __=fastMultLargeNums(a,b)
end = time.time()
print(f'time taken for {iter} iterations of fastft_product = ',end - start, 's.')

start = time.time()
for _ in range(iter):
    __=school_product(str(a),str(b))
end = time.time()
print(f'time taken for {iter} iterations of school_product = ',end - start, 's.')

start = time.time()
for _ in range(iter):
    __=a*b
end = time.time()
print(f'time taken for {iter} iterations of python product = ',end - start, 's.')


print('fastft_product =',fastMultLargeNums(a,b))
print('school_product =',school_product(str(a),str(b)))
print('python product =',a*b)