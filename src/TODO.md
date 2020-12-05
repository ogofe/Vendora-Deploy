## Create a middleware that adds the users cart to the context variable. [FAILED]

## Create a search.html file to show search results. [DONE]

## Create a filters.py file to handle item filtering on
###    - Price
###    - Category
###    - Size

## Create a worker that writes changes to <store_name>-custom-css.css  [DONE]


## Write a documentation on how to add custom html file i.e
###    - Naming Conventions
###    - Available css and js files
###    - How to add custom events (EventBinding) # e.g 
###    let item = document.querySelector("#item").addEventListener("hover", animateHover())


#   2ND DEC. 2020
## Create a mini asynchronuous sub terminal in django to run plugins (if possible ** ask django **)

## Fix updating cart when user logs in with usable password.


## Change how name lookups on stores work (perhaps slugs?). [DONE]

## Remove the ForeignKey "Store" on Product since each product must belong to a store. [DONE]

## Define a get_absolute_url to handle store reverse urls using slugs.

## Change how 'django.contrib.auth.urls' looks for templates i.e use: 'admin/auth/' instead_of: 'registration/'

## Create a hosts.py file for every app to handle its urls using django_hosts.

## Change the Integrations view to show a horizontal slider of each category on mobile devices (max-width: 900px) using rows(x3) and a vertical slider on desktop using cols(x3).


## Auto hide the invoice and items cells on mobile devices (max-width: 900px).

## Plugins should listen for signals that are needed to trigger actions with a receiver method. This method will be called by the store app anytime events happen or failed as well as timely events (for cart abandonment notification). Developers should create plugins with a listener function.

```python3.8.6

# example Plugin
class SimplePlugin:
    name = 'Simple Plugin'

    def listener(self, sender, **kwargs): # as required by django !important
        if kwargs:
            print(arg for arg in kwargs)
            if kwargs['dispatch_id']:
                if kwargs['dispatch_id'] == 'checkout success':
                    for item in sender.products.all():
                        if item.quantity <= self.threshold +5:
                            # raise an alert
                            self.perform_plugin_action()
                        pass
                pass
        print('no kwargs')
        
```