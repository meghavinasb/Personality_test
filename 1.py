import pandas as pd

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv("Book1.csv")

# Get unique t_code values
t_codes = df['t_code'].unique()

# Create an empty dictionary to store the split DataFrames
split_dfs = {}

# Iterate over each unique t_code
for t_code in t_codes:
    # Filter the DataFrame for the current t_code
    df_filtered = df[df['t_code'] == t_code]

    # Create a new DataFrame with the desired columns
    split_dfs[t_code] = pd.DataFrame({
        't_name': df_filtered['t_name'],
        'Response_1': df_filtered['Response_1'],
        'Response_2': df_filtered['Response_2'],
        'Response_3': df_filtered['Response_3']
    })

# Access the DataFrame for the t_code you want to use
df_t_code_1 = split_dfs[4]

def generate_personalized_quote(teacher_traits_csv):
    # Count and sort responses
    response_counts = pd.concat([df_t_code_1['Response_1'], 
                                 df_t_code_1['Response_2'], 
                                 df_t_code_1['Response_3']]).value_counts()

    top_3_traits = response_counts.index[:3].tolist()

    # Find matching quote
    df_quotes = pd.read_csv(teacher_traits_csv)
    matching_quotes = df_quotes[
        (df_quotes['Trait 1'].isin(top_3_traits)) & 
        (df_quotes['Trait 2'].isin(top_3_traits)) & 
        (df_quotes['Trait 3'].isin(top_3_traits))
    ]

    if matching_quotes.empty:
        return "No matching quote found for the top traits."

    matching_quote = matching_quotes['Quote'].iloc[0]
    teacher_counts = df_t_code_1['t_name'].value_counts()
    teacher = teacher_counts.idxmax()
    qu = matching_quote.replace("[This teacher]", teacher)
    return qu

traits_file = 'Top_traits.csv'
quote = generate_personalized_quote(traits_file)

# Write the output to a CSV file
output_df = pd.DataFrame({'Generated Quote': [quote]})
output_df.to_csv('Generated_Quote.csv', index=False)

print("Quote has been written to Generated_Quote.csv")
