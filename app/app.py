# PROGRAMA DESARROLLADO POR HERNANDEZ CHAVARRIA MAURICIO ANTONIO Y ANTONIO
import os
import sys

if __package__:
    from .gui import main
else:
    # Ejecutado como script (python app/app.py): se agrega la raiz del
    # proyecto al path para poder importar "app" como paquete.
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from app.gui import main


if __name__ == "__main__":
    main()
