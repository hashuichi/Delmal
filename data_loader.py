import streamlit as st
import pandas as pd
from datetime import datetime

class DataLoader:
    def __init__(self):
        self.revenue_path = 'revenue.csv'
        self.revenue = pd.read_csv(self.revenue_path)
        self.expenditure_path = 'expenditure.csv'
        self.expenditure = pd.read_csv(self.expenditure_path)

    def get_data(self):
        return self.data
    
    # TODO: Change this method to account for the separate rev and exp files
    def calculate_metrics(df, date):
        total_revenue = (df['Price'] * df['Quantity']).sum()
        total_expenditure = (df['Cost'] * df['Quantity']).sum()
        gross_profit = total_revenue - total_expenditure
        gross_profit_margin = (gross_profit / total_revenue) * 100 if total_revenue != 0 else 0
        cash_reserves = total_revenue - total_expenditure
        burn_rate = total_expenditure / len(df['Date'].unique()) if len(df['Date'].unique()) != 0 else 0
        
        return (
            round(total_revenue),
            round(total_expenditure),
            round(gross_profit_margin),
            round(cash_reserves),
            round(burn_rate)
        )
    
    def add(self, df, new_entry):
            if df == 'Revenue':
                self.revenue = pd.concat([self.revenue, pd.DataFrame([new_entry])], ignore_index=True)
                self.revenue.to_csv(self.revenue_path, index=False)
            elif df == 'Expenditure':
                self.expenditure = pd.concat([self.expenditure, pd.DataFrame([new_entry])], ignore_index=True)
                self.expenditure.to_csv(self.expenditure_path, index=False)
            else:
                raise ValueError("Incorrect value for df. Must be 'Revenue' or 'Expenditure'.")

    def delete(self, df, file, index):
        df = df.drop(index=index)
        df.to_csv(file, index=False)