# The Database Layout
## Tables
* [Products](#products)
* [ProductTypes](#producttypes)
* [Offers](#offers)

### Products
* **ProductID**
* Name
* *ProductTypeID*
* PCPP_URL

### ProductTypes
* **ProductTypeID**
* Description

### Offers
* **OfferID**
* Active
* Displayed
* *ProductID*
* Normal_Price
* Offer_Price
* Shop_URL
* Shop_Name
* Updated
* Flames
