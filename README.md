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

- home.html – Landing page with featured properties  
- listings.html – Shows all properties  
- property_details.html – Full details for a selected property  
- account.html – Login and registration  
- checkout.html – Stripe payment page  
- success.html – Payment confirmation  

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

# Deployment & Twelve-Factor Architecture

This project is hosted live on Railway and follows the Twelve-Factor App methodology (Factor III - Config) to keep configuration completely separate from the codebase.

Instead of hardcoding settings or exposing private keys in GitHub, the app shifts its behavior automatically depending on where it is running:

* **Local Development:** Uses a local `.env` file with `DEBUG=True` so Django can display detailed error screens during coding and testing.
* **Production (Railway):** Railway injects live environment variables directly into the hosting container. This forces `DEBUG=False` for security and tells WhiteNoise to safely serve the compiled static CSS and JavaScript files.

---

# Bugs and Troubleshooting Log

During development and deployment, several technical roadblocks emerged across different layers of the stack. Below is a structured breakdown of those issues and how they were resolved.

### Python / Django Bugs I Ran Into

| Bug ID | What Happened | Why It Happened | Fix |
|--------|----------------|------------------|------|
| P001 | Application kept running in debug mode on Railway | django-environ reads values as strings, so "False" was read as a truthy string instead of a boolean | Swapped the settings line to use explicit boolean casting: `DEBUG = env.bool('DEBUG', default=False)` |
| P002 | Railway app crashed at startup with `KeyError: 'BACKEND'` | The new Django 6 `STORAGES` dictionary was accidentally using the older `"ENGINE"` key syntax | Changed `"ENGINE"` to `"BACKEND"` inside the `STORAGES` dictionary settings |
| P003 | App crashed locally with `ModuleNotFoundError: No module named 'environ'` | Installed the library to use environment variables but forgot to freeze it into the project requirements | Ran `pip install django-environ` and pushed the updated `requirements.txt` file |
| P004 | Database changes didn't show up on the live server | Forgot to create or push tracking files for recent database schema changes | Ran `python manage.py makemigrations` and pushed the new migration files to GitHub |
| P005 | Received an `IndentationError` when trying to run the server | A quick edit inside `views.py` accidentally mixed tabs and spaces on a code line | Cleared the whitespace indentation and re-aligned the block using standard 4 spaces |
| P006 | Code check spacing warning | Only put one blank line between the new view functions | Added a second blank line to keep PEP8 guidelines happy |
| P007 | Trailing whitespace warnings | Left accidental spaces at the very end of code lines | Deleted the empty spaces at the ends of lines |
| P008 | Default post-login redirect loop | `LOGIN_REDIRECT_URL` wasn't declared, defaulting routing to a generic `/accounts/profile/` path | Appended `LOGIN_REDIRECT_URL = 'account_dashboard'` and `ACCOUNT_LOGOUT_REDIRECT_URL = 'home'` to `settings.py` |
| P009 | WhiteNoise static files deployment crash (500 Error) | Storage backend used `CompressedManifestStaticFilesStorage`, crashing over modified/missing assets | Updated staticfiles backend storage to use `"whitenoise.storage.CompressedStaticFilesStorage"` instead |
| P010 | Allauth system check configuration error | Mandatory email confirmation requires an explicit asterisk inside the signup fields array | Updated configuration array setting to parse cleanly using `ACCOUNT_SIGNUP_FIELDS = ['email*']` |
| P011 | Syntax error in `settings.py` configuration | A stray comma inside an array/tuple definition blocked Python from parsing the config blocks | Located the misplaced structural syntax token and removed it to clear the build blockages |
| P012 | Hardcoded API credentials security risk | The third-party RentCast API key was originally hardcoded directly into the production code file | Refactored integration to use `os.environ.get('RENTCAST_API_KEY', '')` and stored secrets securely in the local `.env` file |
| P013 | **Railway deployment log** threw a 401 Unauthorized API error during live testing | The recently added RentCast API key worked locally but was missing from the live production ecosystem | Added the `RENTCAST_API_KEY` key-value pair directly into the Railway Dashboard variables settings panel |

### CSS Bugs I Ran Into

| Bug ID | What Happened | Why It Happened | Fix |
|--------|----------------|------------------|------|
| C001 | Live site loaded as completely blank, unstyled text | Django 6 completely removed the old `STATICFILES_STORAGE` string fallback setting | Reconfigured `settings.py` to use the unified `STORAGES` dictionary block for WhiteNoise |
| C002 | MIME type / 404 static asset loading errors | Asset folders failed to resolve properly or mismatched mime headers during pipeline production loading | Adjusted `STATICFILES_DIRS` routes and verified proper middleware layer ordering for WhiteNoise execution |

### HTML Bugs I Ran Into

| Bug ID | What Happened | Why It Happened | Fix |
|--------|----------------|------------------|------|
| H001 | Property data fields weren't displaying on the template page | The variable name inside the HTML loop didn't match what the view function sent over | Matched the spelling inside the `{% for property in properties %}` loop to the view context |
| H002 | Details button did nothing when clicked | It was a standard `<button>` tag with no active link destination | Replaced it with an `<a href="...">` link tag styled to look like a button |
| H003 | Template missing error on render | Forgot to create the actual HTML template file or put it in the wrong directory | Created the missing template file inside the correct templates directory path |
| H004 | Unstyled Allauth authentication interfaces | Allauth automatically falls back to raw white screens on paths like `/accounts/login/` if unguided | Built a custom overridden `templates/account/` subfolder matching Allauth's naming rules extending `base.html` |
| H005 | RentCast API property data metrics (like square footage or property type) rendered completely blank | The JSON keys returned by the external RentCast payload dictionary were lowercase/snake_case, but the template variables mistakenly used Django model TitleCase syntax | Updated the HTML template variable keys (e.g. `{{ property.squareFootage }}` to `{{ property.squareFeet }}`) to mirror the precise JSON object strings returned by RentCast |

### JavaScript Bugs I Ran Into

| Bug ID | What Happened | Why It Happened | Fix |
|--------|----------------|------------------|------|
| J001 | **Browser DevTools Console** crashed with: `DOMException: Failed to execute 'querySelector' on 'Document': '#' is not a valid selector.` | Clicking an anchor tag with a dummy placeholder `href="#"` caused the smooth scroll script to execute `document.querySelector('#')`, which is an illegal CSS selector. | Refactored the event handler to verify if the attribute is strictly equal to `"#"` first, and safely skipped execution if true. |
| J002 | **No console error**, but the mobile navigation menu completely failed to toggle open on smaller mobile preview viewports. | The custom `$` shortcut helper relies on `document.querySelector`, which only returns the absolute first matching instance. The desktop and mobile menus shared similar classes, causing it to bind to the hidden desktop node instead. | Modified the script target selectors to use unique, explicit ID handles to guarantee precise layout node matching in the DOM. |
| J003 | **Browser Console** threw an unhandled type crash: `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')`. | The script file was linked inside the HTML `<head>` tag. The browser executed the JS engine before it finished parsing the body DOM, meaning elements like `menuBtn` returned `null`. | Appended the `defer` keyword property to the script element tracking tag, forcing it to wait until the browser finished loading the entire layout structure. |
| J004 | **VS Code side gutter** lit up with a bright red syntax error marker, and the file refused to execute in the browser. | A careless typing slip at the boundary edge of the smooth scroll `.forEach()` loop where a trailing closing bracket sequence `});` was accidentally deleted during a clean-up. | Tracked down the flagged red line inside VS Code's editor interface and restored the missing structural block syntax parameters. |
| J005 | **Browser Console** logged a rigid layout error: `Uncaught TypeError: Assignment to constant variable.` when toggling elements. | Attempted to change variable states by writing direct reassignments like `navLinks = document.querySelector(...)` after initializing the binding reference under a strict `const` modifier. | Maintained the immutable reference identifier and cleanly manipulated the object's properties using the correct API rule: `navLinks.classList.toggle('open')`. |
| J006 | **VS Code linter code view** highlighted a line with red squiggly warnings stating: `';' expected`. | A physical typing error where the period dot accessor token character was completely left out between the object handle name and its built-in sub-method (e.g., `navLinks classList.toggle`). | Located the structural gap flagged on the side panel of the editor and inserted the missing separation dot delimiter character. |
| J007 | **VS Code side gutter** displayed a fatal syntax dot warning layout stating: `Declaration or statement expected`, breaking all text color highlighting below it. | Accidentally omitted the assignment declaration equality character (`=`) when defining the global `$()` selector helper function array structure (e.g., typing `const $(selector) => ...`). | Corrected the initial arrow function assignment syntax block layout to read cleanly as: `const $ = (selector) => ...`. |
| J008 | **Browser Developer Tools** threw a broken compilation block: `Uncaught SyntaxError: Invalid or unexpected token`. | Copy-pasting code snippets from external cheat sheets introduced stylized smart/curly quotes (`“click”`) into the event listener argument string instead of raw development-safe straight quotes. | Audited the event handler line hooks inside the code workspace and re-typed all quote strings using standard straight quotes (`'click'`). |
| J009 | **VS Code side bar panel** threw a strict syntax warning outlining a missing bracket expression: `')' expected`. | Omitted the mandatory conditional tracking parenthesis markers wrapping around the `if` statement validation block (e.g., typing `if menuBtn { ... }`). | Encased the logic node verification argument cleanly inside standard structural parameters: `if (menuBtn) { ... }`. |
| J010 | **Browser Console** blocked script parsing with: `Uncaught SyntaxError: Malformed arrow function parameter list`. | Accidentally typed a single assignment equals token operator instead of the mandatory fat-arrow pointer layout component inside a callback sequence (e.g., typing `() = { ... }`). | Refactored the structural execution block sequence to match valid ECMAScript arrow mechanics: `() => { ... }`. |
| J011 | **No error thrown**, but the browser UI printed literal variable characters on screen (like `#{target}`) as plain un-evaluated text strings. | Attempted to execute dynamic template literal interpolation processing parameters while using basic single or double quotation marks instead of backticks. | Swapped out the basic outer quote delimiters with valid template literal backticks to let the browser interpret variables dynamically. |
| J012 | **VS Code side panel linter** flagged a parsing breakdown warning stating: `Expression expected`. | Accidental duplication of a trailing closing bracket character right inside a block conditional evaluation boundary (e.g., typing `if (menuBtn)) {`). | Cleared out the redundant structural punctuation token to clean up code alignment and allow continuous engine execution. |
| J013 | **Browser DevTools Console** logged a sudden reference crash: `Uncaught ReferenceError: checkoutbtn is not defined` when triggering a placeholder click event. | A simple spelling case-sensitivity mismatch occurred where the temporary button element was cached in camelCase (`checkoutBtn`) but written in lowercase characters (`checkoutbtn`) inside the fallback script logic. | Adjusted character casing states across all script functions to maintain strict uniform naming compatibility. |
| J014 | **Browser Console** threw an execution crash alert: `Uncaught SyntaxError: Identifier 'menuBtn' has already been declared`. | Redundant initialization loops occurred because identical naming blocks were explicitly declared multiple times across interconnected script modules using the strict `const` modifier. | Cleaned out the duplicated asset tracking instances to preserve a singular, clean block scoping layout pattern across the app workspace. |
| J015 | Script execution collapsed at startup with a trailing broken branch statement: `Uncaught SyntaxError: Unexpected token 'else'`. | Placed an accidental early-terminating semicolon punctuation token directly at the conclusion of an evaluation block path (e.g., writing `if (menuBtn); { ... } else { ... }`). | Deleted the rogue semicolon delimiter character to successfully reconnect the logical check block back to its execution branches. |
| J016 | **Browser Console** threw a selector query rejection: `DOMException: Failed to execute 'querySelectorAll' on 'Document': 'a[href^="#"' is not a valid selector.` | Missed the closing square bracket structural parameter when defining a complex CSS attribute filter array sequence within the anchor tag lookup query. | Appended the missing closing structural tracking square bracket token to normalize the selector rules perfectly: `'a[href^="#"]'`. |

### SQL / Database Bugs I Ran Into

| Bug ID | What Happened | Why It Happened | Fix |
|--------|----------------|------------------|------|
| S001 | Work in Progress | Database schema and connection logs will be tracked here once established | N/A |

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