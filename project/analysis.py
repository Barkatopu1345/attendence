import matplotlib.pyplot as plt
import pandas as pd
  
  
# Initialize the lists for X and Y
data = pd.read_csv('test1.csv')

  
df = pd.DataFrame(data)
  
X = list(df.iloc[:, 0])
Y = list(df.iloc[:, 1])
  
# Plot the data using bar() method
plt.bar(X, Y, color='y')
plt.title("Face Recognization(%)")
plt.xlabel("Person")
plt.ylabel("Matching percentage(%)")
  
# Show the plot
plt.show()