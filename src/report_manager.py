import pandas as pd
from typing import Dict, Any
from report_builder import ReportBuilder
from report_displayer import ReportDisplayer


class ReportManager:
    """Handles building and displaying reports"""
    def __init__(self, results_dir: str = "results"):
        self.builder = ReportBuilder(results_dir)
        self.displayer = ReportDisplayer()
    
    def build_complete_report(self, analysis_results: Dict[str, Any], cleaned_data: pd.DataFrame, 
                            display_summary: bool = True, display_detailed: bool = False) -> Dict[str, str]:
        "Build complete report with files and optional display"
        # Build and save files
        file_paths = self.builder.build_report_files(analysis_results, cleaned_data)
        
        # Display reports if requested
        if display_detailed:
            self.displayer.print_detailed_report(analysis_results)
        elif display_summary:
            self.displayer.print_summary(analysis_results)
        
        return file_paths
    
    def build_files_only(self, analysis_results: Dict[str, Any], cleaned_data: pd.DataFrame) -> Dict[str, str]:
        "Build and save report files without any console output"
        return self.builder.build_report_files(analysis_results, cleaned_data)
    
    def display_only(self, analysis_results: Dict[str, Any], detailed: bool = False) -> None:
        "Display report to console only, without saving files"
        if detailed:
            self.displayer.print_detailed_report(analysis_results)
        else:
            self.displayer.print_summary(analysis_results)
