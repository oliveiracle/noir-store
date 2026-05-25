# NOIR Store — Testing Documentation

## Table of Contents

1. [Manual Testing — User Stories](#1-manual-testing--user-stories)
2. [Automated Testing](#2-automated-testing)
3. [Validator Testing](#3-validator-testing)
4. [Browser Testing](#4-browser-testing)
5. [Responsiveness Testing](#5-responsiveness-testing)
6. [Accessibility Testing](#6-accessibility-testing)
7. [Bugs Found & Fixed](#7-bugs-found--fixed)
8. [Known Issues](#8-known-issues)

---

## 1. Manual Testing — User Stories

All 30 user stories were tested manually by navigating the deployed site and the local development server. Test results are recorded below.

---

### US01 — Browse all products

| Field | Detail |
|-------|--------|
| **User Story** | As a visitor, I can browse all products so I can explore the collection |
| **Steps Taken** | 1. Navigate to `/products/`. 2. Scroll through the products page. 3. Verify all products are visible grouped by category. |
| **Expected Result** | All products displayed on the page, grouped by category with names, images and prices. |
| **Actual Result** | Products displayed correctly, grouped by category (Jackets, Trousers, Shirts, T-Shirts, Accessories). |
| **Pass/Fail** | Pass |

---

### US02 — Filter products by category

| Field | Detail |
|-------|--------|
| **User Story** | As a visitor, I can filter products by category so I can find what I'm looking for |
| **Steps Taken** | 1. Navigate to `/products/`. 2. Click a category link in the sidebar (e.g. "Jackets"). 3. Verify only products in that category are shown. |
| **Expected Result** | Only products belonging to the selected category are displayed. |
| **Actual Result** | Filtering by category correctly returns only matching products. URL updates to `?category=jackets`. |
| **Pass/Fail** | Pass |

---

### US03 — Search products

| Field | Detail |
|-------|--------|
| **User Story** | As a visitor, I can search for products by name or description |
| **Steps Taken** | 1. Enter a search term (e.g. "linen") in the navbar search bar. 2. Press Enter. 3. Verify results match the query. 4. Test with a term found only in a description. |
| **Expected Result** | Products whose name or description contains the search term are returned. |
| **Actual Result** | Search returns correct results. Tested with "linen" (found in name), "versatile" (found in description). Both work correctly. |
| **Pass/Fail** | Pass |

---

### US04 — Product detail page

| Field | Detail |
|-------|--------|
| **User Story** | As a visitor, I can view a product detail page with image, price and description |
| **Steps Taken** | 1. Click on any product from the products page. 2. Verify the product detail page loads with image, name, price, description, and rating. |
| **Expected Result** | Full product detail shown including image, price, description, rating and add-to-bag button. |
| **Actual Result** | Product detail page renders all fields correctly. NEW badge shown on new arrivals. Size selector present where applicable. |
| **Pass/Fail** | Pass |

---

### US05 — Add product to shopping bag

| Field | Detail |
|-------|--------|
| **User Story** | As a visitor, I can add a product to my shopping bag |
| **Steps Taken** | 1. Navigate to a product detail page. 2. Set quantity to 2. 3. Click "ADD TO BAG". 4. Verify a success toast appears and the bag count in the navbar updates. |
| **Expected Result** | Product added to bag, success toast displayed, bag icon count increases. |
| **Actual Result** | Product added correctly. Toast shows the product name. Bag count updates from 0 to 2. |
| **Pass/Fail** | Pass |

---

### US06 — View shopping bag

| Field | Detail |
|-------|--------|
| **User Story** | As a visitor, I can view my shopping bag with items and totals |
| **Steps Taken** | 1. Add one or more products to the bag. 2. Navigate to `/bag/`. 3. Verify all items are listed with name, quantity, unit price, subtotal and grand total. |
| **Expected Result** | Bag page shows all added items, subtotals, delivery cost and grand total. |
| **Actual Result** | Bag page displays all line items correctly. Delivery threshold logic works (free delivery over £50, otherwise 10% charge displayed). |
| **Pass/Fail** | Pass |

---

### US07 — Update or remove bag items

| Field | Detail |
|-------|--------|
| **User Story** | As a visitor, I can update or remove items from my bag |
| **Steps Taken** | 1. Go to `/bag/`. 2. Change the quantity of an item and click Update. 3. Verify the quantity and total update. 4. Click Remove on an item. 5. Verify the item is gone. |
| **Expected Result** | Quantity updates correctly; removed items disappear from the bag. |
| **Actual Result** | Update and Remove both work. If all items are removed, the empty bag message is shown with a link to continue shopping. |
| **Pass/Fail** | Pass |

---

### US08 — Complete a purchase using Stripe

| Field | Detail |
|-------|--------|
| **User Story** | As a visitor, I can complete a purchase using Stripe |
| **Steps Taken** | 1. Add a product to the bag. 2. Proceed to checkout. 3. Fill in delivery details. 4. Enter test card `4242 4242 4242 4242` with any future date and CVC. 5. Submit the form. |
| **Expected Result** | Payment processed successfully, redirected to order confirmation page. |
| **Actual Result** | Stripe PaymentIntent created correctly. Card input validates in real time. Order saved to database on successful payment. |
| **Pass/Fail** | Pass |

---

### US09 — Order confirmation page

| Field | Detail |
|-------|--------|
| **User Story** | As a visitor, I can receive an order confirmation page |
| **Steps Taken** | 1. Complete checkout with test card. 2. Observe the page redirected to after payment. 3. Verify order number, line items and delivery details are shown. |
| **Expected Result** | Confirmation page shows order number, all purchased items, delivery address and total. |
| **Actual Result** | `/checkout/success/<order_number>/` renders correctly with all order details. Order number is a unique UUID-based string. |
| **Pass/Fail** | Pass |

---

### US10 — Order confirmation email

| Field | Detail |
|-------|--------|
| **User Story** | As a visitor, I can receive an order confirmation email |
| **Steps Taken** | 1. Complete checkout. 2. Check the email address entered in the form. 3. Verify a confirmation email is received with order details. |
| **Expected Result** | Email sent to customer's address confirming the order number and items. |
| **Actual Result** | `send_confirmation_email()` called on the success view. Email subject and body rendered from templates. Email received successfully in testing. |
| **Pass/Fail** | Pass |

---

### US11 — Register for an account

| Field | Detail |
|-------|--------|
| **User Story** | As a visitor, I can register for an account |
| **Steps Taken** | 1. Click "Account" in the navbar and select "Register". 2. Fill in username, email and password. 3. Submit the form. 4. Verify email confirmation is sent (if configured) or account is created. |
| **Expected Result** | Account created successfully, user redirected and logged in. |
| **Actual Result** | django-allauth handles registration. User created in the database. Verification email sent in production. |
| **Pass/Fail** | Pass |

---

### US12 — Sign in and out

| Field | Detail |
|-------|--------|
| **User Story** | As a registered user, I can sign in and out |
| **Steps Taken** | 1. Click "Account → Sign In". 2. Enter credentials. 3. Verify redirect to homepage. 4. Click "Account → Sign Out". 5. Confirm the sign-out confirmation page, then confirm logged out. |
| **Expected Result** | User can sign in and out with toast messages confirming both actions. |
| **Actual Result** | Sign in and sign out work correctly. Account dropdown changes from "Register / Sign In" to the user's name and "Sign Out". |
| **Pass/Fail** | Pass |

---

### US13 — Reset password

| Field | Detail |
|-------|--------|
| **User Story** | As a registered user, I can reset my password |
| **Steps Taken** | 1. Click "Sign In → Forgot Password". 2. Enter registered email address. 3. Submit. 4. Check email for reset link. 5. Follow link and set new password. |
| **Expected Result** | Password reset email received, new password accepted on login. |
| **Actual Result** | allauth password reset flow works end-to-end. Reset email contains a one-time link. |
| **Pass/Fail** | Pass |

---

### US14 — Save default delivery info

| Field | Detail |
|-------|--------|
| **User Story** | As a registered user, I can save my default delivery info |
| **Steps Taken** | 1. Sign in and go to `/profile/`. 2. Fill in the delivery form (phone, address, postcode, country). 3. Save. 4. Navigate to checkout. 5. Verify the form is pre-filled with saved data. |
| **Expected Result** | Saved delivery info pre-populates the checkout form on the next visit. |
| **Actual Result** | Profile saved correctly. Checkout view reads `request.user.profile` and passes fields as form initial values. |
| **Pass/Fail** | Pass |

---

### US15 — View order history

| Field | Detail |
|-------|--------|
| **User Story** | As a registered user, I can view my order history |
| **Steps Taken** | 1. Sign in. 2. Go to `/profile/`. 3. Scroll to the order history section. 4. Verify past orders are listed with order number, date and total. |
| **Expected Result** | All past orders linked to the user's email are shown on the profile page. |
| **Actual Result** | Orders queried by `email=request.user.email`, sorted by `-date`. Each order links to its confirmation detail page. |
| **Pass/Fail** | Pass |

---

### US16 — Admin: add new products

| Field | Detail |
|-------|--------|
| **User Story** | As an admin, I can add new products via the frontend |
| **Steps Taken** | 1. Sign in as superuser. 2. Navigate to `/products/add/`. 3. Fill in all product fields and upload an image. 4. Submit. 5. Verify product appears in the store. |
| **Expected Result** | New product created and visible in the product list. |
| **Actual Result** | `add_product` view restricted to superusers. Product form validates and saves correctly including the image upload via Pillow. |
| **Pass/Fail** | Pass |

---

### US17 — Admin: edit products

| Field | Detail |
|-------|--------|
| **User Story** | As an admin, I can edit existing products |
| **Steps Taken** | 1. Sign in as superuser. 2. Navigate to any product detail page. 3. Click the "Edit" link. 4. Modify the name and price. 5. Submit and verify the changes are saved. |
| **Expected Result** | Product fields updated and reflected on the product page. |
| **Actual Result** | `edit_product` view pre-fills the form via `instance=product`. Updates persist to the database correctly. |
| **Pass/Fail** | Pass |

---

### US18 — Admin: delete products

| Field | Detail |
|-------|--------|
| **User Story** | As an admin, I can delete products |
| **Steps Taken** | 1. Sign in as superuser. 2. On a product detail page, click "Delete". 3. Confirm deletion. 4. Verify the product no longer appears in the store. |
| **Expected Result** | Product removed from the database and the product list. |
| **Actual Result** | `delete_product` view restricted to superusers. Product deleted on POST. Redirects to `/products/` with a success toast. |
| **Pass/Fail** | Pass |

---

### US19 — Newsletter sign-up

| Field | Detail |
|-------|--------|
| **User Story** | As a visitor, I can sign up for the newsletter |
| **Steps Taken** | 1. Scroll to the footer on any page. 2. Enter an email address in the newsletter field. 3. Submit. 4. Verify a success toast appears. 5. Enter the same email again. 6. Verify a duplicate message appears. |
| **Expected Result** | First submission stores the email and shows success. Repeat submission shows "already subscribed". |
| **Actual Result** | `get_or_create` handles both cases correctly. `NewsletterSubscriber` record created on first signup. |
| **Pass/Fail** | Pass |

---

### US20 — Leave a product review

| Field | Detail |
|-------|--------|
| **User Story** | As a registered user, I can leave a review on a product |
| **Steps Taken** | 1. Sign in. 2. Navigate to a product detail page. 3. Scroll to the reviews section. 4. Select a star rating and write a comment. 5. Submit the review form. 6. Verify the review appears below the product. |
| **Expected Result** | Review saved and displayed on the product page with the rating and comment. |
| **Actual Result** | `add_review` view creates a `Review` object linked to the product and user. Review appears immediately after redirect. |
| **Pass/Fail** | Pass |

---

### US21 — Edit or delete own review

| Field | Detail |
|-------|--------|
| **User Story** | As a registered user, I can edit or delete my own review |
| **Steps Taken** | 1. Sign in as the user who left a review. 2. On the product page, click "Edit" on the review. 3. Change the rating and comment. 4. Submit and verify the update. 5. Click "Delete" and confirm the review is removed. |
| **Expected Result** | Review updated or deleted; other users' reviews remain unaffected. |
| **Actual Result** | `edit_review` and `delete_review` views both filter by `user=request.user`, preventing editing of others' reviews. Both actions work correctly. |
| **Pass/Fail** | Pass |

---

### US22 — Wishlist

| Field | Detail |
|-------|--------|
| **User Story** | As a registered user, I can add products to a wishlist |
| **Steps Taken** | 1. Sign in. 2. Navigate to a product detail page. 3. Click "ADD TO WISHLIST". 4. Verify a success toast appears. 5. Go to `/profile/` and verify the product appears in the wishlist section. 6. Click the button again to remove it. |
| **Expected Result** | Product toggled in and out of the wishlist. Profile page shows current wishlist contents. |
| **Actual Result** | `toggle_wishlist` view handles add and remove correctly using `wishlist.products.add()` and `.remove()`. |
| **Pass/Fail** | Pass |

---

### US23 — NOIR Assistant chat widget

| Field | Detail |
|-------|--------|
| **User Story** | As a visitor, I can use the NOIR Assistant chat widget |
| **Steps Taken** | 1. Navigate to any page. 2. Click the chat icon in the bottom-right corner. 3. Type "shipping" and submit. 4. Verify a relevant response appears. 5. Type a product name and verify a product result is returned. 6. Close the widget. |
| **Expected Result** | Chat widget opens and closes, responds to keyword queries, and can find products by name. |
| **Actual Result** | Widget opens with a smooth animation. Keyword engine matches "shipping", "returns", "sizing", "payment". Product search fallback finds matching products. |
| **Pass/Fail** | Pass |

---

### US24 — About page

| Field | Detail |
|-------|--------|
| **User Story** | As a visitor, I can view the About page with brand story |
| **Steps Taken** | 1. Navigate to `/about/`. 2. Observe the typewriter animation loading (on desktop). 3. Read through the four brand chapter sections. |
| **Expected Result** | About page loads with animated typewriter text on desktop and static text on mobile. |
| **Actual Result** | Typewriter animation triggers correctly on desktop. Mobile version shows all text statically. Optional keyboard sound effect toggleable. |
| **Pass/Fail** | Pass |

---

### US25 — Facebook Business Page evidence

| Field | Detail |
|-------|--------|
| **User Story** | As a visitor, I can see NOIR's Facebook Business Page evidence |
| **Steps Taken** | 1. Navigate to `/facebook/`. 2. Verify Facebook Business Page screenshots are visible. |
| **Expected Result** | Page shows screenshots of the NOIR Facebook Business Page with page name, bio and category. |
| **Actual Result** | `/facebook/` renders the `facebook_mockup.html` template with the two screenshots correctly displayed. |
| **Pass/Fail** | Pass |

---

### US26 — Information pages (FAQ, Shipping, Returns)

| Field | Detail |
|-------|--------|
| **User Story** | As a visitor, I can view FAQ, Shipping and Returns pages |
| **Steps Taken** | 1. Navigate to `/faq/`. 2. Verify questions and answers are displayed. 3. Navigate to `/shipping/`. 4. Verify shipping policy content. 5. Navigate to `/returns/`. 6. Verify returns policy content. |
| **Expected Result** | All three information pages render their content correctly. |
| **Actual Result** | All three views render the correct templates. Content is well-structured with appropriate headings. |
| **Pass/Fail** | Pass |

---

### US27 — Contact page

| Field | Detail |
|-------|--------|
| **User Story** | As a visitor, I can contact the store via the Contact page |
| **Steps Taken** | 1. Navigate to `/contact/`. 2. Fill in the name, email and message fields. 3. Submit the form. 4. Verify a confirmation message appears. 5. Observe the Google Maps embed on the page. |
| **Expected Result** | Contact form accepts submission and shows a confirmation. Map embed loads correctly. |
| **Actual Result** | Form submission sets `message_sent=True` and the template renders a thank you message. Google Maps embed loads via iframe. |
| **Pass/Fail** | Pass |

---

### US28 — Deployed to Heroku

| Field | Detail |
|-------|--------|
| **User Story** | As a developer, I have deployed the site to Heroku |
| **Steps Taken** | 1. Open the live Heroku URL. 2. Navigate through all main pages. 3. Complete a test purchase using a Stripe test card. 4. Verify all features work identically to the local environment. |
| **Expected Result** | Site fully functional on Heroku with production database and environment variables. |
| **Actual Result** | Site deployed and accessible. `DEBUG=False` in production. PostgreSQL database connected. All pages load correctly. |
| **Pass/Fail** | Pass |

---

### US29 — AWS S3 for static and media files

| Field | Detail |
|-------|--------|
| **User Story** | As a developer, I have set up AWS S3 for static and media files |
| **Steps Taken** | 1. Open the live site. 2. Inspect a product image URL in the browser dev tools. 3. Verify the URL points to an S3 bucket. 4. Check CSS and JS asset URLs. |
| **Expected Result** | All static files and media files served from AWS S3 in production. |
| **Actual Result** | Image URLs follow the pattern `https://<bucket>.s3.<region>.amazonaws.com/...`. CSS and JS assets similarly served from S3 via boto3/django-storages. |
| **Pass/Fail** | Pass |

---

### US30 — Full README

| Field | Detail |
|-------|--------|
| **User Story** | As a developer, I have written a full README |
| **Steps Taken** | 1. Open `README.md` at the project root. 2. Verify all required sections are present. |
| **Expected Result** | README covers project overview, UX design, user stories, features, database design, deployment and credits. |
| **Actual Result** | README contains all sections including wireframes, ERD, colour palette, typography, marketing strategy, and full deployment instructions. |
| **Pass/Fail** | Pass |

---

## 2. Automated Testing

Automated tests were written using Django's built-in `TestCase` framework across three apps: `products`, `bag` and `home`. Tests cover models, views, authentication guards and business logic.

### Running the tests

```bash
python manage.py test products bag home
```

### Test results

```
Ran 34 tests in 6.3s
OK
```

All 34 tests pass.

### Test coverage by app

#### products (17 tests)

| Test Class | Test | Description |
|------------|------|-------------|
| `CategoryModelTest` | `test_str_returns_name` | `__str__` returns the internal category name |
| `CategoryModelTest` | `test_get_friendly_name` | `get_friendly_name()` returns the display name |
| `ProductModelTest` | `test_str_returns_name` | `__str__` returns the product name |
| `ProductModelTest` | `test_is_new_default_false` | `is_new` defaults to `False` on new products |
| `ProductModelTest` | `test_category_optional` | Products can be created without a category |
| `ProductViewTest` | `test_all_products_page_loads` | `/products/` returns 200 with correct template |
| `ProductViewTest` | `test_product_detail_page_loads` | Product detail page returns 200 |
| `ProductViewTest` | `test_product_detail_404_for_invalid_id` | Invalid product ID returns 404 |
| `ProductViewTest` | `test_search_returns_matching_product` | Search query returns matching products |
| `ProductViewTest` | `test_search_returns_no_results_for_unknown_term` | Unknown search term shows "NO PRODUCTS FOUND" |
| `ProductViewTest` | `test_category_filter` | Category filter returns only matching products |
| `ReviewModelTest` | `test_str_format` | Review `__str__` includes username and product name |
| `ReviewModelTest` | `test_review_linked_to_product` | Review foreign key links to correct product |
| `AdminProductViewTest` | `test_add_product_requires_login` | Unauthenticated users are redirected to login |
| `AdminProductViewTest` | `test_non_superuser_cannot_add_product` | Regular users redirected away from add product |
| `AdminProductViewTest` | `test_superuser_can_access_add_product` | Superusers can access the add product form |
| `AdminProductViewTest` | `test_superuser_can_delete_product` | Superusers can delete a product from the database |

#### bag (7 tests)

| Test Class | Test | Description |
|------------|------|-------------|
| `BagViewTest` | `test_bag_page_loads` | `/bag/` returns 200 with correct template |
| `BagViewTest` | `test_add_to_bag` | Adding a product stores it in the session |
| `BagViewTest` | `test_add_to_bag_increases_quantity` | Adding the same product again increments quantity |
| `BagViewTest` | `test_remove_from_bag` | Removing a product clears it from the session |
| `BagViewTest` | `test_update_bag_quantity` | Updating quantity changes the session value |
| `BagViewTest` | `test_update_bag_with_zero_removes_item` | Setting quantity to 0 removes the item |
| `BagViewTest` | `test_add_to_bag_rejects_open_redirect` | External redirect URLs are rejected for security |

#### home (10 tests)

| Test Class | Test | Description |
|------------|------|-------------|
| `HomeViewTest` | `test_homepage_loads` | Homepage returns 200 with correct template |
| `HomeViewTest` | `test_homepage_shows_new_products` | Products marked `is_new=True` appear on the homepage |
| `HomeViewTest` | `test_faq_page_loads` | FAQ page returns 200 |
| `HomeViewTest` | `test_shipping_page_loads` | Shipping page returns 200 |
| `HomeViewTest` | `test_returns_page_loads` | Returns page returns 200 |
| `HomeViewTest` | `test_contact_page_loads` | Contact page returns 200 |
| `HomeViewTest` | `test_contact_form_submission` | POST to contact shows confirmation message |
| `HomeViewTest` | `test_about_page_loads` | About page returns 200 |
| `NewsletterTest` | `test_newsletter_signup_creates_subscriber` | New email creates a `NewsletterSubscriber` record |
| `NewsletterTest` | `test_newsletter_duplicate_does_not_create_second_record` | Duplicate email does not create a second record |

---

## 3. Validator Testing

### HTML — W3C Markup Validation Service

Each HTML template was tested by copying the rendered page source from the browser into the [W3C Validator](https://validator.w3.org/nu/).

| Page | Result | Notes |
|------|--------|-------|
| Homepage (`/`) | Pass | No errors or warnings |
| Products (`/products/`) | Pass | No errors or warnings |
| Product Detail (`/products/<id>/`) | Pass | No errors or warnings |
| Shopping Bag (`/bag/`) | Pass | No errors or warnings |
| Checkout (`/checkout/`) | Pass | No errors or warnings |
| Checkout Success | Pass | No errors or warnings |
| Profile (`/profile/`) | Pass | No errors or warnings |
| About (`/about/`) | Pass | No errors or warnings |
| Contact (`/contact/`) | Pass | No errors or warnings |
| FAQ (`/faq/`) | Pass | No errors or warnings |
| Shipping (`/shipping/`) | Pass | No errors or warnings |
| Returns (`/returns/`) | Pass | No errors or warnings |
| Sign In | Pass | No errors or warnings |
| Register | Pass | No errors or warnings |
| 404 page | Pass | No errors or warnings |

> **Note:** Django template tags (`{% %}`, `{{ }}`) are not passed to the validator — the rendered HTML output was tested each time.

---

### CSS — W3C CSS Validation Service

The main stylesheet and any additional CSS files were tested via [W3C Jigsaw Validator](https://jigsaw.w3.org/css-validator/).

| File | Result | Notes |
|------|--------|-------|
| `static/css/base.css` | Pass | No errors |
| `static/css/checkout.css` | Pass | No errors |
| `static/css/products.css` | Pass | No errors |
| `static/css/profile.css` | Pass | No errors |
| `static/css/bag.css` | Pass | No errors |

> **Note:** Vendor-prefixed properties (e.g. `-webkit-`) generate warnings in the validator but are not errors. These warnings were reviewed and deemed acceptable as they are required for cross-browser compatibility.

---

### JavaScript — JSHint

All JavaScript files were tested using [JSHint](https://jshint.com/) with ES6 enabled via the `/* jshint esversion: 6 */` directive (also configured in `.jshintrc`).

| File | Result | Notes |
|------|--------|-------|
| `static/js/noir.js` | Pass | No errors. `requestAnimationFrame` is a browser global. |
| `static/js/checkout.js` | Pass | No errors. `Stripe` marked as global via `/* global Stripe */`. |
| `static/js/chat.js` | Pass | No errors. |
| `static/js/strip.js` | Pass | No errors. |
| `static/js/about.js` | Pass | No errors. |
| `static/js/bag.js` | Pass | No errors. |

---

### Python — PEP8 / flake8

All Python files were checked for PEP8 compliance using flake8 with `max-line-length=79`.

```
flake8 . --max-line-length=79 --exclude=.git,venv,migrations
```

| App | Result |
|-----|--------|
| `home/` | Pass — 0 errors |
| `products/` | Pass — 0 errors |
| `bag/` | Pass — 0 errors |
| `checkout/` | Pass — 0 errors |
| `profiles/` | Pass — 0 errors |
| `noir/` | Pass — 0 errors |

> **Note:** Auto-generated Django migration files were excluded from the check as they are not manually authored.

---

## 3. Browser Testing

The site was tested manually on the following browsers on both the local development server and the deployed Heroku instance.

| Browser | Version | Platform | Result | Notes |
|---------|---------|----------|--------|-------|
| Google Chrome | 145 | macOS | Pass | All features work correctly |
| Mozilla Firefox | 126 | macOS | Pass | Canvas animation, Stripe and all forms work |
| Apple Safari | 17 | macOS / iOS | Pass | Tested on desktop Safari and iPhone Safari |
| Microsoft Edge | 124 | Windows 11 | Pass | Chromium-based — identical to Chrome |
| Chrome for Android | 125 | Android 14 | Pass | Responsive layout adapts correctly |

---

## 4. Responsiveness Testing

The site was tested at the following viewport widths using Chrome DevTools and physical devices.

| Device / Viewport | Result | Notes |
|-------------------|--------|-------|
| iPhone SE (375px) | Pass | Navigation collapses to hamburger. Bag page stacks vertically. Checkout form full-width. |
| iPhone 14 Pro (393px) | Pass | Layout correct. Canvas hero scales. Chat widget accessible. |
| iPad Mini (768px) | Pass | Two-column product grid. Sidebar filter above products on tablet. |
| iPad Pro (1024px) | Pass | Full desktop layout kicks in. Navbar fully expanded. |
| Desktop 1280px | Pass | Standard desktop layout. All grids and columns display correctly. |
| Desktop 1920px | Pass | Layout max-width constrains content. No horizontal overflow. |

Key responsiveness checks:
- Navbar collapses to hamburger below 992px (Bootstrap lg breakpoint)
- Hero canvas scales correctly on all viewport widths
- Product grid switches from 4-column to 2-column to 1-column at appropriate breakpoints
- Shopping bag stacks to a single column on mobile
- Checkout form is full-width and usable on mobile
- About page disables the typewriter animation on mobile and shows static content instead

---

## 5. Accessibility Testing

| Test | Method | Result |
|------|--------|--------|
| Skip-to-content link | Keyboard Tab on page load | Pass — Link visible on focus, jumps to main content |
| Form labels | Manual inspection of rendered HTML | Pass — All inputs have associated `<label>` elements |
| Button aria-labels | Inspect icon-only buttons | Pass — All icon buttons have descriptive `aria-label` attributes |
| Decorative icons | Inspect Font Awesome icons | Pass — All decorative icons have `aria-hidden="true"` |
| Colour contrast | Chrome DevTools Accessibility Audit | Pass — All text meets WCAG AA contrast ratios (4.5:1 minimum) |
| Keyboard navigation | Tab through all interactive elements | Pass — All links, buttons and form fields reachable by keyboard |
| Screen reader | VoiceOver (macOS) on key pages | Pass — Page structure and interactive elements announced correctly |
| Dynamic content | `aria-live` regions on toasts | Pass — Toast messages announced to screen readers |

---

## 6. Bugs Found & Fixed

### Bug 1 — Bag session key type mismatch causing items to duplicate

**Description:** When a product was added to the bag from the product detail page, then added again from a different entry point, the item count doubled instead of incrementing. The root cause was that the session dictionary stored item IDs as integers in one code path and as strings in another, resulting in two separate keys for the same product (e.g. `1` and `"1"`).

**Fix:** All bag views were updated to cast `item_id` to `str()` consistently before reading or writing to the session dictionary. The `add_to_bag` view now always converts: `key = str(item_id)`.

**Files changed:** `bag/views.py`

---

### Bug 2 — Stripe webhook 400 error on order line item creation

**Description:** During testing of the Stripe webhook endpoint (used as a fallback if the browser closes before the redirect), the webhook handler was returning a 400 error. The webhook was receiving the `payment_intent.succeeded` event but failing to find the matching order, because the order had not yet been committed to the database when the webhook fired — a race condition.

**Fix:** Added a retry loop in the webhook handler with a short sleep between attempts (up to 5 retries over 5 seconds) to allow the checkout view time to complete writing the order before the webhook gives up. If the order is still not found after retries, the webhook creates the order itself from the PaymentIntent metadata.

**Files changed:** `checkout/webhook_handler.py`

---

### Bug 3 — Decimal precision error causing grand total mismatch

**Description:** When comparing the bag's grand total to the Stripe PaymentIntent amount during webhook processing, occasional mismatches of £0.01 were observed. The issue was caused by floating-point precision when multiplying the decimal total by 100 to convert to pence — e.g. `£29.99 × 100` produced `2998.9999...` which `round()` corrected to `2999` rather than the expected `3000` for a £30.00 item.

**Fix:** Changed the conversion to use Python's `Decimal` type with explicit quantisation throughout the checkout and bag context pipeline, ensuring that monetary values are always handled as `Decimal('29.99')` rather than `float(29.99)` before multiplication.

**Files changed:** `bag/contexts.py`, `checkout/views.py`

---

### Bug 4 — Newsletter toast not dismissing on mobile

**Description:** After subscribing to the newsletter, the success toast appeared correctly on desktop but did not auto-dismiss on mobile Safari. Users had to manually close it. The issue was that the Bootstrap toast auto-dismiss relied on a `setTimeout` that was being blocked by iOS Safari's aggressive background tab throttling when the page had just performed a redirect.

**Fix:** Added an explicit `addEventListener('shown.bs.toast', ...)` callback that re-triggers the auto-dismiss timer after the toast's shown event fires, ensuring the dismiss works regardless of the redirect timing. Tested on iOS Safari 17.

**Files changed:** `static/js/toasts.js`

---

### Bug 5 — Admin-only product links visible to anonymous users

**Description:** The Edit and Delete links on the product detail page were wrapped in `{% if request.user.is_superuser %}` in the template, but an anonymous user who knew the URL of `/products/edit/<id>/` could access the edit form directly — the view did not enforce the superuser check independently of the template.

**Fix:** Added an explicit `if not request.user.is_superuser` guard at the top of the `add_product`, `edit_product` and `delete_product` views in addition to the template-level check. Non-superusers are now redirected to `/products/` with an error toast if they attempt direct URL access.

**Files changed:** `products/views.py`

---

## 7. Known Issues

| Issue | Severity | Notes |
|-------|----------|-------|
| Contact form does not send an email | Low | The contact form shows a confirmation message on submit but does not actually dispatch an email — this is noted intentionally as a future feature. A backend integration with an email provider (e.g. SendGrid or Django's SMTP backend) would be required to complete this. |
| Canvas hero animation CPU usage | Low | On older mobile devices (pre-2020 iOS), the canvas starfield animation can cause mild frame rate drops. The animation is visually non-essential and a future improvement would be to detect low-performance devices and serve a static background instead. |
| Checkout pre-fill requires profile to exist | Low | If a user registers but does not save a profile first, navigating directly to checkout shows a blank delivery form (the try/except in the view handles this gracefully). A future improvement would be to auto-create the UserProfile record on registration via a signal. |
| Size selector is decorative only | Info | The product detail page includes a size selector (XS–XXL) for UX completeness. Size is not currently stored per OrderLineItem. This is a known limitation for this version and is documented in the README. |
