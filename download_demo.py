#!/usr/bin/env python3
"""
Simple demonstration script to download Instagram account media
Usage: python download_demo.py <account_username>
"""

import sys
import instaloader
from pathlib import Path

def download_account(username, output_dir="./downloads"):
    """
    Download all posts from an Instagram account
    
    Args:
        username: Instagram username (without @)
        output_dir: Directory to save downloads
    """
    print(f"\n{'='*60}")
    print(f"Downloading posts from: @{username}")
    print(f"{'='*60}\n")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize Instaloader
    L = instaloader.Instaloader(
        download_pictures=True,
        download_videos=True,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=True,  # Save JSON with metadata
        compress_json=False,
        post_metadata_txt_pattern='{caption}',  # Save caption in .txt file
        max_connection_attempts=3,
        dirname_pattern=str(output_path / "{target}")
    )
    
    try:
        # Get profile
        print(f"Fetching profile information...")
        profile = instaloader.Profile.from_username(L.context, username)
        
        print(f"✓ Profile found: {profile.full_name}")
        print(f"  Total posts: {profile.mediacount}")
        print(f"  Followers: {profile.followers}")
        print(f"\nStarting download...\n")
        
        # Download all posts
        post_count = 0
        for post in profile.get_posts():
            post_count += 1
            print(f"[{post_count}] Downloading {post.shortcode}...", end=" ")
            
            try:
                L.download_post(post, target=username)
                print("✓")
            except Exception as e:
                print(f"✗ Error: {e}")
        
        print(f"\n{'='*60}")
        print(f"✓ Download complete!")
        print(f"  Downloaded {post_count} posts")
        print(f"  Saved to: {output_path / username}")
        print(f"{'='*60}\n")
        
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"✗ Error: Profile '@{username}' does not exist")
        sys.exit(1)
    except instaloader.exceptions.ConnectionException as e:
        print(f"✗ Connection error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python download_demo.py <instagram_username>")
        print("Example: python download_demo.py teddavisdotorg")
        sys.exit(1)
    
    username = sys.argv[1]
    
    # Remove @ if user included it
    username = username.lstrip('@')
    
    # Optional: specify custom output directory
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./downloads"
    
    download_account(username, output_dir)

if __name__ == "__main__":
    main()