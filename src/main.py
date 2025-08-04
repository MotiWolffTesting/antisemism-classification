import sys
import os
from data_analyzer import DataAnalyzer
from text_cleaner import TextCleaner
from report_builder import ReportBuilder

def main():
    "Main function that handles project runtime"
    print("Antisemitism Classification Data Analysis")
    
    # Configuration
    data_path = "../data/tweets_dataset.csv"
    results_dir = "../results"
    
    cleaner = None
    try:
        # 1: Load and analyze original data
        print("\n1. Loading and analyzing original dataset...")
        analyzer = DataAnalyzer(data_path=data_path)
        
        # Run full analysis on original data
        original_analysis = analyzer.run_full_analysis()
        print("Original data analysis completed.")
        
        print("\n2. Cleaning dataset...")
        if analyzer.data is not None:
            cleaner = TextCleaner(analyzer.data)
            cleaned_data = cleaner.clean_dataset()
        else:
            print("Error: analyzer.data is None. Cannot clean dataset.")
            cleaned_data = None
            
        # Get cleaning statistics
        if cleaner is not None:
            cleaning_stats = cleaner.get_cleaning_stats()
            print(f"Dataset cleaning completed:")
            print(f"Original tweets: {cleaning_stats['original_tweets']}")
            print(f"Cleaned tweets: {cleaning_stats['cleaned_tweets']}")
            print(f"Removed tweets: {cleaning_stats['removed_tweets']} ({cleaning_stats['removal_percentage']}%)")
            
        # Step 3: Use original analysis results (not cleaned data)
        print("\n3. Using original analysis results...")
        # Use the original analysis, not cleaned data analysis
        analysis_results = original_analysis
        print("Original data analysis completed")
        
        # Step 4: Generate reports
        print("\n4. Generating reports...")
        report_builder = ReportBuilder(results_dir)
        
        # Build complete report using original analysis but cleaned data for CSV
        saved_files = report_builder.build_report_files(analysis_results, cleaned_data)
        
        print("\n" + "="*60)
        print("Analysis completed successfully!")
        print("="*60)
        print(f"Cleaned dataset saved to: {saved_files['cleaned_data_path']}")
        print(f"Analysis report saved to: {saved_files['json_report_path']}")
        print("="*60)
        
        return True
    except FileNotFoundError as e:
        print(f"Error: Could not find data file: {e}")
        return False
    except Exception as e:
        print(f"Error during analysis: {e}")
        return False
    
if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 