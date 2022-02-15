import utime
print("Loop starting")
time_1 = utime.time()
while True:
    if utime.time() - time_1 > 5:
        break
    else:
        print(f"Time: {utime.time()}")
    utime.sleep(1)
print("Loop finished!")
