"""
computeSales.py: Este script procesa registros de ventas
a partir de archivos JSON y calcula el total de ventas,
manejando errores y generando un informe.
"""

import json
import sys
import time


def load_json_file(file_path):
    """Carga un archivo JSON y maneja errores si el archivo no existe o
    está malformado."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: El archivo {file_path} no fue encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Error: El archivo {file_path} tiene un formato JSON inválido.")
        return None


def process_sales(product_list, sales_data, sales_file_name):
    """Calcula el costo total de las ventas basado en la lista de productos
    y maneja errores en los datos."""

    # Convertir la lista de productos en un diccionario {producto: precio}
    price_catalog = {product["title"]: product["price"]
                     for product in product_list}

    total_sales = 0  # Variable para almacenar suma total de todas las ventas
    errors = []  # Lista para almacenar errores encontrados

    # Procesar cada venta
    for sale in sales_data:
        product_name = sale.get("Product")
        quantity = sale.get("Quantity", 0)

        # Ignorar ventas con cantidades negativas
        if quantity < 0:
            errors.append(f"[{sales_file_name}] Cantidadignorada {product_name}: {quantity}")  # noqa: E501
            continue

        # Si producto no en catálogo asignarle precio 0 y registrar advertencia
        if product_name not in price_catalog:
            errors.append(f"[{sales_file_name}] Producto no encontrado en catálogo: {product_name} (Asignado precio $0.00)")  # pylint: disable=line-too-long # noqa: E501
            price_catalog[product_name] = 0.00  # Asignar un precio de $0.00

        # Calcular costo de la venta
        product_price = price_catalog[product_name]
        sale_cost = quantity * product_price
        total_sales += sale_cost

    return total_sales, errors


def main():
    """Función principal que gestiona la ejecución del programa."""

    # Verificar que los argumentos sean correctos
    if len(sys.argv) != 5:
        print("Uso: python computeSales.py <ProductList.json> <Sales1.json> <Sales2.json> <Sales3.json>")  # pylint: disable=line-too-long # noqa: E501
        sys.exit(1)

    # Capturar tiempo de inicio
    start_time = time.time()

    # Obtener los nombres de archivos desde los argumentos de línea comandos
    product_file = sys.argv[1]
    sales_files = sys.argv[2:]  # Lista con los tres archivos de ventas

    # Cargar el archivo de productos
    product_list = load_json_file(product_file)
    if product_list is None:
        sys.exit(1)

    # Variables para almacenar los resultados de todos los archivos
    total_global_sales = 0
    all_errors = []

    # Procesar cada archivo de ventas
    results_text = "### Resultados de Ventas ###\n"
    for sales_file in sales_files:
        sales_data = load_json_file(sales_file)
        if sales_data is None:
            continue

        total_sales, errors = process_sales(product_list, sales_data, sales_file)  # noqa: E501
        total_global_sales += total_sales
        all_errors.extend(errors)

        # Formatear los resultados de cada archivo
        results_text += f"\nArchivo procesado: {sales_file}\n"
        results_text += f"Total de ventas: ${total_sales:,.2f}\n"

    # Capturar tiempo de fin y calcular duración
    execution_time = time.time() - start_time

    # Agregar información global
    results_text += "\n### Resumen Global ###\n"
    results_text += f"Total de ventas combinadas: ${total_global_sales:,.2f}\n"
    results_text += f"Tiempo de ejecución: {execution_time:.4f} segundos\n"

    # Mostrar errores si los hay
    if all_errors:
        results_text += "\n### Advertencias Encontradas ###\n"
        results_text += "\n".join(all_errors) + "\n"

    # Imprimir resultado en pantalla
    print(results_text)

    # Guardar resultado en un solo archivo de salida
    with open("SalesResults.txt", "w", encoding="utf-8") as result_file:
        result_file.write(results_text)


if __name__ == "__main__":
    main()
