# The Database Layout
## Tables
* [Products](#products)
* [ProductTypes](#producttypes)
* [Offers](#offers)

### Products
* **ProductID** - Unique product ID [integer]
* Name - Product name [text]
* *ProductTypeID* - Product Type ID [integer] = ProductTypes(ProductTypeID)
* PCPP_URL - PPCP URL [text]

### ProductTypes
* **ProductTypeID** - Unique product type ID [integer]
* Description - Product type [text]

### Offers
* **OfferID** - Unique offer ID [integer]
* Active - Active offer [integer/boolean]
* Displayed - Has been displayed to user [integer/boolean]
* *ProductID* - Product ID [integer] = Products(ProductID)
* Normal_Price - The 'Normal Price' for that offer [real]
* Offer_Price - The offer price [real]
* Shop_URL - URL of the shop/product [text]
* Shop_Name - Shop name [text]
* Updated - Last time the offer was seen [real]
* Flames - Highest flame level seen [integer]
