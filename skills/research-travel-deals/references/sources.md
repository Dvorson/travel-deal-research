# Source registry

## Contents

- Refresh and selection rules
- Flight discovery and data adapters
- Stays and regional discovery
- Ground transport
- Experience leads

## Refresh and selection rules

Reviewed 2026-11-14. Treat access, endpoints, commercial terms and geographic coverage as changeable. Open official documentation before integrating a provider. This list is a starting registry, not a claim of exhaustive coverage, uptime or lower prices.

For a trip, select relevant sources by supply coverage and expected decision value. Record supplier family, access mode, supported party/date inputs, live/indicative status, response completeness, pricing/quotas, restrictions and fallback. Count different inventories and supplier types, not domain count. Several sites may resell the same property or airfare.

### Flight discovery and data adapters

- **Google Flights:** https://www.google.com/travel/flights — use date graphs, nearby airports, Best and Cheapest, then supplier verification. Official coverage/features: https://support.google.com/travel/answer/7664728?hl=en . A community Google Flights scraper is an unofficial, replaceable adapter, not an official API or complete inventory.
- **ITA Matrix:** https://matrix.itasoftware.com/ — route/fare construction, sales-city and airport/date exploration. Official help: https://support.google.com/faqs/faq/1739451?hl=en . Research interface; reproduce selected itinerary with an actual seller. Split overly broad searches into narrower passes.
- **Skyscanner:** https://www.skyscanner.net/ — broad/indicative discovery; reprice exact itineraries. Live API: https://developers.skyscanner.net/docs/flights-live-prices/overview . Complete create/poll workflow. Official MCP access is case by case: https://developers.skyscanner.net/docs/mcp-server . API partner criteria: https://www.partners.skyscanner.net/contact/travel-api . Do not assume immediate free integration access.
- **Kiwi official MCP:** https://www.kiwi.com/en/pages/mcp/ — structured supplementary flight search; documented server https://mcp.kiwi.com . Supports adult/child/infant counts and up to +/-3-day flexibility; returns a curated selection, not exhaustive search. Check ticket protection and verify shortlisted sellers.
- **Duffel:** https://duffel.com/guides/getting-started — structured live offers after account activation. Check pricing and authorized research budget: https://duffel.com/pricing . Sandbox distinction: https://duffel.com/docs/api/overview/test-mode . Synthetic test fares are never real travel evidence. Check selected offer/rate, expiry, terms and supported airline content.
- **Amadeus:** https://github.com/amadeus4dev/developer-guides — official Self-Service documentation is deprecated and repository archived July 2026. Do not depend on old self-service onboarding. Confirm current enterprise options separately: https://developers.amadeus.com/api-catalog . Do not generalize retirement of Self-Service to all Amadeus services.
- **Direct airlines and airport route maps:** discover missing seasonal, low-cost and regional routes; verify date-specific fares with the operating/selling carrier. Route maps are leads, not availability.
- **Leisure flight-only/packages:** https://www.tui.nl/vliegtickets/ and relevant destination/source-market tour operators. Compare actual package inclusions against independent components. Do not assume a charter seat or package is absent just because a mainstream flight search does not show it.
- **Rewards specialists:** choose only for eligible programmes and balances; verify availability and charges with the actual loyalty programme before valuing an award. Provider/tool access and programme rules require a fresh check.

### Stays and regional discovery

- **Broad discovery:** Booking.com, Airbnb, Google Hotels, and a relevant rental/metasearch alternative. Use full party and stay dates; public web inventory and a commercial API can differ. Booking Demand access requires a managed affiliate arrangement: https://developers.booking.com/demand/docs/getting-started/prerequisites . Child policy: https://developers.booking.com/demand/docs/accommodations/child-policies . Discount/eligibility documentation: https://developers.booking.com/demand/docs/accommodations/discounts . Do not present an unofficial Airbnb MCP as official; inspect its actual host capability and page parsing before trusting it.
- **Portugal/Madeira:** https://visitmadeira.com/en/where-to-stay/accommodations/ for local lodging, rural tourism and managers. Example direct-channel discovery: https://visitmadeira.com/en/where-to-stay/accommodations/an-island-apart/ . Registration identity: https://rnt.turismodeportugal.pt/ . A directory/registry is not a live availability feed.
- **France:** https://www.gites-de-france.com/en — gîtes, guest houses and other regional lodging. Check weekly/changeover patterns and total charges.
- **Italy:** https://en.agriturismo.it/ — farm-stay discovery; confirm the actual seller and unit. Relevant when the trip fits rural accommodation.
- **Austria:** https://www.farmholidays.com/en — farm accommodation, apartments and cabins; compare direct supplier terms.
- **Spain:** https://www.escapadarural.com/ — rural accommodation discovery; distinguish whole house from individual rooms.
- **Japan:** official JNTO directory https://www.japan.travel/en/online-reservation-sites/ lists regional channels including Jalan, Rakuten Travel and JAPANiCAN. Compare meal plans, bedding, bathing/toilet configuration and child categories. Native-language offers may have different eligibility.
- **University rooms:** https://www.universityrooms.com/en-GB/about/ — vacant university accommodation can be available to non-students. Check actual holiday dates, bathroom/age restrictions and location.
- **Religious guest houses:** https://www.monasterystays.com/blog/about-us/ and https://www.monasteries.com/en-GB/about — conditional lodging category. Verify family eligibility, curfew, bathroom, meals and access.
- **Home exchange:** https://www.homeexchange.com/p/how-it-works-en — consider only with user interest, membership/points and ability to satisfy the exchange terms. Pending host acceptance is not confirmed accommodation; membership and other costs mean it is not free.

Do not force every regional portal into every search. Discover the destination's equivalent categories using native terms and official tourism sources. For an unfamiliar region, identify one meaningful regional channel and one independently identifiable direct supplier before declaring local inventory covered.

### Ground transport

- **Rome2Rio:** https://www.rome2rio.com/ — discover modes/operators, then verify dates/times and fares. Price methodology: https://rome2rio.freshdesk.com/en/support/solutions/articles/22000239374-how-do-you-determine-your-prices- . Estimated route cost is not a booking quote.
- **Europe rail:** direct railway operators, https://www.nsinternational.com/ for Dutch international journeys, relevant national booking sites and one appropriate aggregator. Check sales opening and children's fare rules: https://www.nsinternational.com/en/buy-train-tickets/when-book-train-tickets and https://www.nsinternational.com/en/train-fares-and-discounts/travelling-with-children . For UK split tickets use https://www.nationalrail.co.uk/tickets-railcards-and-offers/buying-a-ticket/split-train-tickets/ and validate local exceptions.
- **Southeast Asia multimodal:** https://12go.asia/en/FAQ and https://12go.co/en/about — bus, rail, ferry, minivan and transfers. Compare an identifiable direct operator when available; inspect ticket issuance, baggage and connection terms.
- **Ferries:** https://www.ferryhopper.com/ and direct ferry operators. Terms: https://www.ferryhopper.com/en/terms . Recheck fees and separately ticketed connections rather than assuming every combination is protected.
- **Local public transit:** airport authority ground-transport page and the municipal/regional operator; confirm actual-date last service and holiday timetable. Transitland/Navitia can support route discovery, but are not universal saleable fare inventory: https://www.transit.land/documentation/rest-api/ and https://doc.navitia.io/ .
- **Vehicle relocation:** https://www.driiveme.com/en-GB/frequently-asked-questions.html and https://www.transfercar.com.au/what-is-a-vehicle-relocation-how-it-works — highly conditional, flexible routing branch; include mileage, days, fuel, insurance and deposits.

### Experience leads

- Secret Flying FAQ: https://www.secretflying.com/faq/
- HolidayPirates: https://www.holidaypirates.com/about-us
- FlyerTalk deal forums: https://www.flyertalk.com/forum/mileage-run-deals-372/
- Destination-specific forums, local communities and recent traveller reports.

Use these to discover hypotheses, sellers or route combinations. Treat affiliate rankings and headline discounts as unverified claims. Reproduce the actual party, dates and terms on a current supplier source before recommending a deal.
