--http://www.progsoc.uts.edu.au/wiki/Euler_Solution_243

{- Generate prime numbers in the usual way. -}
primes :: [Integer]
primes = 2:3:primes'
  where
    1:p:candidates  = [6*k+r | k <- [0..], r <- [1,5]]
    primes'         = p : filter isPrime candidates
    isPrime n       = all (not . divides n) $ takeWhile (\p -> p*p <= n) primes'
    divides n p     = n `mod` p == 0

{- Determine the Euler Phi of a number "n" (the number of numbers less than "n"
 - with greatest common divisor with "n" of 1).
 - Note: eulerPhi(a * b) == eulerPhi(a) * eulerPhi(b), although not used here, this
 - will be used later! -}
eulerPhi :: Integer -> Integer
eulerPhi n = sum $ snd $ unzip $ zip (filter (== 1) [gcd k n | k <- [1..n]]) $ repeat 1

{- Generate the list of primorials and their euler phi values. -}
primorialPhis :: [(Integer,Integer)]
primorialPhis = map (\x -> (product (take x primes),product (map eulerPhi (take x primes)))) [1..]

{- Convert a numerator and denominator into a double value. -}
conv :: Integer -> Integer -> Double
conv n  d = (fromIntegral n) / (fromIntegral d)

{- Find a number with a resilience ratio less than the one given.
 - ALGORITHM:
 - Note that the lowest values for resilience are the primorials*k for k in [1..] up
 - to the next primorial.
 - 1. Use the list of primorials and their phi values and a multiplier of 1.
 - 2. If the current head of the list (cpri) * m == the next primorial (npri)
 -    then drop the first element of the list, reset m and continue.
 - 3. If the current primorial * the multiplier has a lower resilience than
 -    the target value then return it, otherwise continue.
 - 4. Increment the multiplier and go to step 2. -}
findRlt :: Double -> Integer
findRlt val = inner primorialPhis 1
  where
    inner :: [(Integer,Integer)] -> Integer -> Integer
    inner ((cpri,cphi):(npri,nphi):pps) m | cpri * m == npri = inner ((npri,nphi):pps) 1
    inner ((cpri,cphi):pps) m | conv (cphi * m) ((cpri * m) - 1) < val = cpri * m
    inner pps m = inner pps (m + 1)

{- Find the first denominator with resilience less than 15499/94744. -}
main = print (findRlt (15499 / 94744))
