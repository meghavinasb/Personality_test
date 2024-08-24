from flask import Flask, render_template, request, jsonify
import csv

app = Flask(__name__)

# Define a route to render the HTML page
@app.route('/')
def index():
    return render_template('T1.html')

# Define a route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    selected_questions = request.json.get('questions')
    
    # Write the selected questions to a CSV file
    with open('feedback.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(selected_questions)
    
    return jsonify({"message": "Data saved successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
