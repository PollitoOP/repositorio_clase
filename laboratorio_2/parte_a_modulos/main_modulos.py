from cadenas import normalizar, slugify, validar_email, truncar_palabras

def demo():
    print("== MODULOS A ==")
    print(normalizar("  ¡Hola   MÚNDO!  "))            # "hola mundo"
    print(slugify("Python 3.12 – Módulos & Paquetes")) # "python-3-12-modulos-paquetes"
    print(truncar_palabras("uno dos tres cuatro cinco", 3))  # "uno dos tres"

    # Caso límite que debe producir error controlado:
    try:
        validar_email("no-es-valido@")
    except ValueError as e:
        print("Validación de email OK ->", e)

    # caso válido
    print(validar_email("user@example.com"))

if __name__ == "__main__":
    demo()
