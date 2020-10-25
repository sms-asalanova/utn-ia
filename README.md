# Genetic Algorithms

1. Project Structure  
```
├── LICENSE  
├── README.md  
├── algorithms  //Aqui se encuentra el algortimo.
├── datasets  
│   ├── 24  
│   │   ├── fechas.csv //total de fechas que se juegan
│   │   ├── localVisitante.csv  //fixture ejemplo
│   │   └── teams.csv   //todos los equipos que participan del torneo con su metadata
│   ├── cities.csv  //Ciudades participantes del torneo
│   └── distances.csv  //Matriz de distancias entre CIUDADES
├── models //Clases necesarias para correr el programa
├── main.py    
```
2. Dependencies  
2.1 [pandas](https://pandas.pydata.org/) version 1.1.3  
2.2 [matplotlib](https://matplotlib.org/) version 3.3.2  
    2.2.1  To test if matplotlib was installed correctly run:
    ```
    python3 test.py
    ```

3. Executing the project
```
python3 main.py
```
