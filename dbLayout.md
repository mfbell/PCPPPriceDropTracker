# The Database Layout
## Tables
* [Products](#products) - Table of all unique products
* [ProductTypes](#producttypes) - Table of unique product types
* [Offers](#offers) - Table of unique offers (if still active is updated or if same but not active make a new entry)
* [Filters](#filters) - Table of user defined searches

### Products
* **ProductID** - Unique product ID [integer]
* Name - Product name [text]
* *ProductTypeID* - Product Type ID [integer] = [ProductTypes](#producttypes)(ProductTypeID)
* PCPP_URL - PPCP URL [text]

### ProductTypes
* **ProductTypeID** - Unique product type ID [integer]
* Description - Product type [text]

### Offers
* **OfferID** - Unique offer ID [integer]
* Active - Active offer [integer/boolean]
* Displayed - Has been displayed to user [integer/boolean]
* *ProductID* - Product ID [integer] = [Products](#products)(ProductID)
* Normal_Price - The 'Normal Price' for that offer [real]
* Offer_Price - The offer price [real]
* Shop_URL - URL of the shop/product [text]
* Shop_Name - Shop name [text]
* Updated - Last time the offer was seen [real]
* Flames - Highest flame level seen [integer]

### Filters
* **FilterID** - Unique filter ID [integer]
* Name - Filter name [text]
* Filter - Filter phase (e.g. "[WHERE] X='a' and Y='b'") [text]
* Date_Time - Date/Time filter was created [real]
