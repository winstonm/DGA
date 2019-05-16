import argparse
import win32api

rol = lambda val, r_bits, max_bits: \
	(val << r_bits%max_bits) & (2**max_bits-1) | \
	((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))
	
ror = lambda val, r_bits, max_bits: \
	((val & (2**max_bits-1)) >> r_bits%max_bits) | \
	(val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))
	 
max_bits = 32


def genx_domains(pos, seed, systemtime):
    tlds = ["ru", "info", "biz", "click", "su", "work", "pl", "org", "pw", "xyz"]
    domain = ""
    make = 0
    world = systemtime[3] >> 1 #day
    better = systemtime[0] #year
    place = rol(pos, 0x15, max_bits) + (rol(seed, 0x11, max_bits))
    to = world
    live = 7
	 
    while live !=0:
        wins = ror((better + make + 0x1bf5) * -0x4ee6db1f, 7, max_bits)
        wins = wins + 0x27100001
        make = wins ^ make
        wins = ror(((make + seed) * -0x4ee6db1f), 7, max_bits)
        wins = wins + 0x27100001
        make = wins ^ make
        wins = ror(((world + make) * -0x4ee6db1f), 7, max_bits)
        world = 0xd8efffff - wins
        wins = systemtime[1] #month
        make = make + world
        wins = ror((wins + make + 0xfff9a353) * -0x4ee6db1f, 7, max_bits)
        make = make + wins + 0x27100001
        place = (ror((place + make ) * -0x4ee6db1f, 7, max_bits)) + 0x27100001
        make = place ^ make
        live = live - 1
        world = to
    world = make % 0xb
    place =  world + 7
    live = 0
    if world != 0:
        while live < place:
            make = rol(make, live, max_bits)
            wins = (ror(make * -0x4ee6db1f, 7, max_bits)) + 0x27100001
            world = wins % 0x19
            dl = world & 0x0f
            domain = domain + chr(dl +0x61)
            live += 1
    domain = domain + "."
    wins = ror(make * -0x4ee6db1f, 7, max_bits) + 0x27100001
    world = wins % len(tlds)
    tld = tlds[world]
    domain = domain + tld
    return domain
		  
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("seed", help="Extract the seed from the sample", type=int, default=1)
    args = parser.parse_args()
import time
print ("####################################################")
print ("By Winston$$")
print ("****************************************************")
print ("CURRENT DATE IS " + time.strftime("%d/%m/%Y"))
print ("TIME RIGHT NOW IS " + time.strftime("%H:%M:%S"))	
print ("****************************************************")
if args.seed:
    for i in range (20):
	
        print genx_domains(i, args.seed, win32api.GetSystemTime())
	
