# NOIR Store - Project Context

## About
NOIR is a premium men's fashion e-commerce store built with Django for a Code Institute PP5 assessment.

**Deadline:** 2026-06-02  
**Repo:** https://github.com/oliveiracle/noir-store  
**Heroku account:** cleinofrank@gmail.com  

---

## CRITICAL RULES

1. **Never run `git commit` or `git push`** — the student must run all git commands themselves so commits appear under their name on GitHub.
2. **One day of work per session** — commits must look like natural daily development for the Code Institute evaluator.
3. **No big bang commits** — never create everything at once.

---

## Stack
- Django 6 + django-allauth (authentication)
- Stripe (payments)
- Bootstrap 5 + custom dark CSS (NOIR theme)
- AWS S3 (media/static in production)
- PostgreSQL (production via Heroku)
- WhiteNoise (static in development)

---

## Visual Style
- Dark theme: background `#0a0a0a`, accent gold `#c9a96e`
- Fonts: Montserrat (headings, bold) + Cormorant Garamond (secondary)
- Inspired by: Zara Man, H&M, ASOS — clean, dark, modern

---

## Apps to Build
- `home` — landing page ✅
- `products` — catalogue, search, filters
- `bag` — shopping cart
- `checkout` — Stripe payments
- `profiles` — user profile + order history
- `reviews` — product reviews (custom model)
- `wishlist` — wishlist (custom model)

---

## Commit Plan
| Day | Work |
|-----|------|
| 1 | Initial Django setup ✅ |
| 2 | Home app + base templates + dark CSS ✅ |
| 3 | Products app + models + product listing |
| 4 | Product detail + search + filters |
| 5 | Bag (shopping cart) |
| 6 | Checkout + Stripe |
| 7 | Profiles + order history |
| 8 | Reviews + Wishlist |
| 9 | SEO (sitemap, robots.txt, meta tags) + Newsletter |
| 10 | GitHub Projects + User Stories (Agile board) |
| 11 | Automated tests |
| 12 | Full README |
| 13 | Heroku deploy + AWS S3 |
| 14 | Final fixes + Lighthouse audit |

---

## Code Institute PP5 Checklist

### Authentication
- [ ] Register, login, logout
- [ ] Email verification (allauth)
- [ ] Password reset

### Products
- [ ] Product listing with category filters
- [ ] Search by name/description
- [ ] Product detail page
- [ ] Admin CRUD (without Django admin panel)

### Bag & Checkout
- [ ] Add/remove/update cart
- [ ] Stripe card payment
- [ ] Stripe webhook
- [ ] Order confirmation email

### Profiles
- [ ] Save default delivery address
- [ ] Order history

### Reviews
- [ ] Authenticated users can review products
- [ ] Rating + comment
- [ ] Edit/delete own review

### SEO & Marketing (required for PP5)
- [ ] sitemap.xml
- [ ] robots.txt
- [ ] Meta tags on all pages
- [ ] Alt attributes on all images
- [ ] Facebook business page mockup
- [ ] Newsletter signup (Mailchimp or simple form)

### Agile
- [ ] GitHub Projects board
- [ ] Issues as User Stories
- [ ] Labels: must have / should have / could have
- [ ] Milestones per sprint

### Testing
- [ ] Manual testing documented in README
- [ ] Automated tests (models + views)
- [ ] HTML validation (W3C)
- [ ] CSS validation (W3C)
- [ ] Lighthouse audit
- [ ] Responsiveness tested

### README
- [ ] Project description
- [ ] UX + User Stories
- [ ] Wireframes
- [ ] Data model (ER diagram)
- [ ] Features
- [ ] Technologies
- [ ] Local setup instructions
- [ ] Deployment steps
- [ ] Credits
