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

def generate_personalized_quotes(df_t_code_1, top_traits_file, low_traits_file):
    # Count and sort responses
    response_counts = pd.concat([df_t_code_1['Response_1'], 
                                 df_t_code_1['Response_2'], 
                                 df_t_code_1['Response_3']]).value_counts()

    # Top 3 traits
    top_3_traits = response_counts.index[:3].tolist()
    # Bottom 3 traits
    bottom_3_traits = response_counts.index[-3:].tolist()

    # Find matching quote for top 3 traits
    df_top_quotes = pd.read_csv(top_traits_file)
    matching_top_quotes = df_top_quotes[
        (df_top_quotes['Trait 1'].isin(top_3_traits)) & 
        (df_top_quotes['Trait 2'].isin(top_3_traits)) & 
        (df_top_quotes['Trait 3'].isin(top_3_traits))
    ]

    top_quote = "No matching quote found for the top traits."
    if not matching_top_quotes.empty:
        top_quote = matching_top_quotes['Quote'].iloc[0]

    # Find matching quote for bottom 3 traits
    df_low_quotes = pd.read_csv(low_traits_file)
    matching_low_quotes = df_low_quotes[
        (df_low_quotes['trait_1'].isin(bottom_3_traits)) & 
        (df_low_quotes['trait_2'].isin(bottom_3_traits)) & 
        (df_low_quotes['trait_3'].isin(bottom_3_traits))
    ]

    low_quote = "No matching quote found for the bottom traits."
    if not matching_low_quotes.empty:
        low_quote = matching_low_quotes['quotes'].iloc[0]

    # Replace placeholder with teacher's name
    teacher_counts = df_t_code_1['t_name'].value_counts()
    teacher = teacher_counts.idxmax()
    top_quote = top_quote.replace("[This teacher]", teacher)
    low_quote = low_quote.replace("[This teacher]", teacher)

    # Return both quotes
    return top_quote, low_quote

# Files containing the quotes for top and bottom traits
top_traits_file = 'Top_traits.csv'
low_traits_file = 'Low_traits.csv'

# Create a list to store the results
results = []

# Iterate over each t_code and generate quotes
for t_code in t_codes:
    df_t_code_1 = split_dfs[t_code]
    top_quote, low_quote = generate_personalized_quotes(df_t_code_1, top_traits_file, low_traits_file)
    results.append({'t_code': t_code, 'top_quote': top_quote, 'low_quote': low_quote})

# Convert the results to a DataFrame
results_df = pd.DataFrame(results)

# Save the DataFrame to a CSV file
results_df.to_csv('output_quotes.csv', index=False)

print("Output saved to output_quotes.csv")
