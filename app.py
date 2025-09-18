
# app.py
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Add this import
import json, encoders_util, db_utils, random, joblib
internships_df = db_utils.load_data_internship()
model = joblib.load("model.pkl")
app = Flask(__name__)
CORS(app)  # Add this to handle CORS if needed

@app.route('/')
def home():
    return render_template('frontend.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Get all form data
        form_data = request.form.to_dict()
        name = form_data['name']
        candidateId = form_data['candidateId']
        age = form_data['age']
        education = form_data['education']
        locationPreference = form_data['locationPreference']
        cityPreference = form_data['cityPreference']
        
        # Get skills and interests as lists (they're sent as multiple values with the same key)
        skills = request.form.getlist('skills')
        interests = request.form.getlist('interests')
        
        
        input_features = prepare_input_data(education, skills, interests)
        # for i in input_features:
        #     print("----------------")
        #     print(i)
        
        
        predicted_role_en = model.predict(input_features)[0]
        predicted_role = encoders_util.Internships_lb.inverse_transform([predicted_role_en])
        predicted_role = db_utils.skills_lts(predicted_role)
        print(predicted_role)
        
        # save_user_prediction(can_id, name, age, skill, interest, education, location, city, pred):
        db_utils.save_user_prediction(candidateId, name, age, skills, interests, education, locationPreference, cityPreference, predicted_role)

        

        filtered_internships = internships_df[
            (internships_df['InternshipRole'] == predicted_role) &
            (internships_df['InternshipType'] == locationPreference)
        ]
        
        if cityPreference and cityPreference != 'other':
            filtered_internships = filtered_internships[filtered_internships['CityLocation'] == cityPreference]
        
        # If no matches found, broaden the search
        if len(filtered_internships) == 0:
            filtered_internships = internships_df[internships_df['InternshipRole'] == predicted_role]
        
        # Select top 4 internships
        top_internships = filtered_internships.head(4).to_dict('records')
        
        # Create internship cards
        cards_html = create_internship_cards(top_internships)
        
        return jsonify({'html': cards_html})
        
    except Exception as e:
        print(f"Error processing form: {str(e)}")
        return jsonify({"error": str(e)}), 500
    

# def create_internship_cards(internships):
#     card_template = '''
#     <div class="result-card">
#         <h3>{title}</h3>
#         <p><strong>Company:</strong> {company}</p>
#         <p><strong>Location:</strong> {location}</p>
#         <p><strong>Duration:</strong> {duration}</p>
#         <p><strong>Stipend:</strong> {stipend}</p>
#         <p><strong>Match Score:</strong> {match_score}%</p>
#         <a href="#" class="btn btn-primary">Apply Now</a>
#     </div>'''
    
#     html_output = '<div class="result-cards">\n'
#     for internship in internships:
#         html_output += card_template.format(
#             title=internship['InternshipRole'],
#             company=internship['Organization'],
#             location=f"{internship['CityLocation']} ({internship['InternshipType']})",
#             duration=internship['Duration'],
#             stipend=internship['Stipend'],
#             match_score=random.randint(80, 95)  # Random match score for demo
#         )
#     html_output += '\n</div>'
#     return html_output
def create_internship_cards(internships):
    if not internships:
        return '<div class="no-results"><p>No internships found matching your criteria. Please try different preferences.</p></div>'
    
    cards_html = '<div class="result-cards">'
    for internship in internships:
        cards_html += f'''
        <div class="result-card">
            <h3>{internship.get('InternshipRole', 'Internship')}</h3>
            <p><strong>Company:</strong> {internship.get('Organization', 'Unknown')}</p>
            <p><strong>Location:</strong> {internship.get('CityLocation', 'Unknown')} ({internship.get('InternshipType', 'Unknown')})</p>
            <p><strong>Duration:</strong> {internship.get('Duration', 'Unknown')}</p>
            <p><strong>Stipend:</strong> {internship.get('Stipend', 'Unknown')}</p>
            <p><strong>Match Score:</strong> {random.randint(80, 95)}%</p>
            <a href="#" class="btn btn-primary">Apply Now</a>
        </div>'''
    cards_html += '</div>'
    return cards_html



def prepare_input_data(education, skills, interests):
    # Encode education
    edu_en = encoders_util.Education_lb.fit_transform([education])[0]#_encoder.transform(education)[0]
    skills_encoded = db_utils.get_skill_by_name(skills)
 
    # Encode interests (assuming you have a way to handle multiple interests)
    interests_encoded = db_utils.get_interest_by_name(interests)
    
    
    
    
    
    # This is a simplified input - you need to match the exact features your model expects
    input_features = np.array([
         
        skills_encoded, 
        interests_encoded,
        edu_en

    ]).reshape(1, -1)
    # print(f"INPUT_FEATURES : {input_features}")
    return input_features   


if __name__ == '__main__':
    app.run(debug=True)