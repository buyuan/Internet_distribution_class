import random
def getRandomPwd():
    pwd = random.choice('!@#$%^&*()')
    pwd += random.choice('0123456789')
    pwd += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    for i in range(6):
        pwd += random.choice('abcdefghijklmnopqrstuvwxyz')
    return pwd

print(getRandomPwd())