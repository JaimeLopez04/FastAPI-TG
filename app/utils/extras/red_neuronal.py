'''
    Requerimientos para la ejecución de la red
    1. Instalar TensorFlow y Keras, numpy y demas librerias necesarias en Python, si no están instalados.
        pip install tensorflow
        pip install keras
        pip install numpy matplotlib scipy pandas sklearn seaborn
        
    2. Descargar el conjunto de datos FER2013 en formato CSV desde este enlace y almacenarlo en la carpeta data:
        https://www.kaggle.com/datasets/nicolejyt/facialexpressionrecognition
        
    3. Ejecutar el algoritmo, para esto se recomienda Google colab usando el entorno de ejecución A100 GPU
'''

# Importar las bibliotecas necesarias
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
from keras.models import Model
from keras.layers import Input, Conv2D, BatchNormalization, Activation, MaxPooling2D, Flatten, Dense, Dropout
from keras.optimizers import Adam
import tensorflow as tf

# Constantes
WIDTH, HEIGHT = 48, 48
NUM_CLASSES = 7
NUM_EPOCHS = 50
BATCH_SIZE = 32  # Modificación: reducción del tamaño del lote
NUM_FEATURES = 64

# Cargar datos
data = pd.read_csv('./data/fer2013.csv')

# Función para preprocesar los datos
def preprocess_data(df):
    pixels = df['pixels'].apply(lambda pixel_sequence: np.array([int(pixel) for pixel in pixel_sequence.split()]))
    max_shape = pixels.apply(lambda arr: arr.shape).max()
    pixels = pixels.apply(lambda arr: np.pad(arr, ((0, max_shape[0] - arr.shape[0])), mode='constant'))
    X = np.stack(pixels.values)
    X = X.reshape(-1, WIDTH, HEIGHT, 1) / 255.0
    Y = to_categorical(df['emotion'], NUM_CLASSES)
    return X, Y

# Dividir datos en entrenamiento, validación y prueba
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
val_data, test_data = train_test_split(test_data, test_size=0.5, random_state=42)

train_X, train_Y = preprocess_data(train_data)
val_X, val_Y = preprocess_data(val_data)
test_X, test_Y = preprocess_data(test_data)

# Construir modelo
inputs = Input(shape=(WIDTH, HEIGHT, 1))
x = Conv2D(2*2*NUM_FEATURES, kernel_size=(3, 3), activation='relu', kernel_initializer='he_normal')(inputs)
x = BatchNormalization()(x)
x = Conv2D(2*2*NUM_FEATURES, kernel_size=(3, 3), activation='relu', kernel_initializer='he_normal')(x)
x = BatchNormalization()(x)
x = MaxPooling2D(pool_size=(2, 2))(x)

x = Conv2D(2*NUM_FEATURES, kernel_size=(3, 3), activation='relu', kernel_initializer='he_normal')(x)
x = BatchNormalization()(x)
x = Conv2D(2*NUM_FEATURES, kernel_size=(3, 3), activation='relu', kernel_initializer='he_normal')(x)
x = BatchNormalization()(x)
x = MaxPooling2D(pool_size=(2, 2))(x)

x = Conv2D(NUM_FEATURES, kernel_size=(3, 3), activation='relu', kernel_initializer='he_normal')(x)
x = BatchNormalization()(x)
x = Conv2D(NUM_FEATURES, kernel_size=(3, 3), activation='relu', kernel_initializer='he_normal')(x)
x = BatchNormalization()(x)
x = MaxPooling2D(pool_size=(2, 2))(x)

x = Flatten()(x)
x = Dense(2*2*2*NUM_FEATURES, activation='relu', kernel_initializer='he_normal')(x)
x = BatchNormalization()(x)
x = Dropout(0.5)(x)  # Modificación: añadir dropout para regularización
x = Dense(2*2*NUM_FEATURES, activation='relu', kernel_initializer='he_normal')(x)
x = BatchNormalization()(x)
x = Dropout(0.5)(x)  # Modificación: añadir dropout para regularización
x = Dense(2*NUM_FEATURES, activation='relu', kernel_initializer='he_normal')(x)
x = BatchNormalization()(x)
outputs = Dense(NUM_CLASSES, activation='softmax')(x)


model = Model(inputs=inputs, outputs=outputs)
optimizer = Adam(learning_rate=0.001)  # Modificación: ajustar la tasa de aprendizaje
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

# Entrenar modelo
es = EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True)  # Modificación: aumentar la paciencia de EarlyStopping
history = model.fit(train_X, train_Y, batch_size=BATCH_SIZE, epochs=NUM_EPOCHS,
                    validation_data=(val_X, val_Y), callbacks=[es])


# Visualizar resultados
def plot_results(history):
    # Visualizar resultados
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    plt.show()

plot_results(history)

# Evaluar rendimiento en test set
test_pred = np.argmax(model.predict(test_X), axis=1)
test_true = np.argmax(test_Y, axis=1)
accuracy = accuracy_score(test_true, test_pred)
print(f'CNN Model Accuracy on test set: {accuracy:.4f}')

# Definición de etiquetas de las emociones
emotion_labels = ['Enojado', 'Disgusto', 'Miedo', 'Feliz', 'Triste', 'Sorpresa', 'Neutral']

# Matriz de confusión
cm = confusion_matrix(test_true, test_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=emotion_labels, yticklabels=emotion_labels)
plt.title('Confusion Matrix')
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.show()

# Guardar el modelo
model.save("emotion_model.h5")