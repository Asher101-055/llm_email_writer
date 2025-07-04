#!/usr/bin/env python3
"""
Convert HTML presentation to PDF with exact styling preserved using Playwright
"""

from playwright.sync_api import sync_playwright
import os
import time

def convert_html_to_pdf(html_file, output_file, slide_mode=False):
    """Convert HTML file to PDF while preserving all styling"""
    try:
        # Check if HTML file exists
        if not os.path.exists(html_file):
            print(f"Error: HTML file '{html_file}' not found!")
            return False
        
        print(f"Converting {html_file} to PDF...")
        
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # Get absolute path for the HTML file
            html_path = os.path.abspath(html_file)
            file_url = f"file:///{html_path.replace(os.sep, '/')}"
            
            # Navigate to the HTML file
            page.goto(file_url)
            
            # Wait for page to load completely
            page.wait_for_load_state("networkidle")
            time.sleep(2)  # Extra wait for animations/transitions
            
            if slide_mode:
                # For interactive presentation, capture all slides
                print("📸 Capturing interactive slides...")
                
                # Get total number of slides
                total_slides = page.locator('.slide').count()
                print(f"Found {total_slides} slides")
                
                # Set viewport for consistent sizing
                page.set_viewport_size({"width": 1920, "height": 1080})
                
                # Generate PDF with landscape orientation for better slide viewing
                page.pdf(
                    path=output_file,
                    format="A4",
                    landscape=True,
                    print_background=True,
                    margin={"top": "0.5in", "right": "0.5in", "bottom": "0.5in", "left": "0.5in"}
                )
            else:
                # For PDF-friendly version, normal PDF generation
                print("📄 Generating PDF-friendly version...")
                
                # Set viewport for consistent sizing
                page.set_viewport_size({"width": 1200, "height": 800})
                
                # Generate PDF
                page.pdf(
                    path=output_file,
                    format="A4",
                    print_background=True,
                    margin={"top": "0.5in", "right": "0.5in", "bottom": "0.5in", "left": "0.5in"}
                )
            
            browser.close()
        
        print(f"✅ Successfully created: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error converting to PDF: {e}")
        return False

def main():
    # Convert the interactive presentation
    interactive_html = "LLM_Email_Writer_Presentation_Clean.html"
    interactive_pdf = "LLM_Email_Writer_Presentation_Interactive.pdf"
    
    # Convert the PDF-friendly presentation  
    pdf_html = "LLM_Email_Writer_Presentation_PDF.html"
    pdf_output = "LLM_Email_Writer_Presentation.pdf"
    
    print("🔄 Starting HTML to PDF conversion...")
    print("=" * 50)
    
    # Convert both versions
    success1 = convert_html_to_pdf(interactive_html, interactive_pdf, slide_mode=True)
    success2 = convert_html_to_pdf(pdf_html, pdf_output)
    
    print("=" * 50)
    if success1 or success2:
        print("🎉 PDF conversion completed!")
        if success1:
            print(f"📄 Interactive version: {interactive_pdf}")
        if success2:
            print(f"📄 Print-friendly version: {pdf_output}")
    else:
        print("❌ PDF conversion failed!")

if __name__ == "__main__":
    main()
