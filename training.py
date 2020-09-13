import os
import csv
import pickle
import numpy as np
import imageio
from mtcnn.mtcnn import MTCNN
from sklearn.svm import SVC
import face_recognition


# Path to directory containing images to train
PATH = "./training_pics"

# Filename to save model as
MODEL_FILENAME = "model.sav"

# Filename to save students' names
CSV_FILE = "students.csv"

names = os.listdir(PATH)
mapping = {v: i for i, v in enumerate(names)}

with open(CSV_FILE, "w") as file:
    rows_list = [{"roll_num": i, "name": v} for i, v in enumerate(names)]
    writer = csv.DictWriter(f=file, fieldnames=["roll_num", "name"])
    writer.writerows(rows_list)

detector = MTCNN()

labels = []
face_images = []
encodings = []
for folder in names:
    path_folder = f"{PATH}/{folder}"
    print(f"Training {path_folder}")

    for image in os.listdir(path_folder):
        img = imageio.imread(f"{path_folder}/{image}")
        faces = detector.detect_faces(img)

        if len(faces) != 0:
            face_images.append(img)
            box = faces[0]["box"]
            box = (box[1], box[0] + box[2], box[1] + box[3], box[0])
            encodings.append(face_recognition.face_encodings(img, [box]))
            labels.append(mapping[folder])

        else:
            print(f"{path_folder}/{image} not detected")

face_image_encodings = np.array(encodings)
face_image_labels = np.array(labels)

model = SVC(kernel="rbf", probability=True)
model.fit(
    np.reshape(face_image_encodings, (face_image_encodings.shape[0], 128)),
    face_image_labels,
)

model.score(
    np.reshape(face_image_encodings, (face_image_encodings.shape[0], 128)),
    face_image_labels,
)

pickle.dump(model, open(MODEL_FILENAME, "wb"))
