### B4. Reiniciar un hilo

```python
import threading

hilo = threading.Thread(target=print, args=("hola",))
hilo.start()
hilo.join()
print(hilo.is_alive())
hilo.start()
```
##Tango dudas con este código, ¿por qué no puedo reiniciar un hilo en Python?
