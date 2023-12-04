import random;
import time;


""" Division Algorithm """
def da_(a, b):
    if b == 0:                                            # a = bq +r의 형태로 b=0이면 성립X
        raise Exception("[da_(a,b)]: divisor can't be 0.");
    
    r = a % b;

    b_ = b if b > 0 else -b;
    r = r if 0 <= r and r <= b_ else r + b_;              # r이 0<= r<= abs(b)의 범위에 존재하는지 확인후 r도 fix
    
    q = (a-r)//b;                                         # 역산을 통해 q를 계산
    
    return (q,r);


""" GCD algorithm """
def gcd_(a, b):
    
    if 0 == b:
        return a;
    else:
        return gcd_(b, a % b);
    
    
""" Extended Euclidean Algorithm """
def eea_(a, b):
    
    i = 1;
    a, b = [a, b] if a >= b else [b, a];                 # 일관성 있는 처리를 위해 큰 수를 앞으로 보냄
        
    # 예외, Special Case 처리
    if a == 0 and b == 0:
        raise Exception("[eea_(a,b)]: Since a = b = 0, gcd is none. ");
    elif a == 0:
        return (0, -1, -b);
    elif b == 0:
        return (1, 0, a);
    else:
        pass;
    
    rList = [a, b];
    sList, tList = [0, 1], [1, 0];
    
    while True:
        i += 1;
        q, r = da_(rList[-2], rList[-1]);
        if r == 0:                                      # r = 0이 되면 더 이상은 필요없음
            break;
            
        rList.append(r);
        
        s = sList[-2] - q * sList[-1];                    # 점화식에 의한 s, t값 구하기
        sList.append(s);
        t = tList[-2] - q * tList[-1];
        tList.append(t)
    
    x, y = tList[-1], sList[-1];
    d = rList[-1];                                      # 0이 되기 직전의 r값이 gcd가 됨

    return (x,y,d);                                     # 이 경우 ax+by=d가 나오며 큰 수가 a로 반드시 inv를 구할 때 크기를 fix해서 보낼 것.


""" Decimal to Binary Algorithm """
def dec2bin_(e):
    b = list();
    while True:
        (e, r) = da_(e, 2);
        r = str(r);
        if 0 == e:
            b.append(r);        
            break;
        b.append(r);
    b = ''.join(b[::-1]);
    return b;                                           # binary String 리턴.


""" Square and Multiply technique """
def sqxmul_(g, e, n):
    
    bin_of_e = dec2bin_(e);

    a = 1;    
    l = len(bin_of_e);
    for i in range(l):                         
        i = int(i);
        a = (a * a) % n;
        if int(bin_of_e[i]) & 1:
            a = (a * g) % n;
    
    return a;


""" Inverse a mod n"""
def inverse_(a, n):
    
    (x, y, d) = eea_(a, n) if n >= a else eea_(a % n , n); # eea의 일관적인 계산을 위해 a와 n의 대소관계를 fix해야함.
                                                      # inverse를 구하는 주 대상인 a를 modulus연산을 통해 미리 n보다 작게 줄여놓는다.
                                                      # 이 경우  nx + ay = gcd(a,n)의 형태로 계산되므로 y를 리턴해야함.
    if(d != 1): 
        raise Exception("[inverse_(a, n)]: Since gcd(a,n) = d != 1 and d can't devide 1, there is no inverse.");

    y = y % n;                                          
    
    return y;


""" Chinese Remainder Theorem """
def crt_(a_1, m_1, a_2, m_2, M):
    
   d = gcd_(m_1, m_2);
   if d != 1:
       raise Exception("[crt_(a_1, m_1, a_2, m_2, M)]: Since gcd_(m_1, m_2) = d > 1, There are many solutions by CRT. It is not appropriate for RSA.\n p,q should be a prime");
   
   b_1, b_2 = M // m_1, M // m_2;                             # m_2, m_1
   b_1_inv, b_2_inv = inverse_(b_1, m_1), inverse_(b_2, m_2)  # m_2^(-1), m_1^(-1)
   x = (a_1 * b_1 * b_1_inv + a_2 * b_2 * b_2_inv) % M        # x = a_1*m_2*m_2^(-1) + a_2*m_1*m_1^(-1)  mod M
   return x;


""" modular exponentiation """
def exp_(g, e, p):
    
    d = gcd_(g, p); 
    if d == 1:                               # gcd(g,p) = 1  then by FlT, g^(p-1) = 1 mod p
        r = e % (p - 1);                       # g^((p-1)k) * g^r = g^r = a mod p
        a = sqxmul_(g, r, p);
    else:                                    # By FlT every g, g^p = g mod p 
        q, r = da_(e, p);                    # Using Division Algorithm, g^e = g^(pq+r) = g^(pq)*g^r = g^q * g^r = g^(q+r) mod p                        
        a = sqxmul_(g, q + r, p) 
    
    return a;


""" RSA Key Generation """
def kg_():
    
    p = 375601199303663623918028970851059108690060737622656882374563455828793657622176097876072312856192135832732184463711063068742149077728583657592264634184355528572480870848331527925285086522424780596227266877862629356042916121799732295561664809804146658903901062227723281507212036783947590038192349656017;
    q = 741535735036899290929340755921725340922126992047864186647795356424020718097701406799776074962826931725204974509136221950232938831166940522950197682750552327244568482697981638376366230817652858893476174365335420815424266346442231015266893056250882970513357778294170408345990377051067151512135653719493;
    n = p * q;
    phi_n = (p - 1) * (q - 1);
    
    e = 0;
    while True:                             # 임의의 e 선택
      candidate = random.randint(2, phi_n - 1);
      if gcd_(phi_n, candidate) == 1:
          e = candidate;
          break;
    
    d = inverse_(e, phi_n);
    
    return (e,n,d,p,q);                    # (e, n) 공개값  (d,p,q) hidden값


""" RSA Encryption """
def enc_(e, n, m):                           # (e, n) 공개값 (m) 평문
    c = exp_(m, e, n);
    return c;


""" RSA Decryption """
def dec_(d, n, p, q, c):                       # (d,p,q) hidden값 (n) 공개값 (c) 암호문
    c_p, c_q = c % p, c % q;
    x_p, x_q = exp_(c_p, d, p), exp_(c_q, d, q);
    m = crt_(x_p, p, x_q, q, n);
    return m;


""" RSA Enc/Dec """
def main():
    random.seed(time.time());
    original_msg = random.randrange(1, 1000);
    (e, n, d, p, q) = kg_();
    c = enc_(e, n, original_msg);
    decrypted_msg = dec_(d, n, p, q, c);
    assert(original_msg == decrypted_msg);


""" Execution """
if __name__ == "__main__":
    main()
