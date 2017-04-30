# The Database Layout
## Tables
* [Products](#Products)
* [ProductTypes](#ProductTypes)
* [Offers](#Offers)

### Products [Table]
* **ProductID**
* Name
* *ProductTypeID*
* PCPP_URL

### ProductTypes [Table]
* **ProductTypeID**
* Description

### Offers [Table]
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
