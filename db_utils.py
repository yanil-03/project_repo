from sqlalchemy import create_engine
import pandas as pd
import secret_config, encoders_util

# Create and return SQL connection engine
def get_engine():
    return create_engine(secret_config.config_db)


# # SQL table name
# table_name = 'internship_table'

# # Chunk size for reading CSV
# chunksize = 1000

# # Create engine
# engine = get_engine()

# # Read and insert first chunk using if_exists='replace' to create the table
# first_chunk = pd.read_csv('intern1.csv', nrows=chunksize)
# first_chunk.to_sql(table_name, con=engine, if_exists='replace', index=False)
# print(f"Inserted first chunk of {chunksize} rows, table created.")

# # Append remaining chunks, skipping first chunk rows with header
# for chunk in pd.read_csv('intern1.csv', skiprows=range(1, chunksize + 1), chunksize=chunksize):
#     chunk.to_sql(table_name, con=engine, if_exists='append', index=False)
#     print(f"Appended chunk of {len(chunk)} rows.")

# print("All data converted and inserted successfully!")


# Load data from diet_table
def load_sample_data():
    engine = get_engine()
    query = 'SELECT * FROM sample_data_table'
    return pd.read_sql(query, engine)

def load_data_internship():
    engine = get_engine()
    query = 'SELECT * FROM internship_table'
    return pd.read_sql(query, engine)

def load_skills_data():
    engine = get_engine()
    query = 'SELECT * FROM skills_table'
    return pd.read_sql(query, engine)

def load_interests_data():
    engine = get_engine()
    query = 'SELECT * FROM interests_table'
    return pd.read_sql(query, engine)

# df = load_skills()
# print(df.tail(10))


def save_user_prediction(can_id, name, age, skill, interest, education, location, city, pred):
    skill_id = get_skill_by_name(skill)
    interest_id = get_interest_by_name(interest)
    engine = get_engine()
    feature_columns = ['Candidate_ID', 'Name', 'Age', 'Skill_ID', 'Interest_ID', 'Education', 'LocationPreference', 'CityPreference', 'SuggestedInternship']
    try:
        # Compose single row input data with counter as User_ID
        input_data = [[can_id, name, age, skill_id, interest_id, education, location, city, pred]]
        df = pd.DataFrame(input_data, columns=feature_columns)
        df.to_sql('candidates_data_table', engine, if_exists='append', index=False)
        print(f"Saved record: \n\n{df}")
    except Exception as e:
        print(f"Error saving user prediction record: {e}")

def skills_lts(list):
    list_sorted = sorted(list)
    str_list =  ', '.join(list_sorted)
    str_list = str(str_list)
    return str_list

def get_skill_by_name(skill):
    # skill = str(skill)
    skill = skills_lts(skill)
    print(skill)
    skills_df = load_skills_data()
    skill_row = skills_df[skills_df['new_skills'] == skill]
    if not skill_row.empty:
        print(skill_row['Skill_ID'].values[0])
        return skill_row['Skill_ID'].values[0]
    else:
        print("Skill ID not found.")
        return 0

# def interest_lts(list):
#     list_sorted = sorted(list)
#     str_list =  ', '.join(list_sorted)
#     str_list = str(str_list)
#     return str_list

def get_interest_by_name(interest):
    
    interest = skills_lts(interest)
    print(interest)
    interest_df = load_interests_data()
    interest_row = interest_df[interest_df['Interests_str'] == interest]
    if not interest_row.empty:
        print(interest_row['Interest_ID'].values[0])
        return interest_row['Interest_ID'].values[0]
    else:
        print("Interest ID not found.")
        return 0
