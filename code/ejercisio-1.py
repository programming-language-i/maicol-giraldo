import threading 
import time


def imprimir_mensaje():
    for i in range(5):
        print(f"{i + 1} hello")
        time.sleep(1)

def main():
    thread = threading.Thread(target=imprimir_mensaje)
    thread.start()


    print("finished")


if __name__ == "__main__":
    main() 
