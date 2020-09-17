# Attendance Using Facial Recognition

Our submission for the YI InnovIndia Hackathon 2020, conducted on 31st July, 2020.

## Installing Dependencies

The following instructions are primarily aimed at Linux users.

- Install the `cmake` package using your distribution's package manager.
- Clone the repository.
- `cd` into the project directory.
- Create a Python virtual environment (Python 3.3+):

  ```sh
  python3 -m venv venv
  ```

- Activate the virtual environment:

  ```sh
  source venv/bin/activate
  ```

- Install necessary libraries:

  ```sh
  pip install -r requirements.txt --use-feature=2020-resolver
  ```

  Additionally, to install development requirements (formatter, linter):

  ```sh
  pip install -r dev-requirements.txt --use-feature=2020-resolver
  ```

- Alternatively, with [`pipenv`](https://pipenv.pypa.io/en/latest/), this can be
  done using a single command:

  ```sh
  pipenv install
  ```

  Additionally, to install development requirements (formatter, linter):

  ```sh
  pipenv install --dev
  ```

  To spawn a shell in the created virtual environment:

  ```sh
  pipenv shell
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
