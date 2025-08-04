import pandas as pd
import string
from typing import Optional

class TextCleaner:
    """
    Class for cleaning and preprocessing text data from Twitter dataset
    """
    def __init__(self, data: pd.DataFrame):
        "Initialize cleaner with dataset"
        self.original_data = data.copy()    
        self.cleaned_data = None
        
    def filter_relevant_columns(self) -> None:
        "Keep only relevant columns, 'text' and 'biased'"
        if 'Text' in self.original_data.columns and 'Biased' in self.original_data.columns:
            self.cleaned_data = self.original_data[['Text', 'Biased']].copy()
            print(f"Filtered to relevant columns. Shape: {self.cleaned_data.shape}")
        else:
            raise ValueError("Required columns 'Text' and 'Biased' not found in dataset")
        
    def remove_unclassified_tweets(self) -> None:
        "Remove tweets that don't have proper classification (0 or 1)"
        if self.cleaned_data is None:
            self.filter_relevant_columns()
        if self.cleaned_data is None:
            raise ValueError("cleaned_data is still None after attempting to filter relevant columns.")
            
        # Keep tweets with proper classification
        valid_mask = self.cleaned_data['Biased'].isin([0, 1])
        self.cleaned_data = self.cleaned_data[valid_mask].copy()
        
        removed_count = len(self.original_data) - len(self.cleaned_data)
        print(f"Removed {removed_count} unclassified tweets. Remaining: {len(self.cleaned_data)}")
        
    def remove_punctuation(self, text: str) -> str:
        "Remove punctuation from text"
        return text.translate(str.maketrans('', '', string.punctuation))
    
    def convert_to_lowercase(self, text: str) -> str:
        "Convert text to lowercase"
        return text.lower()
    
    def clean_text(self, text: str) -> str:
        "Apply all text cleaning operations"
        if pd.isna(text):
            return ""
        
        # Convert to string if not already
        text = str(text)
        
        # Remove punctuation
        text = self.remove_punctuation(text)
        
        # Convert to lowercase
        text = self.convert_to_lowercase(text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def clean_dataset(self) -> pd.DataFrame:
        "Apply all the above for the entire dataset"
        if self.cleaned_data is None:
            self.filter_relevant_columns()
        if self.cleaned_data is None:
            raise ValueError("cleaned_data is still None after attempting to filter relevant columns.")
        
        self.filter_relevant_columns()
        self.remove_unclassified_tweets()
        
        # Apply cleaning to all tweets
        self.cleaned_data['Text'] = self.cleaned_data['Text'].apply(self.clean_text)
        
        # Remove empty tweets after cleaning
        self.cleaned_data = self.cleaned_data[self.cleaned_data['Text'].str.len() > 0].copy()
        
        print(f"Dataset cleaning completed. Final shape: {self.cleaned_data.shape}")
        return self.cleaned_data
    
    def get_cleaned_data(self) -> Optional[pd.DataFrame]:
        return self.cleaned_data
    
    def get_cleaning_stats(self) -> dict:
        "Get statistics about cleaning process"
        if self.cleaned_data is None:
            return {"error": "Dataset not cleaned yet"}
        
        original_count = len(self.original_data)
        cleaned_count = len(self.cleaned_data)
        removed_count = original_count - cleaned_count
        
        return {
            "original_tweets": original_count,
            "cleaned_tweets": cleaned_count,
            "removed_tweets": removed_count,
            "removal_percentage": round((removed_count / original_count) * 100, 2)
        } 
            
        