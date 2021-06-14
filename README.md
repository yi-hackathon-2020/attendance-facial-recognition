# Attendance Using Facial Recognition

Our submission for the YI InnovIndia Hackathon 2020, conducted on 31st July, 2020.

## Installing Dependencies

The following instructions are primarily aimed at Linux users.

- Install the `cmake` package using your distribution's package manager.
- Clone the repository and switch to the project directory.

  ```shell
  $ git clone https://github.com/yi-hackathon-2020/attendance-facial-recognition
  $ cd attendance-facial-recognition
  ```

- Install [`poetry`](https://python-poetry.org/docs/) if not installed already.
  Then, install Python requirements using `poetry`:

  ```shell
  poetry install
  ```

- Activate the virtual environment:

  ```shell
  poetry shell
  ```

## Training

- Ensure that the required directory structure is followed. The directory
  assigned to `PATH` in `training.py` should have images stored in directories
  with the name the model has to identify the person with. The names of image
  files themselves doesn't matter.

  An example directory structure would be:

  ```sh
  $ tree training_pics
  training_pics
  ├── person1 name
  │   ├── image1.jpg
  ╎   ╎
  │   └── imageN.jpg
  ├── person2 name
  │   ├── image1.jpg
  ╎   ╎
  │   └── imageN.jpg
  ╎
  └── personN name
      ├── image1.jpg
      ╎
      └── imageN.jpg
  ```

- Once the images follow the expected directory structure, train the model by
  running `python3 training.py`.

  ```sh
  $ python3 training.py
  Training ./training_pics/person1 name
  Training ./training_pics/person2 name
  ⋮
  Training ./training_pics/personN name
  ```

  This also generates a CSV file, `students.csv`, which is to be imported to the
  database.

## Running

- Create the database and table(s). Then, import the list of students into the
  database:

  ```sh
  $ # Creates the database and tables
  $ python3 database.py

  $ sqlite3 studentdb.db
  sqlite> .mode csv
  sqlite> .import students.csv students
  sqlite> .quit
  ```

- Run the application.

  ```sh
  python3 app.py
  ```
