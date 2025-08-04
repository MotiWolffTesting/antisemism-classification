import pandas as pd
import re
from collections import Counter
from typing import List, Dict, Any
from data_loader import DataLoader


NOT_LOADED = "Data not loaded..."


class DataAnalyzer:
    """
    Main class for analyzing tweets with antisemitism context
    """
    def __init__(self, data_path: str):
        "Initiating analyzer"
        self.data_loader = DataLoader(data_path)
        self.data = self.data_loader.data
    
    def reload_data(self) -> None:
        """Reload data from the data loader"""
        self.data_loader.load_data()
        self.data = self.data_loader.data
        
    def analyze_distribution(self) -> Dict[str, int]:
        "Analyze distribution of tweets by category"
        if self.data is None:
            raise ValueError(NOT_LOADED)
        
        # Count tweet by category
        antisemitism_count = len(self.data[self.data['Biased'] == 1])
        non_antisemitism_count = len(self.data[self.data['Biased'] == 0])
        unspecified_count = len(self.data[~self.data['Biased'].isin([0,1])]) # Flipping True/False with ~ sign
        total_count = len(self.data)
        
        return {
            "antisemitic": antisemitism_count,
            "non_antisemitic": non_antisemitism_count,
            "unspecified": unspecified_count,
            "total": total_count
        }
        
    def calc_avg_len(self) -> Dict[str, float]:
        "Calculate average word count per tweet by category"
        if self.data is None:
            raise ValueError(NOT_LOADED)
        
        # Calculate word count for each tweet
        self.data['word_count'] = self.data['Text'].str.split().str.len()
        
        # Calculate average by category
        antisemitic_avg = self.data[self.data['Biased'] == 1]['word_count'].mean()
        non_antisemitic_avg = self.data[self.data['Biased'] == 0]['word_count'].mean()
        total_avg = self.data['word_count'].mean()
        
        return {
            "antisemitic": round(antisemitic_avg, 1),
            "non_antisemitic": round(non_antisemitic_avg, 1),
            "total": round(total_avg, 1)
        }
        
    def find_longest_tweets(self) -> Dict[str, List[str]]:
        "Find 3 longest tweets by category (based on character count)"
        if self.data is None:
            raise ValueError(NOT_LOADED)
        
        # Calculate character count if not already done
        if 'char_count' not in self.data.columns:
            self.data['char_count'] = self.data['Text'].str.len()
            
        # Get longest tweet for each category (by character count)
        antisemitism_longest = self.data[self.data['Biased'] == 1].nlargest(3, 'char_count')['Text'].tolist()
        non_antisemitism_longest = self.data[self.data['Biased'] == 0].nlargest(3, 'char_count')['Text'].tolist()
        
        return {
            "antisemitic": antisemitism_longest,
            "non_antisemitic": non_antisemitism_longest
        }
        
    def get_common_words(self, top_n: int = 10) -> Dict[str, List[str]]:
        "Find most common words across all tweets by category"
        if self.data is None:
            raise ValueError(NOT_LOADED)
        
        # Combine all text and split into words
        all_text = ' '.join(self.data['Text'].astype(str))
        words = re.findall(r'\b\w+\b', all_text.lower())
        
        # Count word frequencies
        word_counts = Counter(words)
        
        # Get top N most common words anfd count
        common_data = word_counts.most_common(top_n)
        common_words = [word for word, count in common_data]        
        return {
           "total": common_words
        }
        
    def count_uppercase_words(self) -> Dict[str, int]:
        "Count words in uppercase by category."
  
        if self.data is None:
            raise ValueError(NOT_LOADED)
        
        def count_uppercase_in_text(text):
            "Count all-uppercased words"
            words = text.split()
            return sum(1 for word in words if word.isupper() and len(word) > 1)
        
        # Count uppercase words by category
        antisemitic_uppercase = self.data[self.data['Biased'] == 1]['Text'].apply(count_uppercase_in_text).sum()
        non_antisemitic_uppercase = self.data[self.data['Biased'] == 0]['Text'].apply(count_uppercase_in_text).sum()
        total_uppercase = self.data['Text'].apply(count_uppercase_in_text).sum()
        
        return {
            "antisemitic": int(antisemitic_uppercase),
            "non_antisemitic": int(non_antisemitic_uppercase),
            "total": int(total_uppercase)
        }
        
    def run_full_analysis(self) -> Dict[str, Any]:
        "Run full analysis and get complete results"
        return {
            "total_tweets": self.analyze_distribution(),
            "average_length": self.calc_avg_len(),
            "common_words": self.get_common_words(),
            "longest_3_tweets": self.find_longest_tweets(),
            "uppercase_words": self.count_uppercase_words()
        }








