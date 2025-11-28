"""
Interactive REPL module for Scrapy shell development
Provides a dedicated environment for REPL-driven development of Scrapy spiders
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collector.settings')

import django
django.setup()

# Import Scrapy components
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.shell import Shell


def start_scrapy_repl(url=None, spider=None):
    """
    Start interactive Scrapy shell with project context
    
    Args:
        url (str): Optional URL to load in the shell
        spider (str): Optional spider name to use in the shell
    """
    # Get project settings
    settings = get_project_settings()
    
    # Create crawler process
    process = CrawlerProcess(settings)
    
    # Initialize shell
    shell = Shell(
        crawler_process=process,
        update_vars=None,
        code=None
    )
    
    # Start interactive shell
    if url:
        shell.onecmd(f'shell "{url}"')
    else:
        shell.cmdloop()


if __name__ == '__main__':
    # Example usage
    print("Starting Scrapy REPL environment...")
    print("Available objects: response, request, spider, crawler")
    print("Use 'fetch(url)' to load a URL, 'view(response)' to open in browser")
    print("-" * 50)
    
    start_scrapy_repl()