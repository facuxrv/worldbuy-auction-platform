# Demo Data Setup Guide

This guide explains how to set up the sample data for the WorldBuy auction platform.

## 🎯 Quick Setup (Recommended)

The easiest way to get demo data is using the automated setup script:

```bash
python setup_demo_data.py
```

This will create:
- A demo user account (`demo_user` / `demo123`)
- 6 sample auction listings across different categories
- All listings will be active and ready for bidding

## 🔧 Manual Setup (Advanced)

If you prefer to load the exact data from the fixtures:

### 1. Load Sample Listings
```bash
python manage.py loaddata fixtures/sample_data.json
```

### 2. Load User Data (Optional)
```bash
python manage.py loaddata fixtures/users_data.json
```

**Note**: The fixtures contain the original data but may have user ID dependencies.

## 📊 Sample Data Overview

### Categories Included:
- **Music**: CDs and albums
- **Musical Instruments**: Pianos and equipment
- **Clothing**: Sports jerseys and apparel
- **Books**: Classic literature
- **Animals**: Pets looking for homes

### Sample Listings:
1. **Romance - Luis Miguel (CD)** - $8.00
2. **Yamaha P45 Piano** - $500.00
3. **Racing Club Jersey (L)** - $20.00
4. **Argentina 2006 World Cup Kit** - $24.00
5. **Crime and Punishment - Dostoevsky** - $14.00
6. **Golden Retriever Puppy** - $200.00

## 🚀 Using Demo Data

After setting up demo data, you can:

1. **Browse Listings**: Visit the home page to see all active auctions
2. **Test Bidding**: Create additional users and place bids
3. **Explore Categories**: Filter listings by category
4. **Add to Watchlist**: Save interesting items
5. **Leave Comments**: Interact with the community

## 🔄 Resetting Demo Data

To reset and recreate the demo data:

```bash
# Remove existing data
python manage.py flush --noinput

# Run migrations
python manage.py migrate

# Set up demo data again
python setup_demo_data.py
```

## 📝 Customizing Demo Data

You can modify `setup_demo_data.py` to:
- Add more sample listings
- Change categories
- Modify starting prices
- Add different images
- Create additional demo users

The script is designed to be reusable and won't create duplicates.

---

