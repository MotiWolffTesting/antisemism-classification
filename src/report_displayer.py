from typing import Dict, Any


class ReportDisplayer:
    """Handles presentation and console output of analysis results"""
    def __init__(self):
        "Initialize the report displayer"
        pass
    
    def print_summary(self, results: Dict[str, Any]) -> None:
        "Print a formatted summary of the analysis results to console"
        print("Analysis Summary")
        print("="*50)
        
        # Tweet distribution
        total_tweets = results["total_tweets"]
        print(f"Total tweets analyzed: {total_tweets['total']}")
        print(f"Antisemitic tweets: {total_tweets['antisemitism']}")
        print(f"Non-antisemitic tweets: {total_tweets['non_antisemitism']}")
        if 'unspecified' in total_tweets:
            print(f"Unspecified tweets: {total_tweets['unspecified']}")
        
        # Average lengths
        avg_lengths = results["average_length"]
        print("\nAverage tweet lengths:")
        print(f"Antisemitic: {avg_lengths['antisemitism']} words")
        print(f"Non-antisemitic: {avg_lengths['non_antisemitism']} words")
        print(f"Overall: {avg_lengths['total']} words")
        
        # Common words
        common_words = results["common_words"]["total"]["words"]
        print(f"\nTop {len(common_words)} common words: {', '.join(common_words)}")
        
        # Uppercase words
        uppercase = results["uppercase_words"]
        print("\nUppercase words:")
        print(f"Antisemitic: {uppercase['antisemitism']}")
        print(f"Non-antisemitic: {uppercase['non_antisemitism']}")
        print(f"Total: {uppercase['total']}")
        
        print("="*50)
    
    def print_detailed_report(self, results: Dict[str, Any]) -> None:
        "Print a detailed report including longest tweets"
        self.print_summary(results)
        
        print("\nLONGEST TWEETS:")
        print("-" * 20)
        
        longest_tweets = results["longest_3_tweets"]
        
        print("\nAntisemitic (top 3):")
        antisemitic_tweets = longest_tweets["antisemitism"]
        for i in range(len(antisemitic_tweets)):
            tweet = antisemitic_tweets[i]
            if len(tweet) > 80:
                tweet = tweet[:80] + "..."
            print(f"{i+1}. {tweet}")
        
        print("\nNon-antisemitic (top 3):")
        non_antisemitic_tweets = longest_tweets["non-antisemitism"]
        for i in range(len(non_antisemitic_tweets)):
            tweet = non_antisemitic_tweets[i]
            if len(tweet) > 80:
                tweet = tweet[:80] + "..."
            print(f"{i+1}. {tweet}")
        
        print("="*50)
