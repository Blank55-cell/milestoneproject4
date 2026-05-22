# RealEstateHub

RealEstateHub is the fourth milestone project I’m building.  
It’s a real‑estate listing site where users can browse properties, view details, save favourites, and pay booking fees using Stripe.  
The aim is to keep everything clean and simple while showing how Django, user accounts, and Stripe payments can work together.

---

# Quick Links

- [How to Copy and Run This Project on Your Own Computer](#how-to-copy-and-run-this-project-on-your-own-computer)
- [What This Site Is For](#what-this-site-is-for)
- [User Stories](#user-stories)
- [Tools (Work in Progress)](#tools-work-in-progress)
- [Who This Is For](#who-this-is-for)
- [Pages Used in This Project](#pages-used-in-this-project)
- [Features](#features)
- [Deployment](#deployment)
- [Manual Testing](#manual-testing)
- [External Code Attribution](#external-code-attribution)
- [Disclaimer](#disclaimer)

---

# What This Site Is For

The goal is to build a simple real‑estate platform where users can browse properties, save the ones they like, and pay booking fees securely.  
Nothing complicated — just a clean layout and a straightforward flow.

---

# How to Copy and Run This Project on Your Own Computer

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR-USERNAME/milestoneproject4.git
```

### 2. Go Into the Project Folder
```bash
cd milestoneproject4
```

### 3. Create a Virtual Environment
```bash
py -m venv venv
```

### 4. Activate It
```bash
venv\Scripts\activate
```

### 5. Install Requirements
```bash
pip install -r requirements.txt
```

### 6. Apply Migrations
```bash
py manage.py migrate
```

### 7. Run the Server
```bash
py manage.py runserver
```

### 8. Open the Site
```
http://127.0.0.1:8000
```

---

# User Stories

- As a user, I want to browse properties so I can see what’s available.  
- I want to click into a property to view more details.  
- I want to create an account so I can save properties I like.  
- I want to pay booking fees securely using Stripe.  
- I want a simple layout so I can move around the site easily.  
- I want to remove saved properties when I no longer need them.

---

# Tools (Work in Progress)

These are the tools and features I plan to build, based on what I used in Project 3:

- Property listing system  
- User favourites (similar to saved books in Project 3)  
- Search and filtering for properties  
- Stripe checkout for booking fees  
- Notes / extra info section for each property  
- Image gallery for property photos  
- Admin tools for adding and editing listings  

---

# Who This Is For

Anyone who wants a simple way to browse properties without dealing with cluttered layouts or confusing navigation.

---

# Pages Used in This Project

- **home.html** – Landing page with featured properties  
- **listings.html** – Shows all properties  
- **property_details.html** – Full details for a selected property  
- **account.html** – Login and registration  
- **checkout.html** – Stripe payment page  
- **success.html** – Payment confirmation  

---

# Features

### Current Features

- Clean, simple UI  
- Responsive layout  
- User login and registration  
- Property listings with images  
- Property details page  
- Stripe payments  
- Save/remove favourites  
- Search and filtering  

---

# Deployment

The project will be deployed on Railway once the core features are complete.

---

# Manual Testing

Manual testing will be added later once the main pages and Stripe flow are built.

---

# External Code Attribution

- Stripe documentation  
- Django documentation  

---

# Disclaimer

This is a student project and isn’t connected to any real estate companies or payment providers.
