#!/usr/bin/env python3
"""
Demo Data Setup Script for WorldBuy Auction Platform

This script sets up sample data for demonstration purposes.
Run this after setting up a fresh database to populate it with sample auctions.

Usage:
    python setup_demo_data.py
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.append(str(project_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commerce.settings')
django.setup()

from auctions.models import User, AuctionListings

def create_demo_user():
    """Create a demo user for the sample listings"""
    if not User.objects.filter(username='demo_user').exists():
        user = User.objects.create_user(
            username='demo_user',
            email='demo@worldbuy.com',
            password='demo123'
        )
        print(f"✅ Created demo user: {user.username}")
        return user
    else:
        user = User.objects.get(username='demo_user')
        print(f"ℹ️  Demo user already exists: {user.username}")
        return user

def create_sample_listings(demo_user):
    """Create sample auction listings"""
    
    sample_listings = [
        {
            'title': 'Romance - Luis Miguel (CD)',
            'description': 'Used CD, original and in good state.',
            'starting_bid': 8.00,
            'image_url': 'https://m.media-amazon.com/images/I/81PkjLWFjTL._AC_SL1425_.jpg',
            'category': 'Music'
        },
        {
            'title': 'Yamaha P45 Piano',
            'description': 'New, 88 keys with appropriate weight.',
            'starting_bid': 500.00,
            'image_url': 'https://d1aeri3ty3izns.cloudfront.net/media/66/669798/1200/preview.jpg',
            'category': 'Musical Instruments'
        },
        {
            'title': 'Racing Club Jersey (L)',
            'description': 'L Size, used home kit from 2019.',
            'starting_bid': 20.00,
            'image_url': 'https://marcadegol.com/fotos/2023/03/review-camisetas-kappa-de-racing-club-2023-1.jpg',
            'category': 'Clothing'
        },
        {
            'title': 'Argentina 2006 World Cup (Home Kit)',
            'description': 'Size XS, used but in perfect state!',
            'starting_bid': 24.00,
            'image_url': 'https://i0.wp.com/bestretrojerseys.com/wp-content/uploads/2023/03/a_09-3-scaled.webp',
            'category': 'Clothing'
        },
        {
            'title': 'Crime and Punishment - Dostoevsky',
            'description': 'Limited Edition from 1995.',
            'starting_bid': 14.00,
            'image_url': 'https://cdn.kobo.com/book-images/b1c96137-0ddf-4ee4-8f46-73bdfa9b8621/1200/1200/False/crime-and-punishment-by-fyodor-dostoevsky-1.jpg',
            'category': 'Books'
        },
        {
            'title': 'Golden Retriever Puppy',
            'description': 'Adorable and well-trained puppy looking for a loving home.',
            'starting_bid': 200.00,
            'image_url': 'https://usercontent2.hubstatic.com/5453351.jpg',
            'category': 'Animals'
        }
    ]
    
    created_count = 0
    for listing_data in sample_listings:
        if not AuctionListings.objects.filter(title=listing_data['title']).exists():
            listing = AuctionListings.objects.create(
                owner=demo_user,
                auction_active=True,
                **listing_data
            )
            print(f"✅ Created listing: {listing.title}")
            created_count += 1
        else:
            print(f"ℹ️  Listing already exists: {listing_data['title']}")
    
    print(f"\n🎉 Setup complete! Created {created_count} new sample listings.")
    return created_count

def main():
    """Main setup function"""
    print("🚀 Setting up demo data for WorldBuy Auction Platform\n")
    
    # Create demo user
    demo_user = create_demo_user()
    
    # Create sample listings
    created_count = create_sample_listings(demo_user)
    
    print(f"\n📊 Demo Data Summary:")
    print(f"   • Total users: {User.objects.count()}")
    print(f"   • Total listings: {AuctionListings.objects.count()}")
    print(f"   • Active listings: {AuctionListings.objects.filter(auction_active=True).count()}")
    
    print(f"\n🌐 You can now visit http://127.0.0.1:8000 to see the demo content!")
    print(f"📝 Demo user credentials:")
    print(f"   Username: demo_user")
    print(f"   Password: demo123")

if __name__ == '__main__':
    main()
