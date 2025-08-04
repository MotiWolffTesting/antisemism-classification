import re
from collections import Counter
from typing import List, Dict, Any
from data_loader import DataLoader


NOT_LOADED = "Data not loaded..."


class DataAnalyzer:
    """
    Main class for classifiying tweets with antisemitism context"
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
        antisemitism_count = len(self.data[self.data['biased'] == 1])
        non_antisemitism_count = len(self.data[self.data['biased'] == 0])
        unspecified_count = len(self.data[~self.data['biased'].isin([0,1])]) # Flipping True/False with ~ sign
        total_count = len(self.data)
        
        return {
            "antisemitism": antisemitism_count,
            "non-antisemitism": non_antisemitism_count,
            "unspesified": unspecified_count,
            "total": total_count
        }
        
    def calc_avg_len(self) -> Dict[str, float]:
        "Calculate average word count per tweet by category"
        if self.data is None:
            raise ValueError(NOT_LOADED)
        
        # Calculate word count for each tweet
        self.data['word_count'] = self.data['text'].str.split().str.len()
        
        # Calculate average by category
        antisemtisim_avg = self.data[self.data['biased'] == 1]['word_count'].mean()
        non_antisemtism_avg = self.data[self.data['biased'] == 0]['word_count'].mean()
        total_avg = self.data['word_count'].mean()
        
        return {
            "antisemitism": round(antisemtisim_avg, 1),
            "non-antisemitism": round(non_antisemtism_avg, 1),
            "total": round(total_avg, 1)
        }
        
    def find_longest_tweets(self) -> Dict[str, List[str]]:
        "Find 3 longest tweets by category"
        if self.data is None:
            raise ValueError(NOT_LOADED)
        
        # Calculate word count if not already done
        if 'word_count' not in self.data.columns:
            self.data['word_count'] = self.data['text'].str.split().str.len()
            
        # Get longest tweet for each category
        antesimitism_longest = self.data[self.data['biased'] == 1].nlargest(3, 'word_count')['text'].tolist()
        non_antesimitism_longest = self.data[self.data['biased'] == 0].nlargest(3, 'word_count')['text'].tolist()
        
        return {
            "antisemitism": antesimitism_longest,
            "non-antisemitism": non_antesimitism_longest
        }
        
    def get_common_words(self, top_n: int = 10) -> Dict[str, Dict[str, List]]:
        "Find most common words across all tweets by category"
        if self.data is None:
            raise ValueError(NOT_LOADED)
        
        # Combine all text and split into words
        all_text = ' '.join(self.data['text'].astype(str))
        words = re.findall(r'\b\w+\b', all_text.lower())
        
        # Count word frequencies
        word_counts = Counter(words)
        
        # Get top N most common words anfd count
        common_data = word_counts.most_common(top_n)
        common_words = [word for word, count in common_data]
        counts = [count for word, count in common_data]
        
        return {
           "total": {
            "words": common_words,
            "count": counts
            }
        }
        
    def count_uppercase_words(self) -> Dict[str, int]:
        "Count words in uppercase by category."
  
        if self.data is None:
            raise ValueError(NOT_LOADED)
        
        def count_uppercase_in_text(text):
            "Count all-uppercased words"
            words = text.split()
            return sum(1 for word in words if word.is_upper() and len(word) > 1)
        
        # Count upprcased words by category
        antesmitism_uppercase = self.data[self.data['biased'] == 1]['text'].apply(count_uppercase_in_text).sum()
        non_antesmitism_uppercase = self.data[self.data['biased'] == 0]['text'].apply(count_uppercase_in_text).sum()
        total_uppercase = self.data['text'].apply(count_uppercase_in_text).sum()
        
        return {
            "antisemitism": int(antesmitism_uppercase),
            "non-antisemitism": int(non_antesmitism_uppercase),
            "total": int(total_uppercase)
        }
        
    def run_full_analysis(self) -> Dict[str, Any]:
        "Run full analysis and get complete results"
        return {
            "total_tweets": self.analyze_distribution(),
            "average_length": self.calc_avg_len(),
            "common_words": self.get_common_words(),
            "longest_three_tweets": self.find_longest_tweets(),
            "uppercase_words": self.count_uppercase_words()
        }
        
        
    
    
        
        
        

