import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import os
from fpdf import FPDF

# Function to generate the report
def generate_report(df):
    # Insights
    total_users = df.shape[0]
    total_lifetime_points = df['Lifetime Points'].sum()
    total_current_points = df['Current Points'].sum()
    users_with_lifetime_points = df[df['Lifetime Points'] > 0].shape[0]
    average_lifetime_points = df['Lifetime Points'].mean()
    users_with_current_points = df[df['Current Points'] > 0].shape[0]
    average_current_points_active_users = df[df['Current Points'] > 0]['Current Points'].mean()
    max_lifetime_points = df['Lifetime Points'].max()
    max_current_points = df['Current Points'].max()
    total_validated_quests = df['Validated Quests'].sum()
    users_with_no_validated_quests_but_lifetime_points = df[(df['Validated Quests'] == 0) & (df['Lifetime Points'] > 0)].shape[0]

    insights_text = f\"\"\"
    Total Users: {total_users}
    Total Lifetime Points Awarded: {total_lifetime_points}
    Total Current Points Awarded: {total_current_points}
    Number of Users with Lifetime Points > 0: {users_with_lifetime_points}
    Average Lifetime Points per User: {average_lifetime_points:.2f}
    Users with Current Points > 0: {users_with_current_points}
    Average Current Points (For Users with Points): {average_current_points_active_users:.2f}
    Max Lifetime Points Held by a User: {max_lifetime_points}
    Max Current Points Held by a User: {max_current_points}
    Total Validated Quests: {total_validated_quests}
    Number of Users with Lifetime Points but No Validated Quests: {users_with_no_validated_quests_but_lifetime_points}
    \"\"\"

    st.text(insights_text)

    # Pie chart data for users with and without lifetime points
    sizes = [users_with_lifetime_points, total_users - users_with_lifetime_points]
    labels = ['Users with Lifetime Points', 'Users without Lifetime Points']
    colors = ['#66b3ff', '#ff9999']

    # Plot the charts and show in the Streamlit app
    st.subheader('Visual Insights')

    # Distribution of Lifetime Points
    fig, ax = plt.subplots()
    ax.hist(df['Lifetime Points'], bins=50, color='blue', alpha=0.7, edgecolor='black')
    ax.set_title('Distribution of Lifetime Points (Granular)')
    ax.set_xlabel('Lifetime Points')
    ax.set_ylabel('Number of Users')
    st.pyplot(fig)

    # Pie chart of Users with and without Lifetime Points
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, explode=(0.1, 0), shadow=True)
    ax.set_title('Users with and without Lifetime Points')
    st.pyplot(fig)

    # Bar chart for Validated Quests Distribution
    fig, ax = plt.subplots()
    ax.bar(df['Validated Quests'].value_counts().index, df['Validated Quests'].value_counts().values, color='purple', alpha=0.7, edgecolor='black')
    ax.set_title('Distribution of Validated Quests')
    ax.set_xlabel('Number of Validated Quests')
    ax.set_ylabel('Number of Users')
    st.pyplot(fig)

# Streamlit UI
st.title("Quest Points Insights Report Generator")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("File uploaded successfully!")
    
    if st.button("Generate Report"):
        generate_report(df)
