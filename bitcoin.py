from random import randint
import hashlib
#secp256k1 parameters, the ones used in bitcoin
Pcurve = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 -1 # The proven prime
Order=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 # Number of points in the field
Acurve = 0; Bcurve = 7 # These two defines the elliptic curve. y^2 = x^3 + Acurve * x + Bcurve
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
GPoint = (Gx,Gy) # This is our generator point. Trillions of dif ones possible
primeModulo = 67

userMessage = raw_input("Message to receiver: ")
privKeyInput = raw_input("Private Key: ")

privKey = int(privKeyInput, 16)
privKeyDead = 75263518707598184987916378021939673586055614731957507592904438851787542395619
randomNumber = randint(0, Order-1)
HashMessage = int(hashlib.sha256("userMessage").hexdigest(), 16)

def ellipticAddition(basePoint, otherPoint):
	lamda = ((otherPoint[1]-basePoint[1])*(pow(otherPoint[0]-basePoint[0], Pcurve-2, Pcurve)))%Pcurve
	rsubx = ((lamda**2)-basePoint[0]-otherPoint[0])%Pcurve
	rsuby = (lamda*(basePoint[0]-rsubx)-basePoint[1])%Pcurve
	return rsubx, rsuby

def ellipticMultiplication(basePoint):
	lamda = ((3*(basePoint[0]**2))*pow(2*basePoint[1],Pcurve-2,Pcurve))%Pcurve
	rsubx = ((lamda**2)+(-2*basePoint[0]))%Pcurve
	rsuby = (lamda*(basePoint[0]-rsubx)-basePoint[1])%Pcurve
	return rsubx, rsuby

def doubleAndAdd(basePoint, privateKey):
	if privateKey == 0 or privateKey >= Order: raise Exeption("Invalid private key")
	maxLength = str(bin(privateKey))[2:]
	Q = basePoint
	for i in range(1, len(maxLength)):
		Q=ellipticMultiplication(Q)
		if maxLength[i] == '1':
			Q=ellipticAddition(Q, basePoint)
	return (Q)
	


PublicKey = (doubleAndAdd(GPoint, privKey))
print "the uncompressed public key (HEX):"; 
print "04" + "%064x" % PublicKey[0] + "%064x" % PublicKey[1]; 
print;
print "the official Public Key - compressed:";
if PublicKey[1] % 2 == 1: # If the Y value for the Public Key is odd.
    print "03"+str(hex(PublicKey[0])[2:-1]).zfill(64)
else: # Or else, if the Y value is even.
    print "02"+str(hex(PublicKey[0])[2:-1]).zfill(64)

print "Signature Generation"
coordinateRandom = doubleAndAdd(GPoint, randomNumber)
xCoordinateRandom = coordinateRandom[0]
rCoordinate = xCoordinateRandom%Order
sCoordinate = ((HashMessage+rCoordinate*privKey)*(pow(randomNumber, Order-2, Order)))%Order
print(sCoordinate)


print "Signature Verification"
wCoor = pow(sCoordinate, Order-2, Order)
uCoor = (HashMessage*wCoor)%Order
vCoor = (rCoordinate*wCoor)%Order
uG = doubleAndAdd(GPoint, uCoor)
uV = doubleAndAdd(PublicKey, vCoor)
uGuV = (uG, uV)
xy = ellipticAddition(uGuV[0], uGuV[1])
if rCoordinate == (xy[0]%Order):
	print("Verified!!!!")
else:
	print("Oh no not verfied")









