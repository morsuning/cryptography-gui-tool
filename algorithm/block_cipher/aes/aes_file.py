# -*- coding:utf-8 -*-


class AESE():

    def __init__(self,blk,key,Nr):
        self.blk=blk
        self.key=key
        self.Nr=Nr
        self.sbox=( 0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
                    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
                    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
                    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
                    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
                    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
                    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
                    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
                    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
                    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
                    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
                    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
                    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
                    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
                    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
                    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16 )
#xtime process
    def xtime(self,x):
        if(x&0x80):
            return (((x<<1)^0x1b)&0xff)
        return x<<1
#MixColumns: Process the entire block
    def MixColumns(self):
        tmp=[0 for t in range(4)]
        xt=[0 for q in range(4)]
        n=0
        for x in range(4):
            xt[0]=self.xtime(self.blk[n])
            xt[1]=self.xtime(self.blk[n+1])
            xt[2]=self.xtime(self.blk[n+2])
            xt[3]=self.xtime(self.blk[n+3])
            tmp[0]=xt[0]^xt[1]^self.blk[n+1]^self.blk[n+2]^self.blk[n+3]
            tmp[1]=self.blk[n]^xt[1]^xt[2]^self.blk[n+2]^self.blk[n+3]
            tmp[2]=self.blk[n]^self.blk[n+1]^xt[2]^xt[3]^self.blk[n+3]
            tmp[3]=xt[0]^self.blk[n]^self.blk[n+1]^self.blk[n+2]^xt[3]
            self.blk[n]=tmp[0]
            self.blk[n+1]=tmp[1]
            self.blk[n+2]=tmp[2]
            self.blk[n+3]=tmp[3]
            n=n+4
#ShiftRows:Shifts the entire block
    def ShiftRows(self):
        #2nd row
        t=self.blk[1]
        self.blk[1]=self.blk[5]
        self.blk[5]=self.blk[9]
        self.blk[9]=self.blk[13]
        self.blk[13]=t
        #3nd row
        t=self.blk[2]
        self.blk[2]=self.blk[10]
        self.blk[10]=t
        t=self.blk[6]
        self.blk[6]=self.blk[14]
        self.blk[14]=t
        #4nd row
        t=self.blk[15]
        self.blk[15]=self.blk[11]
        self.blk[11]=self.blk[7]
        self.blk[7]=self.blk[3]
        self.blk[3]=t
#SubBytes
    def SubBytes(self):
        for x in range(16):
            self.blk[x]=self.sbox[self.blk[x]]
#AddRoundKey
    def AddRoundKey(self,key):
        x=0
        k=[0 for m in range(16)]
        for c in range(4):
            for r in range(4):
                k[x]=key[r][c]
                x=x+1
        for y in range(16):
            self.blk[y]^=int(k[y])

    def show(self):
        for i in range(16):
            print(hex(self.blk[i]))
# Schedule a secret key for use.
    def ScheduleKey(self,w,Nk):
        Rcon=[0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1b,0x36]
        for r in range(4):
            for c in range(4):
                w[0][r][c]=self.key[r+c*4]
        for i in range(1,self.Nr+1,1):
            for j in range(Nk):
                t=[0 for x in range(4)]
                for r in range(4):
                    if j :
                        t[r]=w[i][r][j-1]
                    else:
                        t[r]=w[i-1][r][3]
                if j==0:
                    temp=t[0]
                    for r in range(3):
                        t[r]=self.sbox[t[(r+1)%4]]
                    t[3]=self.sbox[temp]
                    t[0]^=int(Rcon[i-1])
                for r in range(4):
                    w[i][r][j]=w[i-1][r][j]^t[r]

    #加密函数
    def AesEncrypt(self):
        outkey=[]
        outkey=[[[0 for  col in range(4)] for row in range(4)] for s in range(11)]
        self.ScheduleKey(outkey,4)
        self.AddRoundKey(outkey[0])
        for x in range(1,self.Nr,1):
            self.SubBytes()
            self.ShiftRows()
            self.MixColumns()
            self.AddRoundKey(outkey[x])
        self.SubBytes()
        self.ShiftRows()
        self.AddRoundKey(outkey[10])
        cText = ""
        return self.blk

class AESD():
    def __init__(self,blk,key,Nr):
        self.blk=blk
        self.key=key
        self.Nr=Nr
        self.sbox=( 0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
                    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
                    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
                    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
                    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
                    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
                    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
                    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
                    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
                    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
                    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
                    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
                    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
                    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
                    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
                    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16 )

    def xtime(self,x):
        if(x&0x80):
            return (((x<<1)^0x1b)&0xff)
        return x<<1

    def ReMixColumns(self):
        tmp=[0 for q in range(4)]
        xt1=[0 for w in range(4)]
        xt2=[0 for e in range(4)]
        xt3=[0 for r in range(4)]
        n=0
        for x in range(4):
            xt1[0]=self.xtime(self.blk[n])
            xt1[1]=self.xtime(self.blk[n+1])
            xt1[2]=self.xtime(self.blk[n+2])
            xt1[3]=self.xtime(self.blk[n+3])
            xt2[0]=self.xtime(self.xtime(self.blk[n]))
            xt2[1]=self.xtime(self.xtime(self.blk[n+1]))
            xt2[2]=self.xtime(self.xtime(self.blk[n+2]))
            xt2[3]=self.xtime(self.xtime(self.blk[n+3]))
            xt3[0]=self.xtime(self.xtime(self.xtime(self.blk[n])))
            xt3[1]=self.xtime(self.xtime(self.xtime(self.blk[n+1])))
            xt3[2]=self.xtime(self.xtime(self.xtime(self.blk[n+2])))
            xt3[3]=self.xtime(self.xtime(self.xtime(self.blk[n+3])))
            tmp[0]=xt1[0]^xt2[0]^xt3[0]^ self.blk[n+1]^xt1[1]^xt3[1]^ self.blk[n+2]^xt2[2]^xt3[2]^self.blk[n+3]^xt3[3]
            tmp[1]=self. blk[n]^xt3[0]^xt1[1]^xt2[1]^xt3[1]^ self.blk[n+2]^xt1[2]^xt3[2]^ self.blk[n+3]^xt2[3]^xt3[3]
            tmp[2]= self.blk[n]^xt2[0]^xt3[0]^ self.blk[n+1]^xt3[1]^xt1[2]^xt2[2]^xt3[2]^ self.blk[n+3]^xt1[3]^xt3[3]
            tmp[3]=self. blk[n]^xt1[0]^xt3[0]^self. blk[n+1]^xt2[1]^xt3[1]^ self.blk[n+2]^xt3[2]^xt1[3]^xt2[3]^xt3[3]
            self.blk[n]=tmp[0]
            self.blk[n+1]=tmp[1]
            self.blk[n+2]=tmp[2]
            self.blk[n+3]=tmp[3]
            n=n+4

    def ReShiftRows(self):
        #2nd row
        t=self.blk[13]
        self.blk[13]=self.blk[9]
        self.blk[9]=self.blk[5]
        self.blk[5]=self.blk[1]
        self.blk[1]=t
        #3rd row
        t=self.blk[2]
        self.blk[2]=self.blk[10]
        self.blk[10]=t
        t=self.blk[6]
        self.blk[6]=self.blk[14]
        self.blk[14]=t
        #4th row
        t=self.blk[3]
        self.blk[3]=self.blk[7]
        self.blk[7]=self.blk[11]
        self.blk[11]=self.blk[15]
        self.blk[15]=t

    def ReSubBytes(self):
        for i in range(16):
            for j in range(256):
                if(self.sbox[j]==self.blk[i]):
                    self.blk[i]=j
                    break

    def AddRoundKey(self,key):
        x=0
        k=[0 for m in range(16)]
        for c in range(4):
            for r in range(4):
                k[x]=key[r][c]
                x=x+1
        for y in range(16):
            self.blk[y]^=k[y]

    def ScheduleKey(self,w,Nk):
        Rcon=[0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1b,0x36]
        for r in range(4):
            for c in range(4):
                w[0][r][c]=self.key[r+c*4]
        for i in range(1,self.Nr+1,1):
            for j in range(Nk):
                t=[0 for x in range(4)]
                for r in range(4):
                    if j :
                        t[r]=w[i][r][j-1]
                    else:
                        t[r]=w[i-1][r][3]
                if j==0:
                    temp=t[0]
                    for r in range(3):
                        t[r]=self.sbox[t[(r+1)%4]]
                    t[3]=self.sbox[temp]
                    t[0]^=int(Rcon[i-1])
                for r in range(4):
                    w[i][r][j]=w[i-1][r][j]^t[r]

    def AesDecrpyt(self):
        outkey=[]
        outkey=[[[0 for  col in range(4)] for row in range(4)] for s in range(11)]
        self.ScheduleKey(outkey,4)
        self.AddRoundKey(outkey[10])
        self.ReShiftRows()
        self.ReSubBytes()
        for x in range(self.Nr-1,0,-1):
            self.AddRoundKey(outkey[x])
            self.ReMixColumns()
            self.ReShiftRows()
            self.ReSubBytes()
        self.AddRoundKey(outkey[0])
        return self.blk

def StringToListN(string):
    s=[0 for x in range(16)]
    l=len(string)
    for x in range(l):
        s[x]=int(ord(string[x]))
    return s

def HexToInt(string):
    s = [0 for x in range(16)]
    for i in range(16):
        s[i]=int(string[2*i:2*i+2],16)
    return s

def encrypt(filename, skey, newfilename):
    f1=open(filename,"rb")
    data=f1.read()
    f1.close()
    key = StringToListN(skey)
    f2 = open(newfilename, "wb")
    number = int(len(data) / 16)
    if (len(data) % 16 != 0):
        number = number + 1
    for i in range(0, number):
        blk=[0 for x in range(16)]
        tmp=data[i*16:i*16+16]
        for j in range(len(tmp)):
           blk[j]=int(tmp[j])
        a = AESE(blk, key, 10)
        f2.write(bytes(a.AesEncrypt()))
    f2.close()
def decrypt(filename, skey, newfilename):
    f1 = open(filename, "rb")
    data = f1.read()
    key = StringToListN(skey)
    f2 = open(newfilename, "wb")
    number = int(len(data) / 16)
    if (len(data) % 16 != 0):
        number = number + 1
    for i in range(0, number):
        blk=[0 for x in range(16)]
        tmp=data[i*16:i*16+16]
        for j in range(len(tmp)):
           blk[j]=int(tmp[j])
        a = AESD(blk, key, 10)
        f2.write(bytes(a.AesDecrpyt()))
    f2.close()





