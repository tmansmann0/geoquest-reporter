import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import os
from fpdf import FPDF

# Function to generate the PDF report
def generate_pdf_report(df, output_pdf):
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

    insights_text = f"""
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
    """

    # Create a PDF instance
    pdf = FPDF()

    # Title page
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Quest Points Insights Report", ln=True, align='C')
    pdf.ln(20)

    # Add insights as text
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, insights_text)

    # Create and save the graphs
    graph1_path = "lifetime_points_distribution.png"
    plt.figure(figsize=(10, 6))
    plt.hist(df['Lifetime Points'], bins=50, color='blue', alpha=0.7, edgecolor='black')
    plt.title('Distribution of Lifetime Points (Granular)')
    plt.xlabel('Lifetime Points')
    plt.ylabel('Number of Users')
    plt.grid(True)
    plt.savefig(graph1_path)
    plt.close()

    graph2_path = "lifetime_points_pie_chart.png"
    sizes = [users_with_lifetime_points, total_users - users_with_lifetime_points]
    labels = ['Users with Lifetime Points', 'Users without Lifetime Points']
    colors = ['#66b3ff', '#ff9999']
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, explode=(0.1, 0), shadow=True)
    plt.title('Users with and without Lifetime Points')
    plt.savefig(graph2_path)
    plt.close()

    graph3_path = "validated_quests_distribution.png"
    plt.figure(figsize=(10, 6))
    plt.bar(df['Validated Quests'].value_counts().index, df['Validated Quests'].value_counts().values, color='purple', alpha=0.7, edgecolor='black')
    plt.title('Distribution of Validated Quests')
    plt.xlabel('Number of Validated Quests')
    plt.ylabel('Number of Users')
    plt.grid(True)
    plt.savefig(graph3_path)
    plt.close()

    # Add the graphs to the PDF, each on its own page
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, txt="Visual Insights", ln=True, align='C')
    pdf.ln(10)

    # Insert Graph 1 (Lifetime Points Distribution)
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, 'Distribution of Lifetime Points', ln=True)
    pdf.image(graph1_path, x=10, y=30, w=180)

    # Insert Graph 2 (Pie Chart: Users with/without Lifetime Points)
    pdf.add_page()
    pdf.cell(0, 10, 'Users with and without Lifetime Points', ln=True)
    pdf.image(graph2_path, x=40, y=30, w=120)

    # Insert Graph 3 (Validated Quests Distribution)
    pdf.add_page()
    pdf.cell(0, 10, 'Distribution of Validated Quests', ln=True)
    pdf.image(graph3_path, x=10, y=30, w=180)

    # Save the report
    pdf.output(output_pdf)

    # Clean up the temporary image files
    os.remove(graph1_path)
    os.remove(graph2_path)
    os.remove(graph3_path)

# Streamlit UI
st.title("Quest Points Insights Report Generator")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("File uploaded successfully!")
    
    if st.button("Generate PDF Report"):
        output_pdf = "quest_points_insights_report.pdf"
        generate_pdf_report(df, output_pdf)
        
        with open(output_pdf, "rb") as f:
            st.download_button("Download PDF Report", f, file_name=output_pdf)

