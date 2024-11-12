import requests
from bs4 import BeautifulSoup

def scrape_amazon_by_name(product_name, max_pages=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    # Format the search URL
    base_url = f"https://www.amazon.com/s?k={product_name.replace(' ', '+')}"
    page = 1
    products = []

    while page <= max_pages:
        # Construct the URL for the current page
        search_url = f"{base_url}&page={page}"
        response = requests.get(search_url, headers=headers)

        if response.status_code != 200:
            print(f"Error: Unable to retrieve data from Amazon (Page {page}).")
            break

        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all product items on the current page
        for item in soup.select('.s-main-slot .s-result-item'):
            try:
                title_tag = item.select_one('h2 .a-text-normal')
                price_whole = item.select_one('.a-price-whole')
                price_fraction = item.select_one('.a-price-fraction')
                link_tag = item.select_one('h2 a.a-link-normal')
                image_tag = item.select_one('.s-image')

                # Extract and clean up link if available
                raw_link = link_tag['href'] if link_tag else None
                link = f"https://www.amazon.com{raw_link.split('https://www.amazon.com')[-1]}" if raw_link else None

                # Debug print to see extracted content
                print("Title:", title_tag.get_text(strip=True) if title_tag else "N/A")
                print("Price:", price_whole.get_text(strip=True) if price_whole else "N/A", price_fraction.get_text(strip=True) if price_fraction else "N/A")
                print("Link:", link+"&linkCode=ll1&tag=imsalini-20&linkId=286d198bb5aa51743105df9412685538&language=en_US&ref_=as_li_ss_tl")
                print("Image:", image_tag['src'] if image_tag else "N/A")
                print("-" * 40)

                # Store product information
                product_info = {
                    "title": title_tag.get_text(strip=True) if title_tag else "Title not available",
                    "price": f"{price_whole.get_text(strip=True) if price_whole else ''}.{price_fraction.get_text(strip=True) if price_fraction else ''}".strip('.') if price_whole or price_fraction else "Price not available",
                    "link": link if link else "Link not available",
                    "image": image_tag['src'] if image_tag else "Image not available"
                }

                # Filter out products without a title, price, or link
                if product_info["title"] != "Title not available" and product_info["price"] != "Price not available" and product_info["link"] != "Link not available":
                    products.append(product_info)

            except Exception as e:
                print(f"Error processing item: {e}")

        # Find the "Next" page button and update the page number
        next_button = soup.select_one('.s-pagination-next')
        if next_button and 'href' in next_button.attrs:
            page += 1
        else:
            print("No more pages found.")
            break

    return products
