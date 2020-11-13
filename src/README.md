# USE THIS SCHEMA AS A BLUEPRINT FOR CREATING AND MANAGING MODELS.

## SHOPPER SIDE 
User
    - First Name
    - Last Name
    - Username
    - Email
    - Password
    - Billing
    - ShippingAddress

WishList
    - User: User
    - Item 
    - Relative_Price <Price if no discount is available on the time of addage>

Cart
    - User -> User
    - Items

CartItem
    - Cart: Cart
    - Item: Product
    - Quantity

Billing
    - Type
    - Token <Blank until gotten from biller e.g Mastercard, Stripe>

Invoice [CHECKOUT]
    - Number
    - Amount
    - Payer: User
    - Recipient: Store
    - Status: [Pending] [Paid]
    - DateCreated
    - DatePaid

Order
    - Cart
    - Biller: Store
    - Total <Blank momentarily to be filled by the total of the cart and changed when a coupon is redeemed>
    - Billing_Type <Options relative to payment methods added to the biller>

ShippingAddress
    - State
    - City
    - Phone
    - Postal[Optional]
    - Address1
    - Address2[Optional]


## VENDOR SIDE

Vendor
    - Stores

Store
    - Owner: Vendor
    - Logo
    - Products
    - Name
    - Open: Boolean [False]
    - Carousels: Carousel
    - Platforms
    - Customers: User
    - Currency
    - PaymentMethods
    - Invoices
    Attributes
        - Template
        - Background
        - Header
            - Image
            - Title
            - Subtitle
            - Any more content?
        - Nav
            - Display <Option Logo Or Name>
        

Product
    - Store
    - Name
    - Price
    - Description
    - Quantity
    - Category
    - SubCategories
    - Tags
    - DiscountPrice

    Attributes
        - Tag_color

Coupon
    - Store
    - Code
    - Worth
    - Validity: Date

PaymentMethod
    - Client <Type e.g Paypal, Stripe, MasterCard>

Campaign
    - Items: Product
    - Title

Category
    - Name

Tag
    - Name

Currency
    - Name <Type USD OR BPD OR NGN OR EUR IDR>
    - Symbol   <Type $ OR £ OR ₦ OR € OR ₹>



## Direct Buy

Adplacement
    -> Product
    -> Portals <Type Instagram, Craigslist, Facebook>

#### Note to Self
##### portal to facebook stores will allow openAPI fetch products from stores on facebook 
##### and sold on their stores.

