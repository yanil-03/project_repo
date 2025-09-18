import joblib, os

lb_names = []
# Function that loads all pkl files of the encoders with prefix lb 
def load_encoders():
    loaded_objects = {}
    folder_path = '.'
    for filename in os.listdir(folder_path):
        # Check filename starts with lb and ends with .pkl
        if filename.startswith('lb') and filename.endswith('.pkl'):
            full_path = os.path.join(folder_path, filename)
            obj = joblib.load(full_path)
            loaded_objects[filename] = obj
            lb_names.append(filename)
            # print(f"Loaded: {filename}")
    return loaded_objects

encoder = load_encoders()

try:
    Education_lb = encoder['lb_education.pkl']
except KeyError:
    print("Error: 'lb_education.pkl' encoder not found.")
    Education_lb = None



try:
    Internships_lb = encoder['lb_internships.pkl']
except KeyError:
    print("Error: 'lb_internships.pkl' encoder not found.")
    Location_lb = None



# d = ['CSS', 'Cloud', 'JavaScript']
# # get_skill_by_name(d)
# i = ['Web Development']
# i1 = ['AI', 'Data Science']
# get_interest_by_name(i1)