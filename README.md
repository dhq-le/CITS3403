## Fitness Exercise Tracker Website (CITS3403) - Group 45

## Description
Our project is a fitness exercise tracker designed to help users log their workouts, monitor progress, and comparing with friends. The platform allows users to create and manage their exercise routines. This app will record and visualise progress overtime shown through graphs and history from previous workouts. 
### Members
| UWA ID| Name           |   Github User	 |
|:---------|:---------------|:---------------|
| 23625105 | Daniel Le      | dhq-le         |
| 23101312 | Mos Hassanein  | llullabyee     |
| 23940731 | Ritch Rayawang | Ritch-Wang     |
| 24260829 | Ziyuan Jiang   | Michae-ZY    |

## Environment Setup
1. Clone the repository. git clone https://github.com/dhq-le/CITS3403-Project.git

2. Create a virtual environment and activate it.

Windows:
```
python -m venv venv
venv\Scripts\activate
```


macOS/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

3. Install requirements.txt using:
```
pip install -r 'requirements.txt'
```

4. Initialise the database.
```
flask db upgrade
```
**NOTE:** If you are making any changes to the database, run this line first:
```
flask db migrate -m "comment"
```

5. Initialise the database.

Windows:
```
python init_db_rows.py
```
macOS/Linux:
```
python3 init_db_rows.py
```

6. Start the server.

Windows:
```
python run.py
```


macOS/Linux:
```
python3 run.py
```

## Testing Instructions	
To run both selenium and unit tests, run this command from the root directory (whilst in the virtual environment):

```
python -m unittest discover -s tests 
```
 



## Uploading to GitHub
If you install any dependencies, ensure that these are added to the requirements.txt file. 
This can either be done manually, or you can run:
```python
pip freeze > requirements.txt
```
OR
```python
pip3 freeze > requirements.txt
```

**NOTE:** When using pip freeze, ensure you are in the virtual environment, otherwise you risk adding any unnecessary modules installed on your computer.
