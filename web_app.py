def sistema_de_ventas():
    carrito = []
    total_neto = 0
    iva_porcentaje = 0.19  # Ejemplo de IVA del 19%

    print("--- Bienvenido al Sistema de Ventas ---")
    
    while True:
        nombre = input("\nNombre del producto (o 'fin' para terminar): ")
        if nombre.lower() == 'fin':
            break
            
        try:
            precio = float(input(f"Precio de {nombre}: "))
            cantidad = int(input(f"Cantidad de {nombre}: "))
            
            subtotal = precio * cantidad
            carrito.append({
                "nombre": nombre,
                "precio": precio,
                "cantidad": cantidad,
                "subtotal": subtotal
            })
            total_neto += subtotal
        except ValueError:
            print("Error: Ingresa valores numéricos válidos.")

    # Cálculos finales
    valor_iva = total_neto * iva_porcentaje
    total_pagar = total_neto + valor_iva

    # Mostrar Recibo
    print("\n" + "="*30)
    print("      RESUMEN DE VENTA")
    print("="*30)
    for item in carrito:
        print(f"{item['cantidad']}x {item['nombre']}: ${item['subtotal']:.2f}")
    
    print("-" * 30)
    print(f"Subtotal:  ${total_neto:.2f}")
    print(f"IVA (19%): ${valor_iva:.2f}")
    print(f"TOTAL:     ${total_pagar:.2f}")
    print("="*30)

if __name__ == "__main__":
    sistema_de_ventas()
