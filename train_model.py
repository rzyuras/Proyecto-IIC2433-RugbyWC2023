import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import matplotlib.pyplot as plt

data = pd.read_csv('rugby_data_with_elo.csv')

# Filter los datos desde el 2004 para trabajar con Elos más reales
data = data[data['Date'] >= '2004-01-01']

# Borramos todas las filas de partidos de los British and Irish Lions
data = data[(data['Home Team'] != 'LIO') & (data['Away Team'] != 'LIO')]

# Una fila tiene un valor nulo para 'Neutral' asi que los seteamos en 0
data['Neutral'].fillna(0, inplace=True)

# Seleccionamos los datos que nos interesan para el modelo
df = data[['Home Score', 'Away Score', 'Home Rank', 'Away Rank', 'Home Elo', 'Away Elo', 'Neutral']]

# Separamos en X e y
X = df[['Home Rank', 'Away Rank', 'Home Elo', 'Away Elo', 'Neutral']]
y = df[['Home Score', 'Away Score']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = Sequential()
model.add(Dense(15, input_dim=5, kernel_initializer='normal', activation='relu'))
model.add(Dense(8, kernel_initializer='normal', activation='relu'))
model.add(Dense(2, kernel_initializer='normal'))

model.compile(loss='mean_squared_error', optimizer='adam')

test_size = 0.2
batch_size = 25
epochs = 200
verbose = 0

history = model.fit(X_train_scaled, y_train, validation_split=0.25, epochs=epochs, batch_size=batch_size, verbose=verbose, validation_data=(X_test_scaled, y_test))

mse = model.evaluate(X_test_scaled, y_test)
print(f"Mean Squared Error: {mse}")