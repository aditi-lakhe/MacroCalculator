import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def display_macro_pie_charts(recommendations_df):
    """
    Display expandable accordions with pie charts for macro breakdown of each dish.
    
    Parameters:
    recommendations_df (pd.DataFrame): DataFrame containing dish recommendations with 
                                       columns 'Dish', 'Calories', 'Protein', 'Carbs', 'Fats'
    """
    
    st.divider()
    st.subheader("Macro Breakdown by Dish")
    
    # Display the dataframe first
    
    
    st.divider()
    st.subheader(" Detailed Macro Analysis")
    
    # Create expandable sections for each dish
    for idx, (_, dish) in enumerate(recommendations_df[['Dish', 'Calories', 'Protein', 'Carbs', 'Fats']].head(10).iterrows()):
        with st.expander(f"🍽️ {dish['Dish']}"):
            # Prepare data for pie chart
            macro_data = {
                'Calories': dish['Calories'],
                'Protein': dish['Protein'],
                'Carbs': dish['Carbs'],
                'Fats': dish['Fats']
            }
            
            # Create pie chart
            fig, ax = plt.subplots(figsize=(3, 4))
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
            wedges, texts, autotexts = ax.pie(macro_data.values(), 
                                                labels=macro_data.keys(), 
                                                autopct='%1.1f%%',
                                                colors=colors,
                                                startangle=90,
                                                labeldistance=1.1,
                                                pctdistance=0.85)
            
            # Enhance text styling
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(8)
            
            for text in texts:
                text.set_fontsize(9)
                text.set_fontweight('bold')
            
            ax.set_title(f"Macro Breakdown - {dish['Dish']}", fontsize=11, fontweight='bold', pad=10)
            plt.tight_layout()
            
            st.pyplot(fig, width='stretch')
            
            # Display values in columns
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Calories", f"{dish['Calories']:.1f}")
            col2.metric("Protein", f"{dish['Protein']:.1f}g")
            col3.metric("Carbs", f"{dish['Carbs']:.1f}g")
            col4.metric("Fats", f"{dish['Fats']:.1f}g")
