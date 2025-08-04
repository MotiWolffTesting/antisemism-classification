import json
import pandas as pd
from typing import Dict, Any
import os


class ReportBuilder:
    """Handles data processing and file operations for reports"""
    def __init__(self, results_dir: str = "results"):
        self.results_dir = results_dir
        self.ensure_results_dir()
        
    def ensure_results_dir(self) -> None:
        """Create results directory if not exists"""
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
            print(f"Created results directory: {self.results_dir}")
            
    def save_cleaned_data(self, cleaned_data: pd.DataFrame, filename: str = "tweets_dataset_cleaned.csv") -> str:
        """Save the cleaned data into a csv file"""
        filepath = os.path.join(self.results_dir, filename)
        
        try:
            cleaned_data.to_csv(filepath, index=False)
            print(f"Cleaned dataset saved to {filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving to file: {e}")
            raise
        
    def generate_json_report(self, analysis_results: Dict[str, Any], filename: str = "results.json") -> str:
        """Generate and save JSON report with all analysis results"""
        filepath = os.path.join(self.results_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(analysis_results, f, indent=4, ensure_ascii=False)
            
            print(f"JSON report saved to: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving JSON report: {e}")
            raise
        
    def validate_results_structure(self, results: Dict[str, Any]) -> bool:
        """Validate that the results structure matches needed format"""
        required_keys = [
            "total_tweets",
            "average_length", 
            "common_words",
            "longest_3_tweets",
            "uppercase_words"
        ]
        
        for k in required_keys:
            if k not in results:
                print(f"Missing required key: {k}")
                return False
        
        # Validate total_tweets structure
        total_tweets_keys = ["antisemitic", "non_antisemitic", "total"]
        for k in total_tweets_keys:
            if k not in results['total_tweets']:
                print(f"Missing required key: {k}")
                return False
            
        # Validate average_length structure
        avg_length_keys = ["antisemitic", "non_antisemitic", "total"]
        for k in avg_length_keys:
            if k not in results["average_length"]:
                print(f"Missing key in average_length: {k}")
                return False
        
        # Validate longest_3_tweets structure
        longest_keys = ["antisemitic", "non_antisemitic"]
        for key in longest_keys:
            if key not in results["longest_3_tweets"]:
                print(f"Missing key in longest_3_tweets: {key}")
                return False
            
        # Validate uppercase_words structure
        uppercase_keys = ["antisemitic", "non_antisemitic", "total"]
        for key in uppercase_keys:
            if key not in results["uppercase_words"]:
                print(f"Missing key in uppercase_words: {key}")
                return False
            
        print("Results structure validation passed")
        return True
    
    def build_report_files(self, analysis_results: Dict[str, Any], cleaned_data: pd.DataFrame) -> Dict[str, str]:
        """Build and save report files without displaying them"""
        # Validate results structure
        if not self.validate_results_structure(analysis_results):
            raise ValueError("Invalid results structure")
        
        # Save cleaned dataset
        csv_path = self.save_cleaned_data(cleaned_data)
        
        # Save JSON report
        json_path = self.generate_json_report(analysis_results)
        
        return {
            "cleaned_data_path": csv_path,
            "json_report_path": json_path
        } 
        